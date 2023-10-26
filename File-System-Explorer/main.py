import string
from ctypes import windll
from typing import List
from icecream import ic

from NTFS.ntfs import NTFS

# more beautiful traceback (apply globally)
from rich.traceback import install
install(show_locals=True, word_wrap=True)

# more beautiful printing
from rich.console import Console
console = Console()

def get_drives() -> List[str]:
        """
        Ref: https://stackoverflow.com/a/827398

        Returns:
            List[str] : list of volume in computer
        """
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter + ":")
            bitmask >>= 1
        return drives

if __name__=="__main__":
    drives = get_drives()

    if NTFS.check_ntfs(drives[2]):
        ntfs = NTFS(drives[2])
        console.print(ntfs.boot_sector)
    else:
        exit()