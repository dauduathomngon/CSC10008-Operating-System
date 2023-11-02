import sys

class FAT:
    def __init__(self, data) -> None:
        self.elements=[]
        self.data = data
        for i in range(0, len(data),4):
            self.elements.append(int.from_bytes(self.data[i:i+4],byteorder=sys.byteorder))
    
    def get_chain(self, index:int)->list[int]:
        index_list = []
        while True:
            index_list.append(index)
            index = self.elements[index]
            if index == 0x0FFFFFFF or index == 0x0FFFFFF7:
                break
        return index_list 