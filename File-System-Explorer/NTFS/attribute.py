from enum import Flag
from NTFS.boot_sector import BootSector
from utils import to_datetime

from icecream import ic

# ------------------------------------
# Generic Attribute
# ------------------------------------
class Attribute:
    def __init__(self, offset, data) -> None:
        self.data = data
        self.start_offset = offset

    # ------------------------------------
    # Property
    # ------------------------------------
    @property
    def type(self):
        return int.from_bytes(self.data[self.start_offset : self.start_offset + 4],
                              byteorder="little")

    @property
    def length(self):
        return int.from_bytes(self.data[self.start_offset + 4 : self.start_offset + 8],
                              byteorder="little")

    @property
    def non_resident_flag(self):
        return int.from_bytes(self.data[self.start_offset + 8 : self.start_offset + 9],
                              byteorder="little")

    @property
    def attrib_data_offset(self):
        offset_to_data = int.from_bytes(self.data[self.start_offset + 20 : self.start_offset + 22],
                                        byteorder="little")
        return self.start_offset + offset_to_data
                              
    # ------------------------------------
    # Method
    # ------------------------------------
    def is_resident(self) -> bool:
        return not bool(self.non_resident_flag)
    
    @staticmethod
    def get_type(offset, data):
        return int.from_bytes(data[offset : offset + 4],
                              byteorder="little")

    @staticmethod
    def get_length(offset, data):
        return int.from_bytes(data[offset + 4 : offset + 8],
                              byteorder="little")

# ------------------------------------
# $STANDARD_INFORMATION Attribute
# ------------------------------------
class NTFSAttribute(Flag):
    # taken from: https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants?redirectedfrom=MSDN
    READ_ONLY = 0x1
    HIDDEN = 0x2
    SYSTEM = 0x4
    DIRECTORY = 0x10
    ARCHIVE = 0x20
    DEVICE = 0x40
    NORMAL = 0x80
    TEMPORARY = 0x100
    SPARSE_FILE = 0x200
    REPARSE_POINT = 0x400
    COMPRESSED = 0x800
    OFFLINE = 0x1000
    NOT_INDEXED = 0x2000
    ENCRYPTED = 0x4000

class StandardInfoAttrib(Attribute):
    def __init__(self, offset, data) -> None:
        super().__init__(offset, data)

        if self.type != 0x10:
            raise Exception("This is not $STANDARD_INFORMATION attribute")

    # ------------------------------------
    # Property
    # ------------------------------------
    @property
    def created_time(self):
        return to_datetime(int.from_bytes(self.data[self.attrib_data_offset : self.attrib_data_offset + 8],
                                          byteorder="little"))

    @property
    def last_modified_time(self):
        return to_datetime(int.from_bytes(self.data[self.attrib_data_offset + 8 : self.attrib_data_offset + 16],
                                          byteorder="little"))
    
    @property 
    def file_status(self):
        return NTFSAttribute(int.from_bytes(self.data[self.attrib_data_offset + 32 : self.attrib_data_offset + 34],
                                            byteorder="little") & 0xFFFF)

# ------------------------------------
# $FILE_NAME Attribute
# ------------------------------------
class FileNameAttrib(Attribute):
    def __init__(self, offset, data) -> None:
        super().__init__(offset, data)

        if self.type != 0x30:
            raise Exception("This is not $FILE_NAME attribute")

    # ------------------------------------
    # Property
    # ------------------------------------
    @property
    def parent_id(self):
        return int.from_bytes(self.data[self.attrib_data_offset : self.attrib_data_offset + 6],
                              byteorder="little")
    
    @property
    def file_name_length(self):
        return self.data[self.attrib_data_offset + 64]

    @property
    def file_name(self):
        return self.data[self.attrib_data_offset + 66 : self.attrib_data_offset + 66 + self.file_name_length * 2].decode("utf-16le")

# ------------------------------------
# $FILE_NAME Attribute
# ------------------------------------
class DataAttrib(Attribute):
    def __init__(self, offset, data) -> None:
        super().__init__(offset, data)

        if self.type != 0x80:
            raise Exception("This is not $DATA attribute")

        if self.is_resident():
            self.data_len = int.from_bytes(self.data[self.start_offset + 16 : self.start_offset + 20],
                                      byteorder="little")
            self.content_data = self.data[self.attrib_data_offset : self.attrib_data_offset + self.data_len]

        else:
            datarun_offset = self.start_offset + int.from_bytes(self.data[self.start_offset + 32 : self.start_offset + 34],
                                                                byteorder="little")
            size = self.data[datarun_offset]

            # first 4 bits defined how much bytes first cluster of data run has
            first_cluster_bits = (size & 0b1111000) >> 4
            # last 4 bit of datarun_size defined how much bytes cluster count has
            cluster_count_bits = (size & 0b00001111)

            # then we have cluster count and first cluster
            self.cluster_count = int.from_bytes(self.data[datarun_offset + 1 : datarun_offset + 1 + cluster_count_bits],
                                                byteorder="little")

            self.first_cluster = int.from_bytes(self.data[datarun_offset + 1 + cluster_count_bits : datarun_offset + 1 + cluster_count_bits + first_cluster_bits],
                                                byteorder="little")

            # real size of data
            self.real_size = int.from_bytes(self.data[self.start_offset + 48 : self.start_offset + 56],
                                            byteorder="little")