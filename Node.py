class Node:
    def __init__(self, parent=None, leaf=True):
        self.parent = parent
        self.leaf = leaf
        self.keys = []  # Current number of keys
        self.childrens = []

    def toString(self):
        """ affiche tous les attributs du noeud ainsi que celui de tout ses noeuds enfants : parent, leaf, keys, et childrens sous ce format :

        parent node : (noeud)

        keys of parent node : (tableau de clés du noeud parent)

        leaf: (booléen : True | False)

        keys: (tableau de clés du noeud affiché)

        """
        if self.parent is None:
            print("parent node :", self.parent)
        else:
            print("keys of parent node :", self.parent.keys)
        print("leaf:", self.leaf)
        print("keys:", self.keys)
        childs = []
        for child in self.childrens:
            childs.append(child.keys)
        print("key of childrens :", childs)

    def keyIndex(self, key):
        """ Retourne un index permettant de pouvoir placer la clé au bon endroit dans le tableau keys

        :param key: (int) clé à trier
        :return: (int) index du tableau où mettre la clé dans le tableau keys
        """
        i = 0
        for elem in self.keys:
            if key > elem:
                i += 1
            else:
                break
        return i

    def insert(self, key, tree):
        """
        Fonction d'insertion permettant d'ajouter la clé dans un noeud ou dans son noeud enfant selon la structure du noeud avant insertion

        :param key: (int) clé qu'on veut insérer dans le noeud
        :param tree: (Tree) arbre
        :return: False si la taille des clés du noeud (concerné par l'ajout de la valeur) est inférieure au nombre d'enfants maximal de l'arbre en paramètre, True sinon.
        """
        i = self.keyIndex(key)
        if not self.leaf:
            print("on va au fils contenant les clés", self.childrens[i].keys)
            bool = self.childrens[i].insert(key, tree)
            if bool:
                tree.split(self.childrens[i])
                return len(self.keys) > tree.nbChildMax
            else:
                return False
        else:
            print("ajout de", key, "au noeud contenant déjà les clés", self.keys)
            self.keys.insert(i, key)
            return len(self.keys) > tree.nbChildMax

    def exists_key(self, searching_key):
        """
        permet de rechercher la clé fournie en paramètre.

        :param searching_key: (int) clé que l'on cherche
        :return: True si la clé existe dans le noeud (ou dans ses enfants), False sinon.
        """
        i = 0
        while i < len(self.keys) and searching_key > self.keys[i]:
            i += 1

        if self.leaf:
            return i < len(self.keys) and searching_key == self.keys[i]

        else:
            if i == len(self.keys):
                self.childrens[-1].exists_key(searching_key)

            elif self.keys[i] == searching_key:
                return True

            return self.childrens[i].exists_key(searching_key)