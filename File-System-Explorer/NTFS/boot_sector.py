import sys
import binascii
from const import LONGLONG, WORD, BYTE

class BootSector:
    # Taken from: http://ntfs.com/ntfs-partition-boot-sector.htm
    OEM_ID = "OEM ID"
    BYTES_PER_SECTOR = "Bytes Per Sector"
    SECTORS_PER_CLUSTER = "Sectors Per Cluster"
    RESERVED_SECTORS = "Reserved Sectors"
    TOTAL_SECTORS = "Total Sectors"
    SECTORS_PER_CLUSTER = "Sector Per Cluster"
    STARTING_CLUSTER_MFT = "Starting cluster of $MFT"
    STARTING_CLUSTER_MFTMIRR = "Starting cluster of $MFTMirr"
    BYTES_PER_ENTRY = "Bytes Per Entry"
    SERIAL_NUMBER = "Serial Volume Number"
    BYTES_PER_CLUSTER = "Bytes Per Cluster"

    def __init__(self, data) -> None:
        self.data = data

    @property
    def oem_id(self) -> str:
        # oem_id at offset 0x03 and has length LONGLONG (8 bytes)
        return self.data[0x03 : 0x03 + LONGLONG].decode()

    @property
    def bytes_per_sector(self) -> int:
        # bytes_per_sector at offset 0x0B and has length WORD (2 bytes)
        return int.from_bytes(self.data[0x0B : 0x0B + WORD],
                              byteorder="little")

    @property
    def sectors_per_cluster(self) -> int:
        # sectors_per_cluster at offset 0x0D and has length BYTE
        return int.from_bytes(self.data[0x0D : 0x0D + BYTE],
                              byteorder="little")

    @property 
    def total_sectors(self) -> int:
        # total_sectors at offset 0x28 and has length LONGLONG
        return int.from_bytes(self.data[0x28 : 0x28 + LONGLONG],
                              byteorder="little")

    @property
    def starting_cluster_MFT(self) -> int:
        # starting_cluster_MFT at offset 0x30 and has length LONGLONG
        return int.from_bytes(self.data[0x30 : 0x30 + LONGLONG],
                              byteorder="little")
    
    @property
    def starting_cluster_MFTMirr(self) -> int:
        # starting_cluster_MFTMirr at offset 0x38 and has length LONGLONG
        return int.from_bytes(self.data[0x38 : 0x38 + LONGLONG],
                              byteorder="little")
    
    @property
    def bytes_per_cluster(self) -> int:
        return self.bytes_per_sector * self.sectors_per_cluster

    @property
    def bytes_per_entry(self) -> int:
        # Clusters_Per_File_Record_Segment at offset 0x40 and has length DWORD (4 byte)
        # But we only need first byte (called segment)
        # segment can be:
        # - positive: it shows number of clusters per entry.
        # - negative: it shows number of bytes of entry in log2
        # (segment is negative because size of cluster > size of entry)
        segment = int.from_bytes(self.data[0x40 : 0x40 + BYTE], byteorder=sys.byteorder, signed=True)
        if segment > 0:
            return segment * self.bytes_per_cluster
        else:
            return 2**abs(segment)

    @property
    def reserved_sectors(self) -> int:
        # reserved_sectors at offset 0x0E and has length WORD
        return int.from_bytes(self.data[0x0E : 0x0E + WORD],
                              byteorder="little")

    @property
    def serial_number(self):
        # serial_number at offset 0x48 and has length LONGLONG
        return binascii.hexlify(self.data[0x48 : 0x48 + LONGLONG]).decode("utf-8").upper()

    def described(self):
        return (
            (BootSector.OEM_ID, self.oem_id),
            (BootSector.SERIAL_NUMBER, self.serial_number),
            (BootSector.TOTAL_SECTORS, self.total_sectors),
            (BootSector.RESERVED_SECTORS, self.reserved_sectors),
            (BootSector.BYTES_PER_SECTOR, self.bytes_per_sector),
            (BootSector.SECTORS_PER_CLUSTER, self.sectors_per_cluster),
            (BootSector.BYTES_PER_CLUSTER, self.bytes_per_cluster),
            (BootSector.STARTING_CLUSTER_MFT, self.starting_cluster_MFT),
            (BootSector.STARTING_CLUSTER_MFTMIRR, self.starting_cluster_MFTMirr),
            (BootSector.BYTES_PER_ENTRY, self.bytes_per_entry)
        )

    def __str__(self):
        s = "\nVolume Information from Boot Sector:\n"
        for name, value in self.described():
            s += f"\t{name}: {value}\n"
        return s