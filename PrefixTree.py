from __future__ import division
from __future__ import print_function


class Node:
    """Nodurile dint Trie"""

    def __init__(self):
        self.children = {}  # dictionar cu copii
        self.isWord = False  # daca prefixul este sfarsitul unui cuvant

    def __str__(self):
        s = ''
        for k in self.children.keys():
            s += k
        return 'isWord:' + str(self.isWord) + '; children:' + s


class Trie:
    """arbore de prefixe / trie"""

    def __init__(self):
        self.root = Node()

    def add_word(self, word):
        """adaugam cuvant in trie"""
        node = self.root
        for i in range(len(word)):
            c = word[i]
            if c not in node.children:  # daca nu exista deja in arbore
                node.children[c] = Node()
            node = node.children[c]
            if i+1 == len(word):
                node.isWord = True

    def add_words(self, words):
        for w in words:
            self.add_word(w)

    def get_node(self, text):
        """nodul pentru un anumit text"""
        node = self.root
        for c in text:
            if c in node.children:
                node = node.children[c]
            else:
                return None
        return node

    def is_word(self, text):
        node = self.get_node(text)
        if node:
            return node.isWord
        return False

    def get_next_chars(self, text):
        """toate caracterele copii"""
        chars = []
        node = self.get_node(text)
        if node:
            for k in node.children.keys():
                chars.append(k)
        return chars

    def get_next_words(self, text):
        """toate cuvintele care au prefixul text"""
        words = []
        node = self.get_node(text)
        if node:  # inmplementam BFS cu coada hardcodata
            nodes = [node]
            prefixes = [str(text)]
            while len(nodes) > 0:
                # adaugam toti copii in lista
                for k, v in nodes[0].children.items():  # cheie si valoare
                    nodes.append(v)
                    prefixes.append(prefixes[0] + k)

                # este textul current cuvant?
                if nodes[0].isWord:
                    words.append(prefixes[0])

                # trecem mai departe - pop
                del nodes[0]
                del prefixes[0]
        return words

    def dump(self):
        nodes = [self.root]
        # BFS pentru stergere
        while len(nodes) > 0:
            for v in nodes[0].children.values():
                nodes.append(v)
            # afiseaza
            print(nodes[0])
            del nodes[0]


# testare
# t = Trie()
# t.add_words(['for', 'int', 'if', 'while'])
# print(t.get_next_chars('i'))
# print(t.get_next_words('i'))
# t.dump()
# #
