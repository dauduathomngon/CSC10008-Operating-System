import sys
class FAT:
    def __init__(self, data) -> None:
        self.entry_size = 4
        self.elements=[]
        self.data = data
        for i in range(0, len(data),self.entry_size):
            self.elements.append(int.from_bytes(self.data[i:i+4],byteorder=sys.byteorder))

    def get_chain(self, index:int)-> list[int]:
        index_list = []
        while True:
            index_list.append(index)
            index = self.elements[index]
            if index == 0x0FFFFFFF or index == 0x0FFFFFF7:
                break
            return index_list 
class FAT32:
    # Constructor - Format name example: "D:"
    def __init__(self, name:str) -> None:
        self.name = name
        try:
            self.fd= open(r'\\.\%s'%self.name,'rb')
        # Handle error
        except FileNotFoundError:
            print(f"[ERROR] No volume named {name}")
            exit()
        except PermissionError:
            print("[ERROR] Permission denied, try again as administrator/root")
            exit()
        except Exception as e:
            print(e)
            print(f"[ERROR] {e} ")
            exit() 
            
        try:
            # Read 512 bytes (0x200 hex = 512 dec)
            self.boot_sector_raw = self.fd.read(0x200)
            # Declare dictionary to save data
            self.boot_sector = {}
            # Reading bootsector (Read and convert boot_sector_raw)
            self.reading_boot_sector()
            # Read FAT table
            self.FAT_size
            self.FAT_table:list[FAT]=[]
            self.readFAT_table()
            
        except Exception as e:
            print(f"[Error] {e}")
            
            
    # Check if FAT32
    @staticmethod
    def check_fat32(name: str):
        try:
            with open(r'\\.\%s' % name, 'rb') as fd:
                fd.read(1)
                # Move cursor to offset 0x52
                fd.seek(0x52)
                # Read 8 bytes
                fat_name = fd.read(8)
                if fat_name == b"FAT32   ":
                    return True
                return False
        except Exception as e:
            print(f"[ERROR] {e}")
            exit()
           
    # Reading boot sector
    def reading_boot_sector(self):
         # Jump Boot code: Offset 0 size 3
        self.boot_sector['Jump_Code'] = self.boot_sector_raw[:3]
        # OEM Name: offset 3 size 8
        self.boot_sector['OEM_ID'] = self.boot_sector_raw[3:0xB]
        # Bytes per sector: offset B size 2
        self.boot_sector['Bytes Per Sector'] = int.from_bytes(self.boot_sector_raw[0xB:0xD], byteorder=sys.byteorder)
        # Sector per cluster: offset D size 1
        self.boot_sector['Sectors Per Cluster'] = int.from_bytes(self.boot_sector_raw[0xD:0xE], byteorder=sys.byteorder)
        # Reserved sectors count: offset E size 2
        self.boot_sector['Reserved Sectors'] = int.from_bytes(self.boot_sector_raw[0xE:0x10], byteorder=sys.byteorder)
        # Number of FAT tables: offset 10 size 1
        self.boot_sector['No. Copies of FAT'] = int.from_bytes(self.boot_sector_raw[0x10:0x11], byteorder=sys.byteorder)
        # Volume type: offset 15 size 1
        self.boot_sector['Media Descriptor'] = self.boot_sector_raw[0x15:0x16]
        # Sectors per track: offset 18 size 2
        self.boot_sector['Sectors Per Track'] = int.from_bytes(self.boot_sector_raw[0x18:0x1A], byteorder=sys.byteorder)
        # Number of heads: offset 1A size 2
        self.boot_sector['No. Heads'] = int.from_bytes(self.boot_sector_raw[0x1A:0x1C], byteorder=sys.byteorder)
        # Number of sectors in volume: offset 20 size 4
        self.boot_sector['No. Sectors In Volume'] = int.from_bytes(self.boot_sector_raw[0x20:0x24], byteorder=sys.byteorder)
        # Number of sectors in a FAT table: offset 24 size 4
        self.boot_sector['Sectors Per FAT'] = int.from_bytes(self.boot_sector_raw[0x24:0x28], byteorder=sys.byteorder)
        # Ext Flags: offset 28 size 2
        self.boot_sector['Flags'] = int.from_bytes(self.boot_sector_raw[0x28:0x2A], byteorder=sys.byteorder)
        # FAT32 version: offset 2A size 2
        self.boot_sector['FAT32 Version'] = self.boot_sector_raw[0x2A:0x2C]
        # Starting cluster RDET: offset 2C size 2
        self.boot_sector['Starting Cluster of RDET'] = int.from_bytes(self.boot_sector_raw[0x2C:0x30], byteorder=sys.byteorder)
        # Sector Number of the FileSystem Information Sector: offset 30 size 2
        #self.boot_sector['Sector Number of the FileSystem Information Sector'] = self.boot_sector_raw[0x30:0x32]
        # Sector Number of BackupBoot: offset 32 size 2
        #self.boot_sector['Sector Number of BackupBoot'] = self.boot_sector_raw[0x32:0x34]
        # FAT type: offset 52 size 8
        self.boot_sector['FAT Name'] = self.boot_sector_raw[0x52:0x5A]
        # Boot code: offset 5A siuze 420
        #self.boot_sector['Executable Code'] = self.boot_sector_raw[0x5A:0x1FE]
        # Signature: offset 1FE size 2
        self.boot_sector['Signature'] = self.boot_sector_raw[0x1FE:0x200]
        # Starting sector of data
        self.boot_sector['Starting Sector of Data'] = self.boot_sector['Reserved Sectors'] + self.boot_sector['No. Copies of FAT'] * self.boot_sector['Sectors Per FAT']
        
        
    # Read FAT table
    def readFAT_table(self)->None:
            self.FAT_size = self.boot_sector['Bytes Per Sector']*self.boot_sector['Sectors Per FAT']
            for _ in range(self.boot_sector['No. Copies of FAT']):
                self.FAT_table.append(FAT(self.fd.read(self.FAT_size)))
                
    def show(self)-> None:
        for key, value in self.boot_sector.items():
            print(f"{key}: {value}")
    