import os
from rich.traceback import install
from rich.prompt import Prompt

from utils import (
    get_drives,
    GLOBAL_CONSOLE,
    print_greeting,
    print_member,
    print_label)
from NTFS.ntfs import NTFS
from FAT32.fat32 import FAT32
from shell import Shell

# more beautiful traceback (apply globally)
install(show_locals=True, word_wrap=True)

if __name__=="__main__":
    print_member()
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

    os.system("cls")
    
    # run shell
    try:
        if NTFS.check_ntfs(choice_vol):
            print_greeting()
            shell = Shell(NTFS(choice_vol))
        else:
            print_greeting()
            shell = Shell(FAT32(choice_vol))
        shell.cmdloop()
    except PermissionError:
        GLOBAL_CONSOLE.print(f"Không thể truy cập được volume [bold red]{choice_vol}[/bold red] cần mở dưới [bold]quyền admin[/bold].")