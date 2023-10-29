from ctypes import windll
import os
from datetime import datetime
from shlex import shlex
import string
import winreg
import time
from contextlib import contextmanager

from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table

def parse_path(path: str):
    return path.split(os.sep)

# http://sunshine2k.blogspot.com/2014/08/where-does-116444736000000000-come-from.html
TIME_OFFSET = 11644473600

def to_datetime(timestamp):
  return datetime.fromtimestamp((timestamp - TIME_OFFSET * 1e7) // 1e7)

def get_default_windows_app(suffix):
    if suffix == ".jpg":
        suffix = ".png"
    # https://stackoverflow.com/questions/48051864/how-to-get-the-default-application-mapped-to-a-file-extention-in-windows-using-p
    class_root = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, suffix)
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'{}\shell\\open\\command'.format(class_root)) as key:
        command = winreg.QueryValueEx(key, '')[0]
        return shlex.split(command)[0]

def get_drives():
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

GLOBAL_CONSOLE = Console()

@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * 0.04)

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

def print_label():
    title = Align.center(Panel.fit("Đồ án HĐH: [bold green]File System Explorer :smile:", 
                                    border_style="yellow", 
                                    padding=(0,7)))
    GLOBAL_CONSOLE.print(title)