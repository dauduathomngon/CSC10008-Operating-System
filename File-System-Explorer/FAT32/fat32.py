from FAT32.bootsector import BootSector
from FAT32.fat import FAT
from FAT32.rdet import RDET
import re
class FAT32:
    def __init__(self,vol_name) -> None:
        self.name= vol_name
        try:
            self.fd= open(r'\\.\%s'%self.name,'rb')
        except FileNotFoundError:
            print(f"[ERROR] No volume named {self.name}")
            exit()
        except PermissionError:
            print("[ERROR] Permission denied, try again as admin/root")
            exit()
        except Exception as e:
            print(e)
            print("[ERROR] Unknown error occurred")
            exit() 
        try:
            boot_sector_raw = self.fd.read(0x200)
        except Exception as e:
            print(f"[Error] {e}")
            exit()
            
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
    
    
    
    """ Methods """
    # Parse path
    def parse_path(self, path):
        dirs = re.sub(r"[/\\]+", r"\\", path).strip("\\").split("\\")
        return dirs
    
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
    def visit_dir(self,path)-> RDET:
        if path=="":
            raise Exception("Directory name is required!")
        dirs = self.parse_path(path)
        
        if dirs[0]==self.name:
            currentDET = self.RDET
            dirs.pop(0)
        else:
            currentDET= self.RDET
        
        for d in dirs:
            entry = currentDET.find_entry(d)
            if entry is None:
                raise Exception("Directory not found!")
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
                raise Exception("Not a directory")
        return currentDET
                
    # Get directory
    def get_dir(self, path):
        try:
            if path!="":
                currentDET= self.visit_dir(path)
                entry_list = currentDET.get_active_entries()
                
            else:
                entry_list= self.RDET.get_active_entries()
            ret = []
            for entry in entry_list:
                obj={}
                obj["Flags"]= entry.attr.value
                obj["Date Modified"] = entry.date_updated
                obj["Size"] = entry.size
                obj["Name"] = entry.long_name
                if entry.start_cluster == 0:
                    obj["Sector"] = (entry.start_cluster + 2) * self.bootsector.sectors_per_cluster
                else:
                    obj["Sector"] = entry.start_cluster * self.bootsector.sectors_per_cluster
                ret.append(obj)
            return ret
        except Exception as e:
            raise(e)
        
    # Change dir
    def change_dir(self, path=""):
        if path == "":
            raise Exception("Path to directory is required!")
        currentDET = self.visit_dir(path)
        self.RDET = currentDET    
            
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
        except Exception as e:
            print(f"[ERROR] {e}")
            exit()    
    
    
    def __del__(self):
        if getattr(self, "fd", None):
            print("Closing Volume...")
            self.fd.close()