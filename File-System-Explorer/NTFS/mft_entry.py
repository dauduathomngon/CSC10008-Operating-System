import sys
from const import *
from NTFS.attribute import *

from icecream import ic

class MFTEntry:
    def __init__(self, data):
        self.data_attr = data

        # $STANDARD_INFORMATION Attribute
        offset_first_attr = int.from_bytes(self.data_attr[0x14 : 0x14 + WORD], byteorder=sys.byteorder)
        ic(offset_first_attr)
        self.standard_info = StandardInfo(self.data_attr, offset_first_attr)

        # $FILE_NAME Attribute
        filename_offset = self.standard_info.start_offset + self.standard_info.length
        self.name = FileName(self.data_attr, filename_offset)

        # $DATA Attribute
        data_offset = self.name.start_offset + self.name.length
        self.data_attr = Data(self.data_attr, data_offset)

    @property
    def file_id(self):
        return int.from_bytes(self.data_attr[0x2C : 0x2C + DWORD],
                              byteorder=sys.byteorder)

    @property
    def flag(self):
        return self.data_attr.data[0x16]