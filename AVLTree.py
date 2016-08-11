from BST import Bst


class AVL(Bst):
    def _rotation_ll(self, node):
        lc = node._lc
        rc = node._rc
        temp = AVL()
        temp._key = node._key
        temp._value = node._value
        temp._rc = rc
        temp._lc = lc._rc
        temp._update_properties()
        node._key = lc._key
        node._value = lc._value
        node._lc = lc._lc
        node._rc = temp
        node._update_properties()

    def _rotation_rr(self, node):
        lc = node._lc
        rc = node._rc
        temp = AVL()
        temp._key = node._key
        temp._value = node._value
        temp._rc = rc._lc
        temp._lc = lc
        temp._update_properties()
        node._key = rc._key
        node._value = rc._value
        node._rc = rc._rc
        node._lc = temp
        node._update_properties()

    def _rotation_lr(self, node):
        # first step
        lc = node._lc
        node._lc = node._lc._rc
        lc._rc = node._lc._lc
        lc._update_properties()
        node._lc._lc = lc
        node._lc._update_properties()
        node._update_properties()
        # second step
        self._rotation_ll(node)

    def _rotation_rl(self, node):
        # first step
        rc = node._rc
        node._rc = node._rc._lc
        rc._lc = node._rc._rc
        rc._update_properties()
        node._rc._rc = rc
        node._rc._update_properties()
        node._update_properties()
        # second step
        self._rotation_rr(node)

    def __add_number__(self, num, tree=None, key=None):
        if tree is not None:
            root = tree._root
        else:
            root = self._root
        super().__add_number__(num, root, key)
        if not self._is_children_None(root):
            lch = root._lc._height
            rch = root._rc._height
            if lch - rch > 1:
                if root._lc._lc._lc is None or root._lc._lc._lc._value is None:
                    self._rotation_lr(root)
                else:
                    self._rotation_ll(root)
            if rch - lch > 1:
                if root._rc._rc._rc is None or root._rc._rc._rc._value is None:
                    self._rotation_rl(root)
                else:
                    self._rotation_rr(root)

    def _remove_node(self, tree, key):
        if super()._remove_node(tree, key):
            if not self._is_children_None(tree):
                tree._update_properties()
                lch = tree._lc._height
                rch = tree._rc._height
                if lch - rch > 1:
                    if tree._lc._lc._lc is None or tree._lc._lc._lc._value is None:
                        self._rotation_lr(tree)
                    else:
                        self._rotation_ll(tree)
                if rch - lch > 1:
                    if tree._rc._rc._rc is None or tree._rc._rc._rc._value is None:
                        self._rotation_rl(tree)
                    else:
                        self._rotation_rr(tree)
            return True
        return False


bst = Bst()
import random

rand = [81, 72, 80, 7, 2, 70, 34, 50, 30, 44, 64, 57, 55, 71, 88, 100, 12, 51, 34, 1]
# for i in range(20):
#    rand.append(random.randint(0, 100))
# rand=list(range(10))
bst.add_number(rand)
avl = AVL()
avl.add_number(rand)
avl.remove_node("55")
avl.remove_node("44")
a = avl["1"]
print(bst.height, avl.height)
