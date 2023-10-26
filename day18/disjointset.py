from typing import Optional, Any, Union

class Node:

    def __init__(self, obj: Any, parent: Optional['Node']=None, size: int=1, rank: int=0):
        self.obj = obj
        self.parent = parent
        self.size = size
        self.rank = rank

    def is_root(self):
        return self.parent is None

    def __hash__(self):
        return hash(self.obj)

    def __eq__(self, other: 'Node'):
        return hash(self) == hash(other)


class DisjointSet():

    def __init__(self, use_size: bool = True, use_rank: bool = False):
        self.nodes = {}
        if use_size == use_rank:
            raise ValueError("Please use only one of rank, size to order the disjoint sets.")
        self.use_size = use_size
        self.use_rank = use_rank

        self.union = self.union_rank
        if self.use_size:
            self.union = self.union_size
            

    def contains(self, obj: Any) -> bool:
        return obj in self.nodes.keys()

    def make_set(self, obj: Any) -> None:
        if not self.contains(obj):
            self.nodes[obj] = Node(obj)

    def find(self, obj: Any, return_node: bool=False) -> Union[Any, Node]:
        if not self.contains(obj):
            raise ValueError("Can't find root of an element that is not in a set!")
        root = self.nodes[obj]
        while self.nodes[root].parent is not None:
            root = self.nodes[root].parent

        while self.nodes[obj].parent != None:
            parent = self.nodes[obj].parent
            self.nodes[obj].parent = root
            obj = parent

        if return_node:
            return root
        else:
            return root.obj

    def union_size(self, x: Any, y: Any) -> None:
        if not self.contains(x):
            self.make_set(x)
        if not self.contains(y):
            self.make_set(y)

        x = self.find(x, return_node=True)
        y = self.find(y, return_node=True)

        if x != y:
            if x.size < y.size:
                temp = x
                x = y
                y = temp
            y.parent = x
            x.size = x.size + y.size

    def union_rank(self, x: Any, y: Any) -> None:
        x = self.find(x, return_node=True)
        y = self.find(y, return_node=True)

        if x != y:
            if x.rank < y.rank:
                temp = x
                x = y
                y = temp
            y.parent = x
            if x.rank == y.rank:
                x.rank = x.rank+1
            
