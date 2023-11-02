from ctypes import windll
import os
from datetime import datetime
import shlex
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

def get_default_windows_app(ext):
    """
    Ref: https://stackoverflow.com/a/73815712
    """
    try:  # UserChoice\ProgId lookup initial
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{}\UserChoice'.format(ext)) as key:
            progid = winreg.QueryValueEx(key, 'ProgId')[0]
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\{}\shell\open\command'.format(progid)) as key:
            path = winreg.QueryValueEx(key, '')[0]
    except:  # UserChoice\ProgId not found
        try:
            class_root = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, ext)
            if not class_root:  # No reference from ext
                class_root = ext  # Try direct lookup from ext
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(class_root)) as key:
                path = winreg.QueryValueEx(key, '')[0]
        except:  # Ext not found
            path = None
    # Path clean up, if any
    if path:  # Path found
        path = os.path.expandvars(path)  # Expand env vars, e.g. %SystemRoot% for ext .txt
        path = shlex.split(path, posix=False)[0]  # posix False for Windows operation
        path = path.strip('"')  # Strip quotes
    # Return
    return path

def get_drives():
        """
        # Ref: https://stackoverflow.com/a/827398
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

def print_greeting(again=False):
    if not again:
        GLOBAL_CONSOLE.print("-------------------------------------------------------------------------------------------------------------------------")
        GLOBAL_CONSOLE.print("[bold italic green]Hi[/bold italic green] :dragon: \nTớ là rồng, tớ sẽ hướng dẫn cậu cách dùng chương trình này")
    else:
        GLOBAL_CONSOLE.print("-------------------------------------------------------------------------------------------------------------------------")
        GLOBAL_CONSOLE.print("[bold italic green]Hi[/bold italic green] :dragon: \nTớ đã trở lại rồi đây")

    GLOBAL_CONSOLE.print("- Lệnh [bold red]clear[/bold red] sẽ clear toàn bộ màn hình.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]exit[/bold red] sẽ thoát chương trình.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]type[/bold red] để in loại của volume hiện tại.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]ls <path>[/bold red] sẽ liệt kê những file và folder có trong path.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]pwd[/bold red] sẽ in ra vị trí hiện tại.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]cd <path>[/bold red] sẽ thay đổi vị trí hiện tại thành path.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]vol_info[/bold red] sẽ đưa ra thông tin về volume đang chọn.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]cat <file_path>[/bold red] sẽ in ra nội dung của file_path, nếu không là .txt thì sẽ gợi ý những app để mở file tương ứng.")
    GLOBAL_CONSOLE.print("- Lệnh [bold red]tree <path>[/bold red] sẽ các thư mục con và file của path dưới dạng cây.")
    GLOBAL_CONSOLE.print("Đến đây là hết rồi, tạm biệt cậu :cry:.")
    GLOBAL_CONSOLE.print("Nhưng cậu có thể dùng lệnh [bold red]help[/bold red] để gọi tớ trợ giúp cậu.")
    GLOBAL_CONSOLE.print("-------------------------------------------------------------------------------------------------------------------------")

    if not again:
        print(r"""
      \                   / \  //\
       \    |\___/|      /   \//  \\
            /0  0  \__  /    //  | \ \
           /     /  \/_/    //   |  \  \
           @_^_@'/   \/_   //    |   \   \
           //_^_/     \/_ //     |    \    \
        ( //) |        \///      |     \     \
      ( / /) _|_ /   )  //       |      \     _\
    ( // /) '/,_ _ _/  ( ; -.    |    _ _\.-~        .-~~~^-.
  (( / / )) ,-{        _      `-.|.-~-.           .~         `.
 (( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \
 (( /// ))      `.   {            }                   /      \  \
  (( / ))     .----~-.\        \-'                 .~         \  `. \^-.
             ///.----..>        \             _ -~             `.  ^-`  ^-_
               ///-._ _ _ _ _ _ _}^ - - - - ~                     ~-- ,.-~
                                                                  /.-~          
              """)
    else: 
        print(r"""
      \                   / \  //\
       \    |\___/|      /   \//  \\
            /^  ^  \__  /    //  | \ \
           /     /  \/_/    //   |  \  \
           @_^_@'/   \/_   //    |   \   \
           //_^_/     \/_ //     |    \    \
        ( //) |        \///      |     \     \
      ( / /) _|_ /   )  //       |      \     _\
    ( // /) '/,_ _ _/  ( ; -.    |    _ _\.-~        .-~~~^-.
  (( / / )) ,-{        _      `-.|.-~-.           .~         `.
 (( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \
 (( /// ))      `.   {            }                   /      \  \
  (( / ))     .----~-.\        \-'                 .~         \  `. \^-.
             ///.----..>        \             _ -~             `.  ^-`  ^-_
               ///-._ _ _ _ _ _ _}^ - - - - ~                     ~-- ,.-~
                                                                  /.-~          
    """)