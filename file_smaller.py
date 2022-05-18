with open('binary_search_tree/words.txt') as src:
    with open('binary_search_tree/words10.txt', 'w') as output:
        i = 0
        for line in src.readlines():
            if i % 90 == 0:
                output.write(line)
                i = 0
            i += 1
