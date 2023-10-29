from NTFS.boot_sector import BootSector
from NTFS.mft_entry import MFTEntry

from icecream import ic

# ------------------------------------
# NTFS
# ------------------------------------
class NTFS:
    def __init__(self, vol_name: str) -> None:
        self.name = vol_name

        # use to read data
        self.__f = open(r'\\.\%s' % self.name, "rb")
        self.__f.seek(0)

        # first read boot sector
        # boot sector took first 512 bytes of disk
        data = self.__f.read(512)
        self.__boot_sector = BootSector(data)

        # move the pointer to the offset of $MFT entry
        mft_offset = self.__boot_sector.starting_cluster_MFT * self.__boot_sector.bytes_per_cluster
        self.__f.seek(mft_offset)

        # and then read $MFT entry
        data = self.__f.read(self.__boot_sector.bytes_per_entry)
        self.__mft_entry = MFTEntry(data)

        # find number sector of entire MFT table
        # First VCN (virtual cluster number) is 0 and Number Last VCN at byte 24 (after $STANDARD_INFORMTION offset) 
        # and has length LONGLONG
        # So number of vcn = last_vcn + first_vcn + 1 (because start at 0)
        # Then sector = no_vcn * sectors_per_clusterr
        start_byte = self.__mft_entry.attributes[0x80].start_offset + 24
        no_vcn = int.from_bytes(data[start_byte : start_byte + 8],
                                byteorder="little") + 1
        no_sector = no_vcn * self.__boot_sector.sectors_per_cluster

        # finally read all remaining entries to a list
        self.entry_list = []

        sector_per_entry = int(self.__boot_sector.bytes_per_entry / self.__boot_sector.bytes_per_sector)
        entry_count = 2

        for _ in range(sector_per_entry, no_sector, sector_per_entry):
            data = self.__f.read(self.__boot_sector.bytes_per_entry)
            try:
                # we wnat to skip entry from 13 -> 16
                if entry_count >= 13 and entry_count <= 16:
                        entry_count += 1
                        continue
                entry = MFTEntry(data)
                self.entry_list.append(entry)
                entry_count += 1
            except:
                pass

    # ------------------------------------
    # Property
    # ------------------------------------
    @property
    def boot_sector_info(self) -> str:
        return f"Volume name: {self.name[0]}" + str(self.__boot_sector)

    # ------------------------------------
    # Method
    # ------------------------------------
    @staticmethod
    def check_ntfs(vol_name) -> bool:
        with open(r'\\.\%s' % vol_name, "rb") as f:
            oem_name = f.read(512)[0x03 : 0x03 + 8].decode()
            if oem_name == "NTFS    ":
                return True
            else:
                return False
