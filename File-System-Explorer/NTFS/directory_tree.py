from collections import defaultdict
from typing import List

from NTFS.mft_entry import MFTEntry

# ------------------------------------
# Directory Tree
# ------------------------------------
class DirTree:
    def __init__(self, list_entry: list[MFTEntry]) -> None:
        self.root : MFTEntry = None
        self.current_node : MFTEntry = None

        self.dict_node = defaultdict(MFTEntry)

        # Get all node of the tree
        for entry in list_entry:
            self.dict_node[entry.id] = entry

        # Build the children of nodes
        for node_id in self.dict_node:
            parent_dir_id = self.dict_node[node_id].parent_id
            if parent_dir_id in self.dict_node:
                self.dict_node[parent_dir_id].children.append(self.dict_node[node_id]) 

        #Root's parent is itself
        for id, node in self.dict_node.items():
            if id == node.parent_id:
                self.root = self.dict_node[id]

        self.current_node = self.root

    # ------------------------------------
    # Method
    # ------------------------------------
    def find_child_entry(self, name):
        self.current_node.find_child_entry(name)

    def find_parent_entry(self, entry):
        return self.dict_node[entry.parent_id]

    def get_active_children(self):
        return self.current_node.get_active_children()