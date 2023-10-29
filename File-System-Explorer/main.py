import time
from contextlib import contextmanager
import string
from ctypes import windll
from typing import List

from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.traceback import install
from rich.prompt import Prompt
from rich.panel import Panel

from NTFS.ntfs import NTFS

# more beautiful traceback (apply globally)
install(show_locals=True, word_wrap=True)

GLOBAL_CONSOLE = Console()

@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * 0.06)

def print_member():
    member = [
        ["Đặng An Nguyên", "21120123"],
        ["Phan Nguyên Phương", "21120123"],
        ["Đỗ Hoàng Long", "21120123"],
        ["Nguyễn Anh Tú", "21120123"],
        ["Lê Nguyễn", "21120123"]
    ]

    table = Table(show_footer=False)
    table_centered = Align.center(table)
    GLOBAL_CONSOLE.clear()

    with Live(table_centered, console=GLOBAL_CONSOLE, screen=False, refresh_per_second=20):
        with beat(10):
            table.add_column(header="Tên thành viên", no_wrap=True)

        with beat(10):
            table.add_column(header="Mã số sinh viên", no_wrap=True)

        with beat(10):
            table.title = "Danh sách các thành viên"

        with beat(10):
            table.title = (
                "[not italic]:vampire:[/] [b green]Danh sách các thành viên [not italic]:vampire:[/]"
            )

        for row in member:
            with beat(10):
                table.add_row(*row)

        with beat(10):
            table.columns[0].header_style = "magenta"

        with beat(10):
            table.columns[1].header_style = "blue"

        with beat(10):
            table.caption = "From FIT HCMUS with love"

        with beat(10):
            table.caption = (
                ":heart: From [b red not dim]FIT HCMUS with love :heart:"
            )


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
    # # print all member
    # print_member()

    # # print title
    # title = Align.center(Panel.fit("Đồ án HĐH: [bold]File System Explorer :smile:", 
    #                                 border_style="yellow", 
    #                                 padding=(0,7)))
    # GLOBAL_CONSOLE.print(title)

    # print and choose volume
    drives = get_drives()
    # GLOBAL_CONSOLE.print("Các volume hiện có: ")
    # for idx, drive in enumerate(drives):
    #     GLOBAL_CONSOLE.print(f"{idx}) {drive}", style="cyan")
    # choice = Prompt.ask("Chọn volume mà bạn muốn :skull:", 
    #                     choices=[str(i) for i in range(len(drives))],
    #                     default="0") 

    choice = Prompt.ask("Chọn volume mà bạn muốn :skull:", 
                        choices=drives,
                        default=None) 

    # check drive
    if NTFS.check_ntfs(choice):
        vol = NTFS(choice)
        GLOBAL_CONSOLE.print(vol.boot_sector_info)