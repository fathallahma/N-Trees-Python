from Node import *
import networkx as nx
import matplotlib.pyplot as plt

class Tree:
    def __init__(self, L, U):
        self.nbChildMin = L - 1
        self.nbChildMax = U - 1
        self.root = Node()
        self.nodes = []

    def toStringAllNodes(self,node):
        """
        affiche tout les attributs du noeud choisi ainsi que celui de tout ses noeuds enfants en utilisant la méthode toString() de Node de manière récursive

        :param node: noeud dont on veut afficher les attributs (dont ceux de ses enfants)
        """
        node.toString()
        for child in node.childrens:
            print("--------------------------------------------------------")
            self.toStringAllNodes(child)

    def print_tree(self, node, l=0):
        """
        affiche toute la structure de l'arbre sous le format :

        Level [hauteur du noeud] : [taille du tableau de clés du noeud] : [tableau de clés du noeud]

        Un noeud de hauteur 0 sera la racine et la valeur s'incrémentera de 1 selon la profondeur du noeud.

        :param node: (Node) noeud à partir du quel on veut afficher les caractéristiques de l'arbre
        :param l: (int) hauteur du noeud
        """
        print("Level ", l, " ", len(node.keys), end=":")
        for i in node.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(node.childrens) > 0:
            for i in node.childrens:
                self.print_tree(i, l)

    def insertKeys(self,keys):
        """
        Ajoute les clés à l'emplacement convenu de l'arbre B

        :param keys: (list) clés à ajouter à l'arbre
        """
        for key in keys:
            self.insert(key)
            self.print_tree(self.root)
            print("-------------------------------------------------")

    def insert(self, key):
        """
        Ajoute la clé à l'emplacement convenu de l'arbre B

        :param key: (int) clé à ajouter à l'arbre
        """
        bool = self.root.insert(key, self)
        if bool:
            self.split(self.root)

    def split(self, node):
        """
        Traite un noeud qui a un nombre de clés supérieurs à l'attribut nbChildMax en le divisant et en créant 1 ou 2 noeuds selon la situation (racine -> 2 sinon 1)

        :param node: (Node) Noeud concerncé par le traitement de l'arbre
        """
        print("Traitement du noeud contenant une valeur en trop:", node.keys)
        length = len(node.keys)

        if length % 2 == 0:
            valueToMove = node.keys[length // 2 - 1]
        else:
            valueToMove = node.keys[length // 2]
        node.keys.remove(valueToMove)

        length = len(node.keys)
        if node.parent is not None:
            newNode = Node(node.parent, node.leaf)
            newNode.keys = node.keys[length // 2:] #partie droite
            node.keys = node.keys[:length // 2] #partie gauche

            newNode.childrens = node.childrens[len(node.childrens) // 2:]
            for child in newNode.childrens:
                child.parent = newNode

            node.childrens = node.childrens[:len(node.childrens) // 2]

            i = node.parent.keyIndex(valueToMove)
            node.parent.keys.insert(i, valueToMove)

            i = 0
            for child in node.parent.childrens:
                if child.keys[-1] < newNode.keys[-1]:
                    i += 1
            node.parent.childrens.insert(i, newNode)

            if len(node.parent.keys) > self.nbChildMax:
                self.split(node.parent)
        else:
            nLeft = Node(node, node.leaf)
            nRight = Node(node, node.leaf)

            if node.leaf:
                node.leaf = False

            nLeft.keys = node.keys[:length // 2]
            nRight.keys = node.keys[length // 2:]
            nLeft.childrens = node.childrens[:len(node.childrens) // 2]
            nRight.childrens = node.childrens[len(node.childrens) // 2:]
            for child in node.childrens[:len(node.childrens) // 2]:
                child.parent = nLeft

            for child in node.childrens[len(node.childrens) // 2:]:
                child.parent = nRight

            node.childrens = [nLeft, nRight]
            node.keys.clear()
            node.keys.append(valueToMove)

    def exists_key(self,key):
        # Je ne peux pas faire de doc en raison d'un bug inconnu de Python sur cette méthode...
        # (l'ajout des 6 quotes ne fonctionne pas : elle provoque une erreur dans les lignes du dessous)

        # permet de rechercher la clé fournie en paramètre à partir du noeud racine de l'arbre
        # :param key: (int) clé que l'on cherche dans l'arbre
        # :return: True si la clé existe dans l'arbre, False sinon.

       return self.root.exists_key(key)

    def initGraph(self, G, node):
        """
        Permet d'initialiser le graphe networkx en créant les noeuds et arêtes du graphe, grâce aux noeuds de l'arbre.

        :param G: (nx.Graph) Graphe à initialiser
        :param node: (Node) noeud à partir du quel on veut initialiser le graphe
        """

        keys = str(node.keys)
        for elem in node.childrens:
            keys2 = str(elem.keys)
            G.add_edge(keys, keys2)
            self.initGraph(G,elem)


    def toGraph(self):
        """
        Permet d'afficher le graphe grâce à networkx et matplotlib
        """
        G = nx.Graph()
        self.initGraph(G, self.root)
        pos = nx.spring_layout(G, k=0.1, iterations=100)
        nx.draw(G, with_labels=True, pos=pos)
        plt.show()
