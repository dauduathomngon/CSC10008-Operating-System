from typing import IO
from cmd import Cmd

class Shell(Cmd):
    # don't care about this, just code suggestion
    def __init__(self, vol) -> None:
        super(Shell, self).__init__()
        self.vol = vol