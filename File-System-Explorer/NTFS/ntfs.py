import sys
from icecream import ic
from typing import List

from NTFS.boot_sector import BootSector
from NTFS.mft_entry import MFTEntry
from NTFS.directory_tree import DirTree
from const import *

class NTFS:
    def __init__(self, vol_name: str) -> None:
        self.name = vol_name

        # boot sector
        self.boot_sector = BootSector(self.name)

        # first $MFT file
        mft_offset = self.boot_sector.cluster_MFT * self.boot_sector.cluster_size
        self.boot_sector.f.seek(mft_offset)
        data = self.boot_sector.f.read(self.boot_sector.MFT_entry_size)
        self.mft_file = MFTEntry(data)

        # find number sector of entire MFT table
        # First VCN (virtual cluster number) is 0 and Number Last VCN at byte 24 (after $STANDARD_INFORMTION offset) 
        # and has length LONGLONG
        # So number of vcn = last_vcn + first_vcn + 1 (because start at 0)
        # Then sector = no_vcn * sectors_per_clusterr
        start_byte = self.mft_file.data_attr.start_offset + 24
        n_vcn = int.from_bytes(data[start_byte : start_byte + LONGLONG], byteorder=sys.byteorder) + 1
        n_sector = n_vcn * self.boot_sector.sectors_per_cluster

        # entry list
        self.entry_list: List[MFTEntry] = []

        # add all remaining entry to entry list
        sector_per_entry = int(self.boot_sector.MFT_entry_size / self.boot_sector.bytes_per_sector)
        entry_count = 2

        for _ in range(sector_per_entry, n_sector, sector_per_entry):
            data = self.boot_sector.f.read(self.boot_sector.MFT_entry_size)

            if data[:4] == b"FILE":
                # Because entry 13->16 reserved for $Extend extension so we skip it
                if entry_count >= 13 and entry_count <= 16:
                    entry_count += 1
                    continue

                entry = MFTEntry(data)
                # we only need entry with flag 1 (file) and 3 (folder) because all of this entry are in use
                if entry.flag == 0 or entry.flag == 2:
                    del entry
                else:
                    self.entry_list.append(entry)

                entry_count += 1

        # create a directory tree
        self.dir_tree = DirTree(self.entry_list)

    @staticmethod
    def check_ntfs(vol_name: str) -> bool:
        with open(r'\\.\%s' % vol_name, "rb") as f:
            oem_name = f.read(512)[0x03 : 0x03 + LONGLONG].decode()
            if oem_name == "NTFS    ":
                return True
            else:
                return False
            
    
    