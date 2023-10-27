from FAT32.attribute import Attribute
from datetime import datetime
from itertools import chain
import sys
class RDET_Entry:
    def __init__(self,data) -> None:
        self.data= data
        self.flag = data[0xB:0xC]
        if self.flag == b'\x0f':
            self.is_subentry = True
        self.is_subentry: bool = False
        self.is_deleted: bool = False
        self.is_empty: bool = False
        self.is_label: bool = False
        self.attr = Attribute(0)
        self.date_created = ""
        self.size = 0
        self.date_created = 0
        self.last_accessed = 0
        self.date_updated = 0
        self.ext = b""
        self.long_name = ""
        
        if not self.is_subentry:
            self.name = self.data[:0x8]
            self.ext = self.data[0x8:0xB]
            if self.data[:1]==b'\xe5':
                self.is_deleted = True
            if self.data[:1]==b'\x00':
                self.is_empty=True;
                self.name=""
                return
            
            
            self.attr = Attribute(int.from_bytes(self.flag,byteorder=sys.byteorder))    
            if Attribute.VOLLABLE in self.attr:
                self.is_label = True
                return

            # I dunno how, but it works?
            self.time_created_raw = int.from_bytes(self.data[0xD:0x10], byteorder=sys.byteorder)
            self.date_created_raw = int.from_bytes(self.data[0x10:0x12], byteorder=sys.byteorder)
            self.last_accessed_raw = int.from_bytes(self.data[0x12:0x14], byteorder=sys.byteorder)

            self.time_updated_raw = int.from_bytes(self.data[0x16:0x18], byteorder=sys.byteorder)
            self.date_updated_raw = int.from_bytes(self.data[0x18:0x1A], byteorder=sys.byteorder)

            h = (self.time_created_raw & 0b111110000000000000000000) >> 19
            m = (self.time_created_raw & 0b000001111110000000000000) >> 13
            s = (self.time_created_raw & 0b000000000001111110000000) >> 7
            ms =(self.time_created_raw & 0b000000000000000001111111)
            year = 1980 + ((self.date_created_raw & 0b1111111000000000) >> 9)
            mon = (self.date_created_raw & 0b0000000111100000) >> 5
            day = self.date_created_raw & 0b0000000000011111

            self.date_created = datetime(year, mon, day, h, m, s, ms)

            year = 1980 + ((self.last_accessed_raw & 0b1111111000000000) >> 9)
            mon = (self.last_accessed_raw & 0b0000000111100000) >> 5
            day = self.last_accessed_raw & 0b0000000000011111

            self.last_accessed = datetime(year, mon, day)

            h = (self.time_updated_raw & 0b1111100000000000) >> 11
            m = (self.time_updated_raw & 0b0000011111100000) >> 5
            s = (self.time_updated_raw & 0b0000000000011111) * 2
            year = 1980 + ((self.date_updated_raw & 0b1111111000000000) >> 9)
            mon = (self.date_updated_raw & 0b0000000111100000) >> 5
            day = self.date_updated_raw & 0b0000000000011111
            
            self.date_updated = datetime(year, mon, day, h, m, s)
            self.start_cluster = int.from_bytes(self.data[0x14:0x16][::-1] + self.data[0x1A:0x1C][::-1], byteorder='big')
            self.size = int.from_bytes(self.data[0x1C:0x20], byteorder='little')

        else:
            self.index = self.data[0]
            self.name = b""
            for i in chain(range(0x1, 0xB), range(0xE, 0x1A), range(0x1C, 0x20)):
                self.name += int.to_bytes(self.data[i], 1, byteorder='little')
                if self.name.endswith(b"\xff\xff"):
                    self.name = self.name[:-2]
                    break
            self.name = self.name.decode('utf-16le').strip('\x00')
            

    def is_active_entry(self) -> bool:
        return not (self.is_empty or self.is_subentry or self.is_deleted or self.is_label or Attribute.SYSTEM in self.attr)
  
    def is_directory(self) -> bool:
        return Attribute.DIRECTORY in self.attr

    def is_archive(self) -> bool:
        return Attribute.ARCHIVE in self.attr