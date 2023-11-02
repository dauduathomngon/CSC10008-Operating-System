import sys
class BootSector:
    def __init__(self,data) -> None:
        self.boot_sector_raw = data
        
    @property
    # Jump Boot code: Offset 0 size 3
    def jump_code(self):
        return int.from_bytes(self.boot_sector_raw[:3], byteorder="little")
    
    @property
    # OEM Name: offset 3 size 8
    def OEM_id(self):
        return self.boot_sector_raw[3:0xB]
    
    @property
    # Bytes per sector: offset B size 2
    def bytes_per_sector(self):
        return int.from_bytes(self.boot_sector_raw[0xB:0xD], byteorder=sys.byteorder)
    
    @property
    # Sector per cluster: offset D size 1
    def sectors_per_cluster(self):
        return int.from_bytes(self.boot_sector_raw[0xD:0xE], byteorder=sys.byteorder)
    
    @property
    # Reserved sectors count: offset E size 2
    def reserved_sectors(self):
        return int.from_bytes(self.boot_sector_raw[0xE:0x10], byteorder=sys.byteorder)
    
    @property
    # Number of FAT tables: offset 10 size 1
    def number_of_FAT_table(self):
        return int.from_bytes(self.boot_sector_raw[0x10:0x11], byteorder=sys.byteorder)
    
    @property
    # Volume type: offset 15 size 1
    def volume_type(self):
        return self.boot_sector_raw[0x15:0x16]
    
    @property
    # Sectors per track: offset 18 size 2
    def sectors_per_track(self):
        return int.from_bytes(self.boot_sector_raw[0x18:0x1A], byteorder=sys.byteorder)
    
    @property
    # Number of heads: offset 1A size 2
    def number_of_head(self):
        return int.from_bytes(self.boot_sector_raw[0x1A:0x1C], byteorder=sys.byteorder)
    
    @property
    # Number of sectors in volume: offset 20 size 4
    def number_sectors_in_volume(self):
        return int.from_bytes(self.boot_sector_raw[0x20:0x24], byteorder=sys.byteorder)
    
    @property
    # Number of sectors in a FAT table: offset 24 size 4
    def sectors_per_FAT(self):
        return int.from_bytes(self.boot_sector_raw[0x24:0x28], byteorder=sys.byteorder)
    
    @property
    # Ext Flags: offset 28 size 2
    def ext_flag(self):
        return int.from_bytes(self.boot_sector_raw[0x28:0x2A], byteorder=sys.byteorder)
    
    @property
    #FAT32 version: offset 2A size 2
    def FAT_version(self):
        return self.boot_sector_raw[0x2A:0x2C]
    
    @property
    # Starting cluster RDET: offset 2C size 2
    def start_cluster_RDET(self):
        return int.from_bytes(self.boot_sector_raw[0x2C:0x30], byteorder=sys.byteorder)
    
    @property
    # Sector Number of the FileSystem Information Sector: offset 30 size 2
    def filesystem_info_sector(self):
        return self.boot_sector_raw[0x30:0x32]
    
    @property
    #Sector Number of BackupBoot: offset 32 size 2
    def backupRoot_sector(self):
        return self.boot_sector_raw[0x32:0x34]
    
    @property
    # FAT type: offset 52 size 8
    def FAT_name(self):
        return self.boot_sector_raw[0x52:0x5A].decode()

    @property
    # Boot code: offset 5A size 420
    def boot_code(self):
        return self.boot_sector_raw[0x5A:0x1FE]
    
    @property
    # Signature: offset 1FE size 2
    def signature(self):
        return self.boot_sector_raw[0x1FE:0x200]
    
    @property
    # Starting sector of data
    def data_sector_start(self):
        return self.reserved_sectors+self.number_of_FAT_table*self.sectors_per_FAT
    
    # Show infomation     
    def described(self):
        return (
            ("Jump code", self.jump_code),
            ("OEM_ID", self.OEM_id),
            ("Bytes per sector", self.bytes_per_sector),
            ("Reversed sector", self.reserved_sectors),
            ("Number of FAT table", self.number_of_FAT_table),
            ("Sectors per track", self.sectors_per_track),
            ("Number of head", self.number_of_head),
            ("Number of sector in volume", self.number_sectors_in_volume),
            ("Start cluster of RDET", self.start_cluster_RDET),
            ("Sectors per FAT", self.sectors_per_FAT),
            ("Sectors per cluster", self.sectors_per_cluster)
        )

    def __str__(self):
        s = "\nVolume Information from Boot Sector:\n"
        for name, value in self.described():
            s += f"\t{name}: {value}\n"
        return s