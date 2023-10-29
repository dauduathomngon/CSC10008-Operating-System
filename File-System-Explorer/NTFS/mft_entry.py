import sys

from const import DWORD, WORD

class MFTEntry:
    def __init__(self, data) -> None:
        self.data = data

        # check if an entry is valid
        if not self.__is_valid():
            raise Exception("This is invalid entry")

    def __is_valid(self) -> bool:
        if self.signature == "FILE":
            return True
        return False

    @property
    def signature(self) -> str:
        # signature of an entry at offset 0 and has length DWORD (4 bytes)
        return self.data[0 : 0 + DWORD].decode("utf-8")

    @property
    def first_attribute_offset(self) -> int:
        # first attribute offset at offset 0x14 and has length WORD
        return int.from_bytes(self.data[0x14 : 0x14 + WORD],
                              byteorder="little")