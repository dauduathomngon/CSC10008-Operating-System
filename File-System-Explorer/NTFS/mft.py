import sys

from UI.utils import GLOBAL_CONSOLE
from NTFS.boot_sector import BootSector

LONGLONG = 8
WORD = 2
BYTE = 1

class MFTFile:
    def __init__(self, boot_sector: BootSector) -> None:
        self.offset = boot_sector.cluster_MFT * boot_sector.cluster_size
        self.size = boot_sector.MFT_entry_size

        boot_sector.f.seek(self.offset)
        self.data = boot_sector.f.read(self.size)

    @property
    def info_offset(self):
        # offset of first attribute ($STANDARD_INFORMATION) start at 0x14 offset and length WORD (2 byte)
        return int.from_bytes(self.data[0x14 : 0x14 + WORD], 
                              byteorder=sys.byteorder)

    @property
    def info_len(self):
        # length of ($STANDARD_INFORMATION) start at byte 4 (after offset) and length DWORD (4 byte)
        start_byte = self.info_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + (WORD * 2)], 
                              byteorder=sys.byteorder)

    @property
    def name_offset(self):
        # offset of attribute $FILE_NAME (right after $STANDARD_INFORMATION) so it = info_len + info_offset 
        return self.info_len + self.info_offset