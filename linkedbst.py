"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from tqdm import tqdm
from random import shuffle, choice
from sys import setrecursionlimit
from time import time,sleep

setrecursionlimit(10**7)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        lst = list()
        def postorder1(node, node_list):
            if node.left is not None:
                postorder1(node.left, node_list)
            node_list.append(node.data)
            if node.right is not None:
                postorder1(node.right, node_list)
        postorder1(self._root, lst)
        return lst

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        # I rewrote find to be iterative so recursion limit won't be exceeded
        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)
        # return recurse(self._root)

        node = self._root
        while node.data != item:
            if item > node.data:
                node = node.right
            else:
                node = node.left
            if node is None:
                return
        return node, node.data

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left == None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right == None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        # P.S. Again, I rewrote the function to be iterative to handle recursion limit
        else:
            node = self._root
            while True:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    node = node.left
                else:
                    if node.right is None:
                        node.right = BSTNode(item)
                        break
                    node = node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            return 1 + max(height1(top.right), height1(top.left))

        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''

        return self.height() < (2 * log(self._size + 1) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

        nodes = self.postorder()
        lower = 0
        upper = len(nodes) - 1
        while nodes[lower] < low:
            lower += 1
        while nodes[upper] > high:
            upper -= 1
        if lower > upper:
            return
        return nodes[lower:upper+1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        nodes = self.postorder()
        self.clear()
        def recursive_add_mid(tree:LinkedBST, lst:list):
            if len(lst) == 0:
                return
            l = len(lst)
            tree.add(lst[l // 2])
            lst.pop(l // 2)
            recursive_add_mid(tree, lst[:l//2])
            recursive_add_mid(tree, lst[l//2:])

        recursive_add_mid(self, nodes) 

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        nodes = self.postorder()
        i = 0
        while nodes[i] < item:
            i += 1
            if i >= len(nodes):
                return
        if nodes[i] != item:
            return nodes[i]
        elif i + 1 < len(nodes):
            return nodes[i + 1]
        return

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        nodes = self.postorder()
        i = len(nodes) - 1
        while nodes[i] > item:
            i -= 1
            if i < 0:
                return
        if nodes[i] != item:
            return nodes[i]
        elif i > 0:
            return nodes[i - 1]
        return

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        ITERATIONS = 10000
        lst = list()
        unbalanced_tree = LinkedBST()
        random_add_tree = LinkedBST()
        balanced_tree = LinkedBST()
        lines = list()

        with open(path, 'r', encoding='utf-8') as src:
            lines = src.readlines()
        progres = 0
        total = len(lines)
        for line in lines:
            if progres % 500 == 0:
                print(f'Progress: {round(progres * 100 / total, 2)}%', end='\r')
            progres += 1
            line = line.strip()
            lst.append(line)
            unbalanced_tree.add(line)
            balanced_tree.add(line)
        print()
        shuffle(lst)
        for line in lst:
            random_add_tree.add(line)
        # print(len(lst), unbalanced_tree._size)
        balanced_tree.rebalance()

        print('Words added successfully!')
        print(f'\nFinding {ITERATIONS} words :')
        print('\n--Built-in list:')
        now = time()
        for i in tqdm(range(ITERATIONS)):
            word = choice(lst)
            lst.index(word)
        print(f'Total time: {round(time() - now, 3)} seconds.')
        print('\n--Unbalanced binary search tree (de facto linked list):')
        now = time()
        for i in tqdm(range(ITERATIONS)):
            word = choice(lst)
            unbalanced_tree.find(word)
        print(f'Total time: {round(time() - now, 3)} seconds.')
        print('\n--Random-add binary search tree (unbalanced bst):')
        now = time()
        for i in tqdm(range(ITERATIONS)):
            word = choice(lst)
            random_add_tree.find(word)
        print(f'Total time: {round(time() - now, 3)} seconds.')
        print('\n--Balanced search tree:')
        now = time()
        for i in tqdm(range(ITERATIONS)):
            word = choice(lst)
            balanced_tree.find(word)
        print(f'Total time: {round(time() - now, 3)} seconds.')

if __name__ == '__main__':
    my_tree = LinkedBST()
    print('Attention: adding words may take some time')
    my_tree.demo_bst('binary_search_tree/words100.txt')
