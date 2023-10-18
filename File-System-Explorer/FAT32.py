class FAT32:
    important_info = [
        "Bytes Per Sector",
        "Sectors Per Cluster",
        "Reserved Sectors", 
        "Sectors Per FAT",
        "No. Copies of FAT",
        "No. Sectors In Volume",
        "Starting Cluster of RDET",
        "Starting Sector of Data",
        "FAT Name"
    ]
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
        self.boot_sector['Jump_Code'] = self.boot_sector_raw[:3]
        self.boot_sector['OEM_ID'] = self.boot_sector_raw[3:0xB]
        self.boot_sector['Bytes Per Sector'] = int.from_bytes(self.boot_sector_raw[0xB:0xD], byteorder='little')
        self.boot_sector['Sectors Per Cluster'] = int.from_bytes(self.boot_sector_raw[0xD:0xE], byteorder='little')
        self.boot_sector['Reserved Sectors'] = int.from_bytes(self.boot_sector_raw[0xE:0x10], byteorder='little')
        self.boot_sector['No. Copies of FAT'] = int.from_bytes(self.boot_sector_raw[0x10:0x11], byteorder='little')
        self.boot_sector['Media Descriptor'] = self.boot_sector_raw[0x15:0x16]
        self.boot_sector['Sectors Per Track'] = int.from_bytes(self.boot_sector_raw[0x18:0x1A], byteorder='little')
        self.boot_sector['No. Heads'] = int.from_bytes(self.boot_sector_raw[0x1A:0x1C], byteorder='little')
        self.boot_sector['No. Sectors In Volume'] = int.from_bytes(self.boot_sector_raw[0x20:0x24], byteorder='little')
        self.boot_sector['Sectors Per FAT'] = int.from_bytes(self.boot_sector_raw[0x24:0x28], byteorder='little')
        self.boot_sector['Flags'] = int.from_bytes(self.boot_sector_raw[0x28:0x2A], byteorder='little')
        self.boot_sector['FAT32 Version'] = self.boot_sector_raw[0x2A:0x2C]
        self.boot_sector['Starting Cluster of RDET'] = int.from_bytes(self.boot_sector_raw[0x2C:0x30], byteorder='little')
        self.boot_sector['Sector Number of the FileSystem Information Sector'] = self.boot_sector_raw[0x30:0x32]
        self.boot_sector['Sector Number of BackupBoot'] = self.boot_sector_raw[0x32:0x34]
        self.boot_sector['FAT Name'] = self.boot_sector_raw[0x52:0x5A]
        self.boot_sector['Executable Code'] = self.boot_sector_raw[0x5A:0x1FE]
        self.boot_sector['Signature'] = self.boot_sector_raw[0x1FE:0x200]
        self.boot_sector['Starting Sector of Data'] = self.boot_sector['Reserved Sectors'] + self.boot_sector['No. Copies of FAT'] * self.boot_sector['Sectors Per FAT']
        
    
                