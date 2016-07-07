import unittest

from german_dictionary.adjective import Adjective


class AdjectiveTest(unittest.TestCase):
    def test_word_hash(self):
        test_adj = Adjective({'Entry': 'xyz', 'Comparative': 'a',
                              'Superlative': 'b',
                              'Meaning': 'c', 'Examples': 'd'})
        self.assertEqual(test_adj.word_hash['Entry'], 'xyz')
        self.assertEqual(test_adj.word_hash['Comparative'], 'a')
        self.assertEqual(test_adj.word_hash['Superlative'], 'b')
        self.assertEqual(test_adj.word_hash['Meaning'], 'c')
        self.assertEqual(test_adj.word_hash['Examples'], 'd')

    def test_to_str(self):
        test_adj = Adjective({'Entry': 'xyz', 'Comparative': 'a',
                              'Superlative': 'b',
                              'Meaning': 'c', 'Examples': 'd'})
        self.assertEqual(str(test_adj),
                         ("Entry: xyz\nComparative: a\nSuperlative: b\n"
                          "Meaning: c\nExamples: d"))

if __name__ == '__main__':
    unittest.main()
