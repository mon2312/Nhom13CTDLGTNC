import json
import os

class Node:
    def __init__(self, key, meaning):
        self.key = key
        self.meaning = meaning
        self.left = None
        self.right = None
        self.height = 1

class AVLDictionary:
    def __init__(self, filename = os.path.join(os.path.dirname(__file__), "dictionary.json")):
        self.root = None
        self.filename = filename
        self.load_from_file()

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        return y

    def insert(self, node, key, meaning):
        if not node:
            return Node(key, meaning)
        elif key < node.key:
            node.left = self.insert(node.left, key, meaning)
        elif key > node.key:
            node.right = self.insert(node.right, key, meaning)
        else:
            node.meaning = meaning
            return node

        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, node, key):
        if not node:
            return node
        elif key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.meaning = temp.meaning
            node.right = self.delete(node.right, temp.key)

        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.meaning
        elif key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def in_order_traversal(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.in_order_traversal(node.left, result)
            result.append((node.key, node.meaning))
            self.in_order_traversal(node.right, result)
        return result

    def add_word(self, key, meaning):
        key = key.lower()
        self.root = self.insert(self.root, key, meaning)
        self.save_to_file()

    def delete_word(self, key):
        key = key.lower()
        self.root = self.delete(self.root, key)
        self.save_to_file()

    def find_meaning(self, key):
        key = key.lower()
        meaning = self.search(self.root, key)
        return meaning

    def get_all_words(self):
        return dict(self.in_order_traversal(self.root))

    def save_to_file(self):
        words = self.get_all_words()
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for word, meaning in data.items():
                    self.root = self.insert(self.root, word.lower(), meaning)
