import sys
from const import *
from datetime import datetime
from enum import Flag, auto

from icecream import ic

class FileAttribute(Flag):
    # take from: https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants?redirectedfrom=MSDN
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

def to_datetime(timestamp):
  return datetime.fromtimestamp(timestamp - (TIME_OFFSET * 1e7) // 1e7)

class StandardInfoAttrib:
    def __init__(self, data, start_offset) -> None:
        self.data = data
        self.start_offset = start_offset

        signature = int.from_bytes(self.data[start_offset : start_offset + 4],
                                   byteorder=sys.byteorder)
        if signature != 0x10:
            raise Exception("Not Standard Info Attribute!")
        
    @property
    def offset_to_content(self):
        start_byte = self.start_offset + 20
        return int.from_bytes(self.data[start_byte : start_byte + WORD], 
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
        return to_datetime(int.from_bytes(self.data[self.start_content_offset : self.start_content_offset + LONGLONG],
                                          byteorder=sys.byteorder))

    @property
    def last_modified_time(self):
        start_byte = self.start_content_offset + 8
        return to_datetime(int.from_bytes(self.data[start_byte : start_byte + LONGLONG],
                                          byteorder=sys.byteorder))

    @property 
    def file_permissions(self):
        start_byte = self.start_content_offset + 32
        return FileAttribute(int.from_bytes(self.data[start_byte : start_byte + DWORD],
                                            byteorder=sys.byteorder) & 0xFFFF)

class FileNameAttrib:
    def __init__(self, data, start_offset) -> None:
        self.data = data
        self.start_offset = start_offset

        signature = int.from_bytes(self.data[start_offset : start_offset + 4],
                                   byteorder=sys.byteorder)
        if signature != 0x30:
            raise Exception("Not File Name Attribute!")

    @property
    def length(self):
        start_byte = self.start_offset + 4
        return int.from_bytes(self.data[start_byte : start_byte + DWORD],
                              byteorder=sys.byteorder)
    
    @property
    def offset_to_content(self):
        return int.from_bytes(self.data[self.start_offset + 20 : self.start_offset + 20 + WORD], 
                              byteorder= sys.byteorder) 

    @property 
    def start_offset_content(self):
        return self.start_offset + self.offset_to_content
    
    @property
    def parent_dir_id(self):
        return int.from_bytes(self.data[self.start_offset_content : self.start_offset_content + 6])
    
    @property
    def file_name_length(self):
        return self.data[self.start_offset_content + 64]
    
    @property
    def file_name(self):
        return self.data[self.start_offset_content + 66 : self.start_offset_content + 66 + self.file_name_length * 2].decode('utf-16le')
    
class DataAttrib:
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
            # take first 4 bit at start_offset + 0x40
            offset = (self.data[self.start_offset + 0x40] & 0xF0) >> 4
            # take last 4 bit at start_offset + 0x40
            size = self.data[self.start_offset + 0x40] & 0x0F
            self.cluster_size = int.from_bytes(self.data[self.start_offset + 0x41 : self.start_offset + 0x41 + size],
                                               byteorder=sys.byteorder)
            self.cluster_offset =  int.from_bytes(self.data[self.start_offset + 0x41 + size : self.start_offset + 0x41 + size + offset],
                                                  byteorder=sys.byteorder)
            return (self.cluster_size, self.cluster_offset)

        else:
            offset = int.from_bytes(self.data[self.start_offset + 0x14 : self.start_offset + 0x16],
                                    byteorder=sys.byteorder)
            self.content = self.data[self.start_offset + offset:self.start_offset + offset + self.data['size']]
            return self.content

    @property
    def data_size(self):
        if self.non_resident:
            return int.from_bytes(self.data[self.start_offset + 0x30 : self.start_offset + 0x38],
                                  byteorder=sys.byteorder)
        else:
            return int.from_bytes(self.data[self.start_offset + 0x10 : self.start_offset + 0x14],
                                  byteorder=sys.byteorder)

class IndexRootAttrib:
    def __init__(self, data, start_offset) -> None:
        self.data = data
        self.start_offset = start_offset