import unittest

from german_dictionary.trie import TrieNode, Trie
from german_dictionary.noun import Noun


class TrieTest(unittest.TestCase):
    def test_add_single_word(self):
        trie = Trie()
        test_noun = Noun({'Entry': 'Hund'})
        self.assertEqual(trie.search_for_word('Hund'), None)
        trie.add_word(test_noun)
        self.assertEqual(trie.search_for_word('Hund'), test_noun)
        self.assertEqual(trie.search_for_word('Hun'), None)
        self.assertEqual(trie.search_for_word('Hu'), None)
        self.assertEqual(trie.search_for_word('H'), None)

    def test_add_word_with_no_common_first_letters(self):
        trie = Trie()
        first_noun = Noun({'Entry': 'Hund'})
        second_noun = Noun({'Entry': 'Katze'})
        trie.add_word(first_noun)
        trie.add_word(second_noun)
        self.assertEqual(trie.search_for_word('Hund'), first_noun)
        self.assertEqual(trie.search_for_word('Katze'), second_noun)

    def test_add_word_with_common_first_letters(self):
        trie = Trie()
        first_noun = Noun({'Entry': 'Hund'})
        second_noun = Noun({'Entry': 'Hundert'})
        trie.add_word(first_noun)
        trie.add_word(second_noun)
        self.assertEqual(trie.search_for_word('Hund'), first_noun)
        self.assertEqual(trie.search_for_word('Hundert'), second_noun)

    def test_delete_single_word(self):
        trie = Trie()
        test_noun = Noun({'Entry': 'Hund'})
        trie.add_word(test_noun)
        trie.delete_word('Hund')
        self.assertEqual(trie.search_for_word('Hund'), None)

    def test_delete_word_with_no_common_first_letters(self):
        trie = Trie()
        first_noun = Noun({'Entry': 'Hund'})
        second_noun = Noun({'Entry': 'Katze'})
        trie.add_word(first_noun)
        trie.add_word(second_noun)
        trie.delete_word('Hund')
        self.assertEqual(trie.search_for_word('Hund'), None)
        self.assertEqual(trie.search_for_word('Katze'), second_noun)

    def test_delete_word_that_is_substring_of_another(self):
        trie = Trie()
        first_noun = Noun({'Entry': 'Hund'})
        second_noun = Noun({'Entry': 'Hundert'})
        trie.add_word(first_noun)
        trie.add_word(second_noun)
        trie.delete_word('Hund')
        self.assertEqual(trie.search_for_word('Hund'), None)
        self.assertEqual(trie.search_for_word('Hunde'), None)
        self.assertEqual(trie.search_for_word('Hundert'), second_noun)

    def test_delete_word_that_contains_another_as_substring(self):
        trie = Trie()
        first_noun = Noun({'Entry': 'Hund'})
        second_noun = Noun({'Entry': 'Hundert'})
        trie.add_word(first_noun)
        trie.add_word(second_noun)
        trie.delete_word('Hundert')
        self.assertEqual(trie.search_for_word('Hund'), first_noun)
        self.assertEqual(trie.search_for_word('Hundert'), None)
        self.assertEqual(trie.search_for_word('Hunde'), None)

    def test_delete_word_that_has_common_first_letters(self):
        trie = Trie()
        first_noun = Noun({'Entry': 'Baum'})
        second_noun = Noun({'Entry': 'Bart'})
        trie.add_word(first_noun)
        trie.add_word(second_noun)
        trie.delete_word('Bart')
        self.assertEqual(trie.search_for_word('Baum'), first_noun)
        self.assertEqual(trie.search_for_word('Bart'), None)
        self.assertEqual(trie.search_for_word('Ba'), None)


if __name__ == '__main__':
    unittest.main()
