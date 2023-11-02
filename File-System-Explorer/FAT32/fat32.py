from FAT32.bootsector import BootSector
from FAT32.fat import FAT
from FAT32.rdet import RDET
from utils import parse_path

from icecream import ic

class FAT32:
    def __init__(self,vol_name) -> None:
        self.name= vol_name

        self.cwd=[vol_name]

        try:
            self.fd= open(r'\\.\%s'%self.name,'rb')
        except PermissionError:
            raise PermissionError

        try:
            boot_sector_raw = self.fd.read(0x200)
        except Exception as e:
            raise e
            
        # Read bootsector
        self.bootsector = BootSector(boot_sector_raw)
        
        # Read reversed sector
        self.reversed_sector = self.fd.read(self.bootsector.bytes_per_sector*(self.bootsector.reserved_sectors-1))
        
        # Read FAT table
        self.FAT_table:list[FAT]=[]
        self.read_FAT_table()
        
        # Read RDET
        self.DET={} # To archive DET of all folder in Root directory
        self.RDET= RDET(self.get_cluster_data(self.bootsector.start_cluster_RDET))
        self.DET[self.bootsector.start_cluster_RDET] =self.RDET

    @property
    def boot_sector_info(self) -> str:
        return f"Volume name: {self.name[0]}" + str(self.bootsector)
    
    """ Methods """
    def get_cwd(self):
        if len(self.cwd) == 1:
            return self.cwd[0] + "\\"
        return "\\".join(self.cwd)
    
    # Cluster to sector index
    def cluster_to_sector(self,clusterIndex):
        return self.bootsector.reserved_sectors+self.bootsector.number_of_FAT_table*self.bootsector.sectors_per_FAT+(clusterIndex-2)*self.bootsector.sectors_per_cluster
    
    # Read FAT table
    def read_FAT_table(self):
        FAT_size = self.bootsector.sectors_per_FAT* self.bootsector.bytes_per_sector
        for _ in range(self.bootsector.number_of_FAT_table):
            self.FAT_table.append(FAT(self.fd.read(FAT_size)))

    # Get cluster data
    def get_cluster_data(self, clusterIndex):
        index_list=self.FAT_table[0].get_chain(clusterIndex)
        data= b""
        for i in index_list:
            offset = self.cluster_to_sector(i)
            self.fd.seek(offset*self.bootsector.bytes_per_sector)
            data+=self.fd.read(self.bootsector.sectors_per_cluster*self.bootsector.bytes_per_sector)
        return data
          
    # Visit dir
    def access_dir(self,path)-> RDET:
        dirs = parse_path(path)
        
        if dirs[0]==self.name:
            currentDET = self.RDET
            dirs.pop(0)
        else:
            currentDET= self.RDET
        
        for d in dirs:
            entry = currentDET.find_entry(d)
            if entry is None:
                raise Exception("Not found!")
            if entry.is_directory():
                # If entry is RDET
                if entry.start_cluster==0:
                    currentDET= self.DET[self.bootsector.start_cluster_RDET]
                    continue
                # If exists entry before => Saving time for reading again DET
                if entry.start_cluster in self.DET:
                    currentDET = self.DET[entry.start_cluster]
                    continue
                # If not exists, read DET of folder
                self.DET[entry.start_cluster]=RDET(self.get_cluster_data(entry.start_cluster))
                # Set folder to current DET 
                currentDET = self.DET[entry.start_cluster]
            else:
                raise Exception("Not directory")
        return currentDET
                
    # Get directory
    def get_dir_info(self, path):
        if path!="":
            currentDET= self.access_dir(path)
            entry_list = currentDET.get_active_entries()
        else:
            entry_list= self.RDET.get_active_entries()

        ret = []
        for entry in entry_list:
            obj={}
            obj["Flags"]= entry.attr
            obj["Last Modified"] = entry.date_updated
            obj["Size"] = entry.size
            obj["Name"] = entry.long_name
            if entry.start_cluster == 0:
                obj["Sector Offset"] = (entry.start_cluster + 2) * self.bootsector.sectors_per_cluster
            else:
                obj["Sector Offset"] = entry.start_cluster * self.bootsector.sectors_per_cluster
            ret.append(obj)
        return ret
        
    # Change dir
    def change_dir(self, path=""):
        if path == "":
            raise Exception("Path is required")

        currentDET = self.access_dir(path)
        self.RDET = currentDET    

        #Update the cwd
        dirs = parse_path(path)
        if dirs[0] == self.name:
            self.cwd.clear()
            self.cwd.append(self.name)
            dirs.pop(0)
        for d in dirs:
            if d == "..":
                if len(self.cwd) > 1: 
                    self.cwd.pop()
            elif d != ".":
                self.cwd.append(d)
            
    # Check FAT32         
    @staticmethod
    def check_fat32(name: str):
        try:
            with open(r'\\.\%s' % name, 'rb') as fd:
                fd.read(1)
                fd.seek(0x52)
                fat_name = fd.read(8)
                if fat_name == b"FAT32   ":
                    return True
                return False
        except PermissionError:
            raise PermissionError
    
    # Read text file
    def get_text_file(self,path):
        path= parse_path(path)
        
         # ../abc/text.txt
        if len(path)>1:
            name= path[-1]
            path = "\\".join(path[:-1])
            currentDet = self.access_dir(path)
            entry = currentDet.find_entry(name)
        else:
            # text.txt
            entry = self.RDET.find_entry(path[0])
        
        if entry is None:
            raise Exception(f"File {path[-1]} does not exists")
        if entry.is_directory():
            raise Exception(f"{path[-1]} is not a file")
        
        # Get data cluster list from FAT table
        index_list = self.FAT_table[0].get_chain(entry.start_cluster)
        data=""
        size_left = entry.size
        for i in index_list:
            if size_left<=0:
                break
            # Get sector offset
            offset = self.cluster_to_sector(i)
            # Seek offset (byte)
            self.fd.seek(offset*self.bootsector.bytes_per_sector)
            # Read 1 data cluster. If left data < cluster size then read size left
            raw_data=self.fd.read(min(self.bootsector.sectors_per_cluster*self.bootsector.bytes_per_sector, size_left))
            size_left -= self.bootsector.sectors_per_cluster*self.bootsector.bytes_per_sector   
            try:
                data+= raw_data.decode()
            except UnicodeDecodeError as e:
                raise Exception("Not a .txt file")

        return data
            
    def __del__(self):
        if getattr(self, "fd", None):
            self.fd.close()

    def __str__(self):
        return "FAT32"