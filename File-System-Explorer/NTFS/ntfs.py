from NTFS.boot_sector import BootSector
from NTFS.mft import MFTFile
# for more beautiful traceback
from UI.utils import GLOBAL_CONSOLE

from icecream import ic

class BTree:
    def __init__(self) -> None:
        pass

class NTFS:
    def __init__(self, vol_name: str) -> None:
        self.name = vol_name
        self.boot_sector = BootSector(self.name)
        self.mft_file = MFTFile(self.boot_sector)

        sector_per_entry = int(self.boot_sector.MFT_entry_size / self.boot_sector.bytes_per_sector)

        for _ in range(sector_per_entry, self.mft_file.num_sector_mft, sector_per_entry):
            ic(self.boot_sector.f.read(self.boot_sector.MFT_entry_size)[:10])

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