"""
File: bst_probe.py

A tester program for binary search trees.
"""

from linkedbst import LinkedBST
import random

def main():

    tree = LinkedBST()
    tree.add("D")
    tree.add("B")
    tree.add("A")
    tree.add("C")
    tree.add("F")
    tree.add("E")
    tree.add("G")
    tree.add('R')
    tree.add('Q')
    # tree.add('S')
    print(tree)
    print(tree.height())
    # tree.rebalance()
    print(tree.range_find('C', 'G'))
    print(tree.is_balanced())
    print(tree.find('A'))


    
if __name__ == "__main__":
    main()



