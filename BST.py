class Bst(object):
    # properties
    _value = None
    _lc = None
    _rc = None
    _key = None
    _height = 0
    _size = 0

    # constructor
    def __init__(self, nums=None):
        if hasattr(nums, "__iter__"):
            data = nums
        elif nums is not None:
            data = [nums]
        else:
            data = None
        self.__init_tree__(data)

    def __init_tree__(self, data):
        if not data:
            self._root = self
            self._root._value = None
            return
        else:
            self._root = self
            self._root._value = None
            for i in data:
                self.__add_number__(i)

    # properties methods
    @property
    def height(self):
        return self._height

    def _get_height(self, tree):
        if self._is_children_None(tree):
            return 0
        lch = -1
        rch = -1
        if not self._is_empty(tree._lc):
            lch = tree._lc._height
        if not self._is_empty(tree._rc):
            rch = tree._rc._height
        tree._height = max(lch, rch) + 1
        return tree._height

    @property
    def min(self):
        return self._min(self)._value

    def _min(self, tree, callback=None):
        if tree is not None and tree._value is not None:
            if tree._lc is not None and tree._lc._value is not None:
                ret = self._min(tree._lc)
                if callback is not None:
                    callable(tree)
                return ret
            else:
                return tree
        else:
            return None

    @property
    def max(self):
        return self._max(self)._value

    def _max(self, tree, callback=None):
        if tree is not None and tree._value is not None:
            if tree._rc is not None and tree._rc._value is not None:
                ret = self._max(tree._rc)
                if callback is not None:
                    callable(tree)
                return ret
            else:
                return tree
        else:
            raise ValueError("This is an empty Tree, does not have a max.")

    @property
    def size(self):
        return self._size

    def _get_size_(self, tree):
        if self._is_empty(tree):
            return 0
        if self._is_children_None(tree):
            tree._size = 1
            return 1
        lcs = 0
        if not self._is_empty(tree._lc):
            lcs = tree._lc._size
        rcs = 0
        if not self._is_empty(tree._rc):
            rcs = tree._rc._size
        tree._size = lcs + rcs + 1
        return tree._size

    # python intern methods
    def __repr__(self):
        if self._key is None:
            return str(None)
        return self._key

    def __iter__(self):
        return self.order()

    def __getitem__(self, item):
        return self.get_node(item)

    def __setitem__(self, key, value):
        node = self._get_node_(self,key)
        if node is not None:
            node._value = value
        else:
            self.add_node(key, value)

    def __len__(self):
        return self._size

    # utils
    def _is_empty(self, tree):
        return (tree is None) or (tree._value is None)

    def _is_left_children_none(self, tree):
        return (tree is None) or (tree._lc is None or tree._lc._value is None)

    def _is_right_children_none(self, tree):
        return (tree is None) or (tree._rc is None or tree._rc._value is None)

    def _is_children_None(self, tree):
        return (tree is None) or (tree._lc is None or tree._lc._value is None) \
                                 and (tree._rc is None or tree._rc._value is None)

    def _is_all_None(self, nodes):
        for n in nodes:
            if n is not None and n._value is not None:
                return False
        return True

    def _update_properties(self, tree=None):
        if tree is None:
            tree = self
        tree._size = self._get_size_(tree)
        tree._height = self._get_height(tree)

    def __copy_node_(self, src, obj):
        src_dict = src.__dict__
        obj.__dict__ = src_dict

    # internal methods
    def __add_number__(self, num, tree=None, key=None):
        if tree is not None:
            root = tree._root
        else:
            root = self._root
        root._size += 1
        if root._value is None:
            root._value = num
            if key is None:
                key = str(num)
            root._key = key
            root._lc = self.__class__()
            root._rc = self.__class__()
            return
        if self._is_children_None(root):
            root._height += 1
        if num <= root._value:
            self.__add_number__(num, root._lc, key)
        else:
            self.__add_number__(num, root._rc, key)
        root._height = max(root._lc._height, root._rc._height) + 1

    def _in_order(self, tree):
        if tree._value is not None:
            for i in self._in_order(tree._lc):
                yield i
            yield tree
            for i in self._in_order(tree._rc):
                yield i

    def add_number(self, nums):
        if hasattr(nums, "__iter__"):
            for i in nums:
                self.__add_number__(i)
        else:
            self.__add_number__(nums)

    def add_node(self, key, value):
        self.__add_number__(value, key=key)

    def remove_node(self, key):
        self._remove_node(self, key)

    def _remove_node(self, tree, key):
        if self._is_empty(tree):
            return False
        if tree._key == key:
            if self._is_children_None(tree):
                self.__copy_node_(tree.__class__(), tree)
                return True
            if self._is_right_children_none(tree):
                self.__copy_node_(tree._lc, tree)
                return True
            if self._is_left_children_none(tree):
                self.__copy_node_(tree._rc, tree)
                return True
            rc = tree._lc._rc

            def _node_update(node):
                node._size += rc._size
                node._height = max(node._lc._height + rc._height + 1, node._height)

            min_rc = self._min(tree._rc, _node_update)
            min_rc._lc = rc
            min_rc._update_properties()
            tree._lc._rc = tree._rc
            self.__copy_node_(tree._lc, tree)
            tree._update_properties()
            return True
        if self._remove_node(tree._lc, key):
            tree._update_properties()
            return True
        if self._remove_node(tree._rc, key):
            tree._update_properties()
            return True
        return False

    def _get_node_(self, tree, key):
        if self._is_empty(tree):
            return None
        if tree._key == key:
            return tree
        return None or self._get_node_(tree._lc, key) or self._get_node_(tree._rc, key)

    def get_node(self, key):
        node = self._get_node_(self, key)
        if node is None:
            return node
        return node._value

    def order(self):
        for i in self._in_order(self):
            yield i._value

    def level_order(self):
        stack = [self._root]
        current_node = [self._root]
        while current_node:
            i = current_node[0]
            if i._lc._value is not None:
                stack.append(i._lc._value)
                current_node.append(i._lc)
            if i._rc._value is not None:
                stack.append(i._rc._value)
                current_node.append(i._rc)
            current_node.pop(0)
        return stack

    def pprint(self):
        ret = self._print_interval_level([self], 1, self.height)
        return ret

    def _print_interval_level(self, nodes, level, max_level):
        if self._is_all_None(nodes):
            return ""
        ret = ""
        space = "\t"
        floor = max_level - level
        edge_lines = int(2 ** max((floor - 1), 0))
        first_space = int(2 ** floor - 1)
        between_space = int(2 ** (floor + 1) - 1)
        ret += space * first_space
        next_nodes = []
        for node in nodes:
            if node is not None and node._value is not None:
                ret += str(node._value)
                next_nodes.append(node._lc)
                next_nodes.append(node._rc)
            else:
                next_nodes.append(None)
                next_nodes.append(None)
            ret += space * between_space
        ret += "\n"
        return ret + self._print_interval_level(next_nodes, level + 1, max_level)


bst = Bst()
import random

rand = []
for i in range(10):
    rand.append(random.randint(0, 100))
bst.add_node("aa", 50)
bst.add_number(rand)
print(rand)
print("\n")
# print(list(bst))
# print(bst.level_order())
# print(bst.min,bst.max)

bst["ee"] = 101
print(bst.level_order())
print("end")
