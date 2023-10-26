import string
from ctypes import windll
from typing import List
from icecream import ic

from UI.utils import GLOBAL_CONSOLE
from NTFS.ntfs import NTFS

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

    if NTFS.check_ntfs(drives[3]):
        ntfs = NTFS(drives[3])
        GLOBAL_CONSOLE.print(ntfs.boot_sector)

    else:
        exit()