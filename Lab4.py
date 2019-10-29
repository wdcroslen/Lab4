#Lab4
import timeit
start1 = timeit.default_timer()
# Code to implement a B-tree
# Programmed by Olac Fuentes
# Modified by Diego Aguirre on October 9, 2019

class BTreeNode:
    def __init__(self, keys=[], children=[], is_leaf=True, max_num_keys=5):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf
        if max_num_keys < 3:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys = 3
        if max_num_keys % 2 == 0:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys += 1
        self.max_num_keys = max_num_keys

    def is_full(self):
        return len(self.keys) >= self.max_num_keys


class BTree:
    def __init__(self, max_num_keys=5):
        self.max_num_keys = max_num_keys
        self.root = BTreeNode(max_num_keys=max_num_keys)

    def find_child(self, k, node=None):
        # Determines value of c, such that k must be in subtree node.children[c], if k is in the BTree
        if node is None:
            node = self.root

        for i in range(len(node.keys)):
            if k < node.keys[i]:
                return i
        return len(node.keys)

    def insert_internal(self, i, node=None):
        if node is None:
            node = self.root
        # node cannot be Full
        if node.is_leaf:
            self.insert_leaf(i, node)
        else:
            k = self.find_child(i, node)
            if node.children[k].is_full():
                m, l, r = self.split(node.children[k])
                node.keys.insert(k, m)
                node.children[k] = l
                node.children.insert(k + 1, r)
                k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def split(self, node=None):
        if node is None:
            node = self.root
        # print('Splitting')
        # PrintNode(T)
        mid = node.max_num_keys // 2
        if node.is_leaf:
            left_child = BTreeNode(node.keys[:mid], max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], max_num_keys=node.max_num_keys)
        else:
            left_child = BTreeNode(node.keys[:mid], node.children[:mid + 1], node.is_leaf, max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], node.children[mid + 1:], node.is_leaf, max_num_keys=node.max_num_keys)
        return node.keys[mid], left_child, right_child

    def insert_leaf(self, i, node=None):
        if node is None:
            node = self.root

        node.keys.append(i)
        node.keys.sort()

    def insert(self, i, node=None):
        if node is None:
            node = self.root
        if not node.is_full():
            self.insert_internal(i, node)
        else:
            m, l, r = self.split(node)
            node.keys = [m]
            node.children = [l, r]
            node.is_leaf = False
            k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def search(self, k, node=None):
        if node is None:
            node = self.root
        # Returns node where k is, or None if k is not in the tree
        if k in node.keys:
            return node
        if node.is_leaf:
            return None
        return self.search(k, node.children[self.find_child(k, node)])
            
    def printTree(self, node):
        if node is None:
            return
        print(node.keys)
        for i in node.children:
            self.printTree(i)
        return


###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
def print_anagrams_BTree(word,english_words,prefix = ""):
    if len(word) <= 1:
       str = prefix + word
       if english_words.search(prefix + word,english_words.root):
           print(prefix + word)
    else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur
           if cur not in before: # Check if permutations of cur have not been generated.
               print_anagrams_BTree(before + after,english_words, prefix + cur) 

def BTree_readfile(user_input):
    file = open("10Ktest.txt", "r")
    singleLine = file.readline() #reads a single line at a time
    tree = BTree(max_num_keys=user_input)
    for singleLine in file:
        #Inserts each line in BTree
        tree.insert(singleLine.replace("\n",""))
    return tree

def count_anagrams_avl(word,english_words,prefix = ""):
    global count # calls global count to count recursively
    if len(word) <= 1:
       str = prefix + word
       if english_words.avl_search(prefix + word,english_words.root):
           count = count + 1
    else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur
           if cur not in before: # Check if permutations of cur have not been generated.
               count_anagrams_avl(before + after, english_words, prefix + cur) 
    return count

def most_anagrams_avl(english_words): # finds word with most anagrams in the file
    file = open("10Ktest.txt", "r")
    biggest = 0
    word = ""
    global count
    count = 0
    for singleLine in file:
        #Inserts each line in avl
        a = str(singleLine.replace("\n",""))
        q = count_anagrams_avl(a,english_words)
        if  q > biggest:
            word = a
            biggest = q
        global count
        count = 0
    print(word, biggest)
    return 0

def main():
     print("Hello! I will be producing anagrams for you using a list of english words.")
     print("What is the max number of keys?")
     print("Odd number")
     a = int(raw_input())
     if a%2 == 0:
        a = a +1
        print("your new number is:")
     print(a)
     tree = BTree(max_num_keys=a)
     nums = [6, 3, 16, 11, 7, 17, 14, 8, 5, 19, 15, 1, 2, 4, 18, 13, 9, 20, 10, 12, 21]
     print("What word would you like to see anagrams for?")
     q = raw_input()
     print("Anagrams for " + q + ":")
     start = timeit.default_timer()
     tree = BTree_readfile(a)
     print_anagrams_BTree(q,tree)

     stop = timeit.default_timer()
     print('Time: ', stop - start) 
    
main()
