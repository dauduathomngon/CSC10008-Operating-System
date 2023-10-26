# for more beautiful traceback
from UI.utils import GLOBAL_CONSOLE

LONGLONG = 8
WORD = 2
BYTE = 1

class BootSector:
    # ------------------------
    # Attributes
    # ------------------------
    OEM_NAME = "OEM name"
    BYTES_PER_SECTOR = "Bytes per sector"
    SECTORS_PER_CLUSTER = "Sectors per cluster"
    CLUSTER_SIZE = "Cluster size"
    RESERVED_SECTORS = "Reserved sectors"
    TOTAL_SECTORS = "Total number of sector"
    LCN_MFT = "MFT ($MFT) starting cluster"
    LCN_MFT_MIRR = "MFT Backup ($MFTMirr) starting cluster"
    MFT_ENTRY_SIZE = "MFT entry size"
    SERIAL_NUMBER = "Serial volume number"

    def __init__(self, vol_name: str) -> None:
        # member variable
        self.name = vol_name

        try:
            self.f = open(r'\\.\%s' % self.name, "rb")
            self.f.seek(0)
            self.data = self.f.read(512)
        except FileNotFoundError:
            GLOBAL_CONSOLE.print_exception(word_wrap=True)
            exit()
        except PermissionError:
            GLOBAL_CONSOLE.print_exception(word_wrap=True)
            exit()
        except Exception:
            GLOBAL_CONSOLE.print_exception(word_wrap=True)
            exit()

    @property
    def oem_name(self) -> str:
        # oem_id at offset 0x03 with length LONGLONG (8 byte)
        return self.data[0x03 : 0x03 + LONGLONG].decode()

    @property
    def bytes_per_sector(self) -> int:
        # bytes_per_sector at offset 0x0B with length WORD (2 byte)
        return int.from_bytes(self.data[0x0B : 0x0B + WORD], byteorder="little")

    @property
    def sectors_per_cluster(self) -> int:
        # sectors_per_cluster at offset 0x0D with length BYTE
        return int.from_bytes(self.data[0x0D : 0x0D + BYTE], byteorder="little")

    @property
    def total_sectors(self) -> int:
        # total_sectors at offset 0x28 with length LONGLONG
        return int.from_bytes(self.data[0x28 : 0x28 + LONGLONG], byteorder="little")

    @property
    def cluster_MFT(self) -> int:
        # cluster_MFT at offset 0x30 with length LONGLONG
        return int.from_bytes(self.data[0x30 : 0x30 + LONGLONG], byteorder="little")

    @property
    def cluster_MFF_mir(self) -> int:
        # cluster_MFT_mir at offset 0x38 with length LONGLONG
        return int.from_bytes(self.data[0x38 : 0x38 + LONGLONG], byteorder="little")

    @property
    def MFT_entry_size(self):
        # Clusters Per File Record Segment at offset 0x40 with length DWORD (4 byte)
        # But we only need first byte (called segment)
        # segment can be:
        # - positive: it shows number of clusters per entry.
        # - negative: it shows number of bytes of entry in log2
        # (segment is negative because size of cluster > size of entry)

        segment = int.from_bytes(self.data[0x40 : 0x40 + BYTE], byteorder="little", signed=True)
        if segment > 0:
            return segment * self.cluster_size
        else:
            return 2**abs(segment)

    @property
    def cluster_size(self):
        return self.bytes_per_sector * self.sectors_per_cluster

    @property
    def reserved_sectors(self):
        # reserved_sectors at offset 0x0E with length WORD
        return int.from_bytes(self.data[0x0E : 0x0E + WORD], byteorder="little")

    @property
    def serial_number(self):
        # serial_number at offset 0x48 with length LONGLONG
        return int.from_bytes(self.data[0x48 : 0x48 + LONGLONG], byteorder="little")

    def described(self):
        return ( 
            (BootSector.OEM_NAME, self.oem_name),
            (BootSector.BYTES_PER_SECTOR, self.bytes_per_sector),
            (BootSector.SECTORS_PER_CLUSTER, self.sectors_per_cluster),
            (BootSector.CLUSTER_SIZE, self.cluster_size),
            (BootSector.RESERVED_SECTORS, self.reserved_sectors),
            (BootSector.TOTAL_SECTORS, self.total_sectors),
            (BootSector.LCN_MFT, self.cluster_MFT),
            (BootSector.LCN_MFT_MIRR, self.cluster_MFF_mir),
            (BootSector.MFT_ENTRY_SIZE, self.MFT_entry_size),
            (BootSector.SERIAL_NUMBER, self.serial_number)
        )

    def __str__(self) -> str:
        s = "Volume name: " + self.name[0]
        s += "\nVolume Information:\n"
        for name, value in self.described():
            s += f"\t{name}: {value}\n"
        return s