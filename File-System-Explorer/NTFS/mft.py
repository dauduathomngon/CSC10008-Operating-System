import sys

from NTFS.boot_sector import BootSector
# for more beautiful traceback
from UI.utils import GLOBAL_CONSOLE

LONGLONG = 8
WORD = 2
BYTE = 1

class MFTFile:
    """
    Read $MFT File in MFT Table for all general information
    """
    def __init__(self, boot_sector: BootSector) -> None:
        self.boot_sector = boot_sector

        self.offset = self.boot_sector.cluster_MFT * self.boot_sector.cluster_size
        self.size = self.boot_sector.MFT_entry_size

        self.boot_sector.f.seek(self.offset)
        self.data = self.boot_sector.f.read(self.size)

    @property
    def info_attr_offset(self):
        # offset of first attribute ($STANDARD_INFORMATION) start at 0x14 offset and length WORD (2 byte)
        return int.from_bytes(self.data[0x14 : 0x14 + WORD], 
                              byteorder=sys.byteorder)

    @property
    def info_attr_len(self):
        # length of ($STANDARD_INFORMATION) start at byte 4 (after offset) and length DWORD (4 byte)
        start_byte = self.info_attr_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + (WORD * 2)], 
                              byteorder=sys.byteorder)

    @property
    def name_attr_offset(self):
        # offset of attribute $FILE_NAME (right after $STANDARD_INFORMATION) so it = info_len + info_offset 
        return self.info_attr_len + self.info_attr_offset

    @property
    def name_attr_len(self):
        # length of ($FILE_NAME) start at byte 4 (after offset) and length DWORD (4 byte)
        start_byte = self.name_attr_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + (WORD * 2)], 
                              byteorder=sys.byteorder)

    @property
    def data_attr_offset(self):
        # offset of attribute $DATA (right after $FILE_NAME)
        return self.name_attr_offset + self.name_attr_len
    
    @property
    def data_attr_len(self):
        # length of ($DATA) start at byte 4 (after offset) and length DWORD (4 byte)
        start_byte = self.data_attr_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + (WORD * 2)], 
                              byteorder=sys.byteorder)

    @property
    def num_sector_mft(self):
        # number sector of entire MFT table
        # First VCN (virtual cluster number) is 0 and Number Last VCN at byte 24 (after offset) and has length LONGLONG
        # So number of vcn = last_vcn + first_vcn + 1 (because start at 0)
        # Then sector = no_vcn * sectors_per_cluster
        start_byte = self.data_attr_offset + 24
        n_vcn = int.from_bytes(self.data[start_byte : start_byte + LONGLONG], byteorder=sys.byteorder) + 1
        return n_vcn * self.boot_sector.sectors_per_cluster