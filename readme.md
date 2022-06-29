# Binary Search Trees Comparison

A lab dedicated to comparing unbalanced and balanced tree data structures.
It was interesting to do a task simillar to my [graduate project](https://github.com/rwmutel/Red_Black_Trees_Demo) from the lyceum. I wrote that project, related to red-black tree data structure back in 2020.

## Dataset

There are 235000 words in alphabet order in words.txt file (also, I've generated a smaller file words100.txt with 2350 words to test the code)

## The Experiment

There are four data structures to compare:

- built-in list
- a tree with the words added in alphabetical order (meaning it's literally a linked list)
- another tree, where the words were added in random order
- the last tree, which was balanced after inserting the words

After the words are added, the user sees a beautiful vizualization of searching process, made with tqdm library

![Experiment demo #1](/experiment_in_progress.jpg)
![Experiment demo #2](/experiment_done.jpg)

## Summary

A nice little project to learn how to code and use binary search tree in real life conditions and how efficient it is.
