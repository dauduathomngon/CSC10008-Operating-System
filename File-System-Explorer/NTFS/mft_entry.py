from collections import OrderedDict
from typing import List

from NTFS.attribute import *

# ------------------------------------
# MFT Entry
# ------------------------------------
class MFTEntry:
    ATTRIBUTE_MAP = {
        0x10: StandardInfoAttrib,
        0x30: FileNameAttrib,
        0x80: DataAttrib
    }

    def __init__(self, data) -> None:
        self.data = data

        # check if an entry is valid
        if not self.__is_valid():
            raise Exception("This is invalid entry")

        # create attribute dictionary with key is attribute type
        self.attributes = OrderedDict()

        attrib_offset = self.offset_to_first_attr
        while (True):
            type = Attribute.get_type(attrib_offset, data)

            # FF FF FF FF is end of attributes
            if type == 0xffffffff:
                break

            length = Attribute.get_length(attrib_offset, data)

            # We only care about $FILE_NAME, $STANDARD_INFORMATION and $DATA
            if type in MFTEntry.ATTRIBUTE_MAP:
                # We only care about first $DATA attribute, because it contains real data
                if type == 0x80:
                    self.attributes[type] = MFTEntry.ATTRIBUTE_MAP[type](attrib_offset, data)
                    break

                # Here, we take $STANDARD_INFORMATION and $FILE_NAME attribute
                self.attributes[type] = MFTEntry.ATTRIBUTE_MAP[type](attrib_offset, data)

            # increment attrib_offset
            attrib_offset += length

        # store all children of this entry
        self.children: List[MFTEntry] = []

    # ------------------------------------
    # Property
    # ------------------------------------
    @property
    def signature(self) -> str:
        # signature of an entry at offset 0 and has length 4
        return self.data[0 : 0 + 4].decode("utf-8")

    @property
    def offset_to_first_attr(self) -> int:
        # first attribute offset at offset 0x14 and has length 2
        return int.from_bytes(self.data[0x14 : 0x14 + 2],
                              byteorder="little")

    @property
    def id(self) -> int:
        # ID of entry at offset 0x2C and has length 4
        return int.from_bytes(self.data[0x2C : 0x2C + 4],
                              byteorder="little")

    @property
    def flag(self) -> int:
        # flag of entry at offset 0x16
        return int.from_bytes(self.data[0x16 : 0x16 + 2],
                              byteorder="little")

    @property
    def parent_id(self) -> int:
        if 0x30 not in self.attributes:
            raise Exception("There is no $FILE_NAME attribute")
        return self.attributes[0x30].parent_id

    @property
    def name(self) -> str:
        if 0x30 not in self.attributes:
            raise Exception("There is no $FILE_NAME attribute")
        return self.attributes[0x30].file_name

    # ------------------------------------
    # Method
    # ------------------------------------
    def __is_valid(self) -> bool:
        if self.signature == "FILE":
            return True
        return False

    def is_directory(self) -> bool:
        return (self.flag == 3)

    def is_file(self) -> bool:
        return (self.flag == 1)

    def is_active(self) -> bool:
        if 0x10 not in self.attributes:
            raise Exception("There is no $STANDARD_INFORMATION attribute")
        
        if FileAttribute.SYSTEM in self.attributes[0x10].file_status or FileAttribute.HIDDEN in self.attributes[0x10].file_status:
            return False
        
        return True

    # see if this entry has children or not
    def is_end(self) -> bool:
        return not len(self.children)

    # return all children in active status of this entry
    def get_active_children(self):
        active_children = []
        for child in self.children:
            if child.is_active():
                active_children.append(child)
        return active_children

    # find child entry in all children of this entry
    def find_child_entry(self, name):
        for entry in self.children:
            if entry.name == name:
                return entry
        return None