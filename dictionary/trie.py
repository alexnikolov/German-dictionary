import math


class TrieNode:
    def __init__(self, value, final):
        self.value = value
        self.final = final
        self.children = {}

    def add_child(self, letter):
        if not letter in self.children:
            new_node = TrieNode(letter, False)
            self.children[letter] = new_node

    def remove_child(self, letter):
        if letter in self.children:
            del self.children[letter]

    def get_child(self, letter):
        if letter in self.children:
            return self.children[letter]

    def make_final(self):
        self.final = True

    def destroy_final(self):
        self.final = False


class Trie:
    def __init__(self):
        self.root = TrieNode(' ', False)

    def add_word(self, word):
        current_node = self.root

        for letter in word:
            current_node.add_child(letter)

            current_node = current_node.get_child(letter)

        current_node.make_final()

    def search_for_word(self, word):
        current_node = self.root
        times_iterated = 0

        for letter in word:
            next_node = current_node.get_child(letter)

            if next_node:
                current_node = next_node
                times_iterated += 1
            else:
                break

        if (current_node.value is word[-1] and times_iterated is len(word) and
               current_node.final):
            return True
        return False

    def delete_word(self, word):
        if self.search_for_word(word):
            current_node = self.root
            last_split = self.root
            last_split_letter = ' '

            for letter in word:
                if len(current_node.children.keys()) > 1 or current_node.final:
                    last_split = current_node
                    last_split_letter = letter

                next_node = current_node.get_child(letter)

                if next_node:
                    current_node = next_node

            # current_node == last_node
            print(current_node.children)
            if current_node.children == {}:
                del last_split.children[last_split_letter]
            else:
                current_node.destroy_final()


t = Trie()
t.add_word("abc")
t.add_word("xyz")
t.add_word("qwerty")
print(t.search_for_word("abc"))
print(t.search_for_word("sbz"))
print(t.search_for_word("qwerti"))
print(t.search_for_word("qwerty"))
print(t.search_for_word("xyzz"))
print('\n')

t = Trie()
t.add_word("dog")
t.add_word("doge")
t.add_word("dodge")

test_word = "dog"

print(t.search_for_word(test_word))
t.delete_word(test_word)
print(t.search_for_word(test_word))
print(t.search_for_word("dog"))