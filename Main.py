import random

from Tree import *


def main():
    tree = Tree(3, 4)

    liste = list(range(1,10 +1))
    random.shuffle(liste)
    tree.insertKeys(liste)
    print(liste)

    tree.toGraph()

if __name__ == '__main__':
    main()