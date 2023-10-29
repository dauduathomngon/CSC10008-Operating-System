from collections import OrderedDict

from NTFS.attribute import *

from icecream import ic

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
            # FF FF FF FF is end of attributes
            if int.from_bytes(self.data[attrib_offset : attrib_offset + 4], byteorder="little") == 0xFFFFFFFF:
                break

            type = Attribute.get_type(attrib_offset, data)

            # We only care about $FILE_NAME, $STANDARD_INFORMATION and $DATA
            if type not in MFTEntry.ATTRIBUTE_MAP:
                pass

            # We only care about first $DATA attribute, because it contains real data
            if type == 0x80:
                self.attributes[type] = MFTEntry.ATTRIBUTE_MAP[type](attrib_offset, data)
                break

            # Here, we take $STANDARD_INFORMATION and $FILE_NAME attribute
            self.attributes[type] = MFTEntry.ATTRIBUTE_MAP[type](attrib_offset, data)

            attrib_offset += self.attributes[type].length

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
        # flag of entry at offset 0x16 and has length 4
        return int.from_bytes(self.data[0x16 : 0x16 + 4],
                              byteorder="little")

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