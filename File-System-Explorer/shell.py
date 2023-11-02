import os
from cmd import Cmd
from datetime import datetime

from NTFS.ntfs import NTFS
from FAT32.fat32 import FAT32
from NTFS.attribute import NTFSAttribute
from FAT32.attribute import FAT32Attribute
from utils import (
    print_greeting,
    GLOBAL_CONSOLE,
    get_default_windows_app,
    parse_path
)

class Shell(Cmd):
    def __init__(self, vol: (NTFS | FAT32)) -> None:
        super(Shell, self).__init__()
        self.vol = vol
        self.__update_prompt()

    def __update_prompt(self): # DONE
        time_now = datetime.now()
        Shell.prompt = f"({time_now.hour}:{time_now.minute}) Cậu đang ở [{self.vol.get_cwd()}] > "

    def do_clear(self, arg): # DONE
        os.system("cls")

    def do_exit(self, arg): # DONE
        GLOBAL_CONSOLE.print("[bold italic]Cảm ơn cậu vì đã sử dụng chương trình này[/bold italic] 🥺")
        del self.vol
        return True

    def do_help(self, arg): # DONE
        self.do_clear(arg)
        print_greeting(again=True)

    def do_pwd(self, arg): # DONE (NTFS, FAT32)
        GLOBAL_CONSOLE.print(self.vol.get_cwd())

    def do_ls(self, arg): # DONE (NTFS, FAT32)
        try:
            list_entry = self.vol.get_dir_info(arg)

            GLOBAL_CONSOLE.print(f"[green]{'Mode':<10}  {'Last Modified Time':<20}  {'Length':>12}  {'Name'}")
            GLOBAL_CONSOLE.print(f"[green]{'────':<10}  {'──────────────────':<20}  {'──────':>12}  {'────'}")

            for entry in list_entry:
                flag = entry["Flags"]
                permissions = list("------")
                if str(self.vol) == "NTFS":
                    if flag & NTFSAttribute.DIRECTORY:
                        permissions[0] = "d"
                    if flag & NTFSAttribute.ARCHIVE:
                        permissions[1] = "a"
                    if flag & NTFSAttribute.READ_ONLY:
                        permissions[2] = "r"
                    if flag & NTFSAttribute.HIDDEN:
                        permissions[3] = "h"
                    if flag & NTFSAttribute.SYSTEM:
                        permissions[4] = "s"
                else:
                    permissions = permissions[0:-1]
                    if flag & FAT32Attribute.DIRECTORY:
                        permissions[0] = "d"
                    if flag & FAT32Attribute.ARCHIVE:
                        permissions[1] = "a"
                    if flag & FAT32Attribute.READ_ONLY:
                        permissions[2] = "r"
                    if flag & FAT32Attribute.HIDDEN:
                        permissions[3] = "h"
                    if flag & FAT32Attribute.SYSTEM:
                        permissions[4] = "s"
                        permissions[4] = "s"

                permissions = "".join(permissions)

                if not permissions.startswith("d"):
                    GLOBAL_CONSOLE.print(f"[cyan]{permissions:<10}[/cyan] {str(entry['Last Modified']):<20} {entry['Size'] if entry['Size'] else '':>14} {entry['Name']}")
                else:
                    GLOBAL_CONSOLE.print(f"{permissions:<10} {str(entry['Last Modified']):<20} {entry['Size'] if entry['Size'] else '':>14} {entry['Name']}")

        except Exception as e:
            if "Not directory" == str(e):
                GLOBAL_CONSOLE.print(f"[red]{arg}[/red] không là một thư mục.")
            else:
                GLOBAL_CONSOLE.print(f"Không tim thấy path [red]{arg}[/red]")

    def do_cd(self, arg): # Done (NTFS, FAT32)
        try:
            self.vol.change_dir(arg)
            self.__update_prompt()
        except Exception as e:
            if "Path is required" == str(e):
                GLOBAL_CONSOLE.print("Thiếu path muốn đi đến, syntax đúng là [red]cd <path>[/red].")
            elif "Not directory" == str(e):
                GLOBAL_CONSOLE.print(f"[red]{arg}[/red] không là một thư mục.")
            else:
                GLOBAL_CONSOLE.print(f"Không tim thấy path [red]{arg}[/red]")

    def do_vol_info(self, arg): # Done (NTFS, FAT32)
        GLOBAL_CONSOLE.print(self.vol.boot_sector_info)

    def do_cat(self, arg): # Done (NTFS, FAT32)
        if arg == "":
            GLOBAL_CONSOLE.print("Không có path nào ở input")
            return
        try:
            GLOBAL_CONSOLE.print(self.vol.get_text_file(arg))
        except Exception as e:
            if "is not a file" in str(e):
                GLOBAL_CONSOLE.print(f"[red]{arg}[/red] là một folder")
            else:
                ext = "." + parse_path(arg)[-1].split(".")[-1]
                GLOBAL_CONSOLE.print(f"[red]{arg}[/red] không là .txt file")
                GLOBAL_CONSOLE.print(f"Nhưng cậu có thể dùng [green]{get_default_windows_app(ext)}[/green] để mở")
                GLOBAL_CONSOLE.print("Hoặc app nào khác tuỳ cậu 😎")

    def do_type(self, arg):
        GLOBAL_CONSOLE.print(self.vol)

    SPACE = '    '
    BRANCH = '│'
    MIDDLE = '├── '
    LAST = '└── '

    def __print_tree(self, entry, tab, is_last=False):
        if (str(self.vol) == "NTFS" and
            entry["Flags"] & NTFSAttribute.DIRECTORY) or (
                str(self.vol) == "FAT32" and
                entry["Flags"] & FAT32Attribute.DIRECTORY
            ):
            GLOBAL_CONSOLE.print(tab + (self.LAST if is_last else self.MIDDLE) + f'📂 [cyan]{entry["Name"]}\\')
        else:
            GLOBAL_CONSOLE.print(tab + (self.LAST if is_last else self.MIDDLE) + f'📃 {entry["Name"]}')

        # base case when an entry is a file
        if (str(self.vol) == "NTFS" and
            entry["Flags"] & NTFSAttribute.ARCHIVE) or (
                str(self.vol) == "FAT32" and 
                entry["Flags"] & FAT32Attribute.ARCHIVE
            ):
                return
            
        tab = self.BRANCH + tab[1:] + self.SPACE

        # get all entry of a folder
        self.vol.change_dir(entry["Name"])
        entry_list = self.vol.get_dir_info("")

        size = len(entry_list)
        for i in range(0, size):
            # FAT32 error handle
            if entry_list[i]["Name"] in (".", ".."):
                continue
            self.__print_tree(entry_list[i], tab, i == size - 1)

        # get all entry of a folder
        self.vol.change_dir("..")

    def do_tree(self, arg):
        entry_list = self.vol.get_dir_info(arg)

        GLOBAL_CONSOLE.print(f'📂 [cyan]{self.vol.get_cwd()}') 

        size = len(entry_list)
        for i in range(0, size):
            # FAT32 error handle
            if entry_list[i]["Name"] in (".", ".."):
                continue
            self.__print_tree(entry_list[i], "", i == size - 1)