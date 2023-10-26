# for more beautiful traceback
from UI.utils import GLOBAL_CONSOLE

from NTFS.boot_sector import BootSector
from NTFS.mft import MFTFile

class NTFS:
    def __init__(self, vol_name: str) -> None:
        self.name = vol_name

        self.boot_sector = BootSector(self.name)

        self.mft_file = MFTFile(self.boot_sector)

    @staticmethod
    def check_ntfs(vol_name: str) -> bool:
        try:
            with open(r'\\.\%s' % vol_name, "rb") as f:
                name = f.read(512)[0x03 : 0x03 + 8].decode()
                if name == "NTFS    ":
                    return True
                else:
                    return False
        except FileNotFoundError:
            GLOBAL_CONSOLE.print_exception(word_wrap=True)
            exit()
        except PermissionError:
            GLOBAL_CONSOLE.print_exception(word_wrap=True)
            exit()
        except Exception:
            GLOBAL_CONSOLE.print_exception(word_wrap=True)
            exit()