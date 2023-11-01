from NTFS.boot_sector import BootSector
from NTFS.mft_entry import MFTEntry
from NTFS.directory_tree import DirTree
from utils import parse_path

from icecream import ic

# ------------------------------------
# NTFS
# ------------------------------------
class NTFS:
    def __init__(self, vol_name: str) -> None:
        self.name = vol_name

        # use to read data
        self.__f = open(r'\\.\%s' % self.name, "rb")
        self.__f.seek(0)

        # first read boot sector
        # boot sector took first 512 bytes of disk
        data = self.__f.read(512)
        self.__boot_sector = BootSector(data)

        # move the pointer to the offset of $MFT entry
        mft_offset = self.__boot_sector.starting_cluster_MFT * self.__boot_sector.bytes_per_cluster
        self.__f.seek(mft_offset)

        # and then read $MFT entry
        data = self.__f.read(self.__boot_sector.bytes_per_entry)
        self.__mft_entry = MFTEntry(data)

        # find number sector of entire MFT table
        # First VCN (virtual cluster number) is 0 and Number Last VCN at byte 24 (after $STANDARD_INFORMTION offset) 
        # and has length LONGLONG
        # So number of vcn = last_vcn + first_vcn + 1 (because start at 0)
        # Then sector = no_vcn * sectors_per_clusterr
        start_byte = self.__mft_entry.attributes[0x80].start_offset + 24
        no_vcn = int.from_bytes(data[start_byte : start_byte + 8],
                                byteorder="little") + 1
        no_sector = no_vcn * self.__boot_sector.sectors_per_cluster

        # finally read all remaining entries to a list
        self.entry_list = []

        sector_per_entry = int(self.__boot_sector.bytes_per_entry / self.__boot_sector.bytes_per_sector)
        entry_count = 2

        for _ in range(sector_per_entry, no_sector, sector_per_entry):
            data = self.__f.read(self.__boot_sector.bytes_per_entry)
            # we want to skip entry from 13 -> 16
            try:
                if entry_count >= 13 and entry_count <= 16:
                        entry_count += 1
                        continue
                entry = MFTEntry(data)
                self.entry_list.append(entry)
                entry_count += 1
            except:
                continue

        # directory tree
        self.dir_tree = DirTree(self.entry_list)

        # use for cwd command
        self.cwd = []
        self.cwd.append(self.name)

    # ------------------------------------
    # Property
    # ------------------------------------
    @property
    def boot_sector_info(self) -> str:
        return f"Volume name: {self.name[0]}" + str(self.__boot_sector)

    # ------------------------------------
    # Method
    # ------------------------------------
    @staticmethod
    def check_ntfs(vol_name) -> bool:
        with open(r'\\.\%s' % vol_name, "rb") as f:
            oem_name = f.read(512)[0x03 : 0x03 + 8].decode()
            if oem_name == "NTFS    ":
                return True
            else:
                return False

    def access_dir(self, path):
        path = parse_path(path)
        current_dir = None

        #If path is in other directory
        if path[0] == self.name:
            current_dir = self.dir_tree.root
            path.pop(0)
        #If path is child of current directory
        else:
            current_dir = self.dir_tree.current_node

        for dir in path:
            if dir == "..":
                current_dir = self.dir_tree.find_parent_entry(current_dir)
            elif dir == ".":
                continue

            current_dir = current_dir.find_child_entry(dir)
       
            if current_dir is None:
                raise Exception("Not found")
            elif not current_dir.is_directory():
                raise Exception("Not directory")
            
        return current_dir

    def get_dir_info(self, path):
        if path != "":
            current_dir = self.access_dir(path)
        else:
            current_dir = self.dir_tree.current_node

        list_active_childen = current_dir.get_active_children()

        list_child_info = []

        for child in list_active_childen:
            info = {}
            info["Flags"] = child.attributes[0x10].file_status
            info["Name"] = child.name
            info["Last Modified"] = child.attributes[0x10].last_modified_time

            if child.is_directory():
                info["Sector Offset"] = self.__boot_sector.starting_cluster_MFT * self.__boot_sector.sectors_per_cluster + child.id

            if child.attributes[0x80].is_resident():
                info["Sector Offset"] = self.__boot_sector.starting_cluster_MFT * self.__boot_sector.sectors_per_cluster + child.id
            else:
                info["Sector Offset"] = child.attributes[0x80].first_cluster * self.__boot_sector.sectors_per_cluster

            list_child_info.append(info)

        return list_child_info

    def change_dir(self, path):
        if path == "":
            raise Exception("Path is required")
        
        #Access the path
        current_dir = self.access_dir(path)

        #Update the current node of the tree
        self.dir_tree.current_node = current_dir
        dirs = parse_path(path)

        #Update the cwd
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
    
    def get_cwd(self) -> str:
        if len(self.cwd) == 1:
            return self.cwd[0] + "\\"
        return "\\".join(self.cwd)

    def get_text_file(self, path: str):
        path = parse_path(path)

        if len(path) == 1:
            entry = self.dir_tree.find_child_entry(path[0])
        else:
            dir = self.access_dir("\\".join(path[0:-1]))
            entry = dir.find_child_entry(path[-1])

        if entry is None:
            raise Exception(f"File {path[-1]} does not exists")

        if entry.is_directory():
            raise Exception(f"{path[-1]} is not a file")

        entry_data = entry.attributes[0x80]

        if entry_data.is_resident():
            try:
                data = entry_data.content_data.decode()
            except UnicodeDecodeError as e:
                raise Exception("Not a .txt file.")
            return data
        else:
            data = ""

            real_size = entry_data.real_size

            first_cluster_bytes = entry_data.first_cluster * self.__boot_sector.bytes_per_cluster

            self.__f.seek(first_cluster_bytes)

            for _ in range(0, entry_data.cluster_count):
                if real_size <= 0:
                    break

                raw_data = self.__f.read(min(self.__boot_sector.bytes_per_cluster, real_size))

                real_size -= self.__boot_sector.bytes_per_cluster

                try:
                    data += raw_data.decode()
                except UnicodeDecodeError as e:
                    raise Exception("Not a .txt file")

            return data