class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val


class Tree:
    def __init__(self):
        self.root = None
        self.listOfNode = list()

    def get_root(self):
        return self.root

    def add(self, val):
        if not self.root:
            self.root = Node(val)
            self.listOfNode.append(self.root)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if val < node.v:
            if node.l:
                self._add(val, node.l)
            else:
                node.l = Node(val)
                self.listOfNode.append(node.l)
        else:
            if node.r:
                self._add(val, node.r)
            else:
                node.r = Node(val)
                self.listOfNode.append(node.r)

    def find(self, val):
        if self.root:
            return self._find(val, self.root)

    def _find(self, val, node):
        if val == node.v:
            return node
        elif val < node.v and node.l:
            return self._find(val, node.l)
        elif val > node.v and node.r:
            return self._find(val, node.r)

    def delete_tree(self):
        # garbage collector will do this for us.
        if self.root:
            self.root = None

    def __iter__(self):
        if self.root:
            yield from self._view_tree(self.root)

    def __str__(self):
        return str(self.v)

    def _view_tree(self, node):
        if  node is None:
            return
        if node.l:
            yield from self._view_tree(node.l)
        
        yield node.v

        if node.r:
            yield from self._view_tree(node.r)

    def view_nodes_from_small(self):
        from_small_list_nums = []
        [from_small_list_nums.append(n.v) for n in self.listOfNode]
        return print(sorted(from_small_list_nums))


#     3
# 0     4
#   2      8
tree = Tree()
tree.add(3)
tree.add(4)
tree.add(0)
tree.add(8)
tree.add(2)
for i in tree:
    print((i))
# tree.view_nodes_from_small()
# print(tree.find(3).v)
# print(tree.find(10))
# tree.delete_tree()
# tree.view_tree()
