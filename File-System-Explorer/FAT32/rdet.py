from rdet_entry import RDET_Entry
class RDET:
    def __init__(self,data) -> None:
        self.data=data
        self.entries:list[RDET_Entry]=[]
        long_name = ""
        for i in range(0, len(self.data), 32):
            self.entries.append(RDET_Entry(self.data[i: i + 32]))
            if self.entries[-1].is_empty or self.entries[-1].is_deleted:
                long_name = ""
                continue
            if self.entries[-1].is_subentry:
                long_name = self.entries[-1].name + long_name
                continue

            if long_name != "":
                self.entries[-1].long_name = long_name
            else:
                extend = self.entries[-1].ext.strip().decode()
                if extend == "":
                    self.entries[-1].long_name = self.entries[-1].name.strip().decode()
                else:
                    self.entries[-1].long_name = self.entries[-1].name.strip().decode() + "." + extend
            long_name = ""

    def get_active_entries(self) -> list[RDET_Entry]:
        entry_list = []
        for i in range(len(self.entries)):
            if self.entries[i].is_active_entry():
                entry_list.append(self.entries[i])
        return entry_list

    def find_entry(self, name) -> RDET_Entry:
        for i in range(len(self.entries)):
            if self.entries[i].is_active_entry() and self.entries[i].long_name.lower() == name.lower():
                return self.entries[i]
        return None