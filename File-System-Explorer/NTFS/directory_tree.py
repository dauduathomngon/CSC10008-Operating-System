from collections import defaultdict

from NTFS.mft_entry import MFTEntry
from icecream import ic

class DirTree:
    def __init__(self, list_entry: list[MFTEntry]) -> None:
        self.root = None
        self.dict_node = defaultdict(MFTEntry)

        #Get all node of the tree
        for entry in list_entry:
            self.dict_node[entry.id] = entry

        #Build the children of nodes
        for node_id in self.dict_node:
            parent_dir_id = self.dict_node[node_id].parent_id
            if parent_dir_id in self.dict_node:
                self.root = self.dict_node[parent_dir_id].childs.append(self.dict_node[node_id])

        #Root's parent is itself
        for node_id in self.dict_node:
            if parent_dir_id == self.dict_node[parent_dir_id].id:
                self.root = self.dict_node[parent_dir_id]
                break

        self.current_node = self.root

    def find_child_entry(self, name:str):
        self.current_node.find_child_entry(name)
    
    def find_parent_entry(self, record: MFTEntry):
        return self.dict_node[record.name_attr.parent_dir_id]
    
    
        


            




    