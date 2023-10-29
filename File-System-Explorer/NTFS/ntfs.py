from const import LONGLONG
from NTFS.boot_sector import BootSector

class NTFS:
    def __init__(self, vol_name: str) -> None:
        self.name = vol_name

        # use to read data
        self.__f = open(r'\\.\%s' % self.name, "rb")
        self.__f.seek(0)

        # first read boot sector
        # because boot sector took first 512 bytes of disk
        boot_data = self.__f.read(512)
        self.__boot_sector = BootSector(boot_data)

        # then move the pointer after boot sector (after 512 bytes)
        self.__f.seek(512)

    @staticmethod
    def check_ntfs(vol_name) -> bool:
        with open(r'\\.\%s' % vol_name, "rb") as f:
            oem_name = f.read(512)[0x03 : 0x03 + LONGLONG].decode()
            if oem_name == "NTFS    ":
                return True
            else:
                return False

    @property
    def boot_sector_info(self) -> str:
        return str(self.__boot_sector)