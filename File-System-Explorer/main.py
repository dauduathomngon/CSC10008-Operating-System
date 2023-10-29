from rich.traceback import install
from rich.prompt import Prompt

from NTFS.ntfs import NTFS
from utils import (get_drives, GLOBAL_CONSOLE, print_member, print_label)

# more beautiful traceback (apply globally)
install(show_locals=True, word_wrap=True)

if __name__=="__main__":
    # # print all member
    print_member()

    # # print title
    print_label()

    # print and choose volume
    drives = get_drives()

    GLOBAL_CONSOLE.print("Các volume hiện có: ")

    for idx, drive in enumerate(drives):
        GLOBAL_CONSOLE.print(f"{idx}) {drive}", style="cyan")

    choice = Prompt.ask("Chọn volume mà bạn muốn :skull:", 
                        choices=[str(i) for i in range(len(drives))],
                        default="0") 

    # check drive
    choice_vol = drives[int(choice)]
    if NTFS.check_ntfs(choice_vol):
        vol = NTFS(choice_vol)
        GLOBAL_CONSOLE.print(vol.boot_sector_info)
        GLOBAL_CONSOLE.print(vol.get_file_content("F:\PDF\Windows-NT-File-System-Internals.pdf"))