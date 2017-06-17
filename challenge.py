from collections import defaultdict
from Queue import Queue

input5 = '''7 aaaaaaaaabbeeeeeeedddddggmmlloooonnssssrrrruvvyyy'''

prefixes = defaultdict(list)
with open('words.txt') as file:
    for l in file:
        l = l.strip()
        for i in xrange(len(l)):
            prefixes[(l[:i], len(l))] += [l]

def wordsquare(input):
    print input
    input = input.split()
    size = int(input[0])
    queue = Queue()
    queue.put([[], input[1]])
    while queue.qsize():
        curr = queue.get()
        if len(curr[0]) == size:
            print '\n'.join(curr[0]), '\n'
            continue
        prefix = '' if not curr[0] else ''.join(zip(*curr[0])[len(curr[0])])
        for i in prefixes[(prefix, size)]:
            if any((''.join(j), size) not in prefixes for j in zip(*(curr[0] + [i]))[len(curr[0]) + 1:]):
                continue
            contains = True
            for j in i:
                if i.count(j) > curr[1].count(j):
                    contains = False
                    break
            if not contains:
                continue
            temp = curr[1]
            for j in i:
                temp = temp.replace(j, '', 1)
            queue.put([curr[0] + [i], temp])

wordsquare(input5)
