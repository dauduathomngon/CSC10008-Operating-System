import sys
from const import *
from NTFS.attribute import *

from icecream import ic

class MFTEntry:
    def __init__(self, data):
        self.data = data

        # $STANDARD_INFORMATION Attribute
        offset_first_attr = int.from_bytes(self.data[0x14 : 0x14 + WORD], byteorder=sys.byteorder)
        self.standard_info = StandardInfoAttrib(self.data, offset_first_attr)

        # ic(self.standard_info.file_permissions)

        # $FILE_NAME Attribute
        filename_offset = self.standard_info.start_offset + self.standard_info.length
        self.name_attr = FileNameAttrib(self.data, filename_offset)

        # ic(self.name_attr.file_name)

        # directory specification
        self.is_dir = (self.flag == 3)

        # ic(self.is_dir)

        # get an offset for $DATA or $INDEX_ROOT
        data_offset = self.name_attr.start_offset + self.name_attr.length

        # $DATA Attribute (for file)
        if not self.is_dir:
            self.data_attr = DataAttrib(self.data, data_offset)
        # $INDEX_ROOT Attribute (for directory)
        else:
            # you need to go through $OBJECT_ID attribute in order to go to $INDEX_ROOT
            object_id_len = int.from_bytes(self.data[data_offset + 4 : data_offset + 4 + DWORD],
                                           byteorder=sys.byteorder)
            index_offset = data_offset + object_id_len
            self.index_attr = IndexRootAttrib(self.data, index_offset)

    @property
    def file_id(self):
        # entry id at 0x2C and has length DWORD
        return int.from_bytes(self.data_attr[0x2C : 0x2C + DWORD],
                              byteorder=sys.byteorder)

    @property
    def flag(self):
        # entry flag at 0x16 and has length one byte
        return self.data[0x16]