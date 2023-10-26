import sys
from const import *
from datetime import datetime
from enum import Flag, auto

from icecream import ic

class FileAttribute(Flag):
    READ_ONLY = auto()
    HIDDEN = auto()
    SYSTEM = auto()
    VOLLABLE = auto()
    DIRECTORY = auto()
    ARCHIVE = auto()
    DEVICE = auto()
    NORMAL = auto()
    TEMPORARY = auto()
    SPARSE_FILE = auto()
    REPARSE_POINT = auto()
    COMPRESSED = auto()
    OFFLINE = auto()
    NOT_INDEXED = auto()
    ENCRYPTED = auto()

def to_datetime(timestamp):
  return datetime.fromtimestamp(timestamp - (TIME_OFFSET * 1e7) // 1e7)

class StandardInfo:
    def __init__(self, data, start_offset) -> None:
        self.data = data
        self.start_offset = start_offset

        ic(start_offset)

        signature = int.from_bytes(self.data[start_offset:start_offset+4], byteorder=sys.byteorder)
        if signature != 0x10:
            raise Exception("Not Standard Info Attribute!")
        
    @property
    def offset_to_content(self):
        return int.from_bytes(self.data[self.start_offset+20 : self.start_offset + 20 + WORD], 
                              byteorder= sys.byteorder) 

    @property
    def length(self):
        start_byte = self.start_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + DWORD],
                              byteorder=sys.byteorder)

    @property 
    def start_content_offset(self):
        return self.start_offset + self.offset_to_content
 
    @property
    def created_time(self):
        return to_datetime(int.from_bytes(self.data[self.start_content_offset: self.start_content_offset + 8], byteorder=sys.byteorder))

    @property
    def last_modified_time(self):
        return to_datetime(int.from_bytes(self.data[self.start_content_offset+8: self.start_content_offset + 16], byteorder=sys.byteorder))

    @property 
    def flags(self):
        return FileAttribute(int.from_bytes(self.data[self.start_content_offset + 32: self.start_content_offset+36]))


class FileName:
    def __init__(self, data, start_offset) -> None:
        self.data = data
        self.start_offset = start_offset

        signature = int.from_bytes(self.data[start_offset:start_offset+4], byteorder=sys.byteorder)
        if signature != 0x30:
            raise Exception("Not File Name Attribute!")

    @property
    def length(self):
        start_byte = self.start_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + DWORD],
                              byteorder=sys.byteorder)
    
    @property
    def offset_to_content(self):
        return int.from_bytes(self.data[self.start_offset+20:self.start_offset + 20 + WORD], 
                              byteorder= sys.byteorder) 

    @property 
    def start_content_offset(self):
        return self.start_offset + self.offset_to_content
    
    @property
    def parent_dir_id(self):
        return int.from_bytes(self.data[self.start_content_offset: self.start_content_offset + 6])
    
    @property
    def file_name_length(self):
        return self.data[self.start_content_offset+64]
    
    @property
    def file_name(self):
        return  self.data[self.start_content_offset + 66 :self.start_content_offset + 66 + self.file_name_length * 2].decode('utf-16le')
    
class Data:
    def __init__(self, data, start_offset) -> None:
        self.data = data
        self.start_offset = start_offset
        self.non_resident = bool(self.data[self.start_offset + 8])

    @property
    def signature(self):
        return int.from_bytes(self.data[self.start_offset : self.start_offset + DWORD],
                              byteorder=sys.byteorder)

    @property
    def length(self):
        start_byte = self.start_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + DWORD],
                              byteorder=sys.byteorder)
        
    @property
    def data_content(self):
        """
        Return content if data is resident or else return cluster_info
        """
        if self.non_resident:
            offset = (self.data[self.start_offset + 0x40] & 0xF0) >> 4
            size = self.data[self.start_offset + 0x40] & 0x0F
            self.cluster_size = int.from_bytes(self.data[self.start_offset + 0x41: self.start_offset + 0x41 + size], byteorder='little')
            self.cluster_offset =  int.from_bytes(self.data[self.start_offset + 0x41 + size: self.start_offset + 0x41 + size + offset], byteorder='little')
            return (self.cluster_size, self.cluster_offset)

        else:
            offset = int.from_bytes(self.data[self.start_offset + 0x14:self.start_offset + 0x16], byteorder='little')
            self.content = self.data[self.start_offset + offset:self.start_offset + offset + self.data['size']]
            return self.content

    @property
    def data_size(self):
        if self.non_resident:
            return int.from_bytes(self.data[self.start_offset + 0x30: self.start_offset + 0x38], byteorder='little')
        else:
            return int.from_bytes(self.data[self.start_offset+0x10:self.start_offset+0x14], byteorder='little')