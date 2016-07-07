import unittest

from german_dictionary.verb import Verb


class VerbTest(unittest.TestCase):
    def test_word_hash(self):
        test_verb = Verb({'Entry': 'xyz', 'Used_case': 'a',
                          'Preposition': 'b', 'Separable': 'c',
                          'Forms': 'd', 'Examples': 'e',
                          'Transitive': 'e', 'Meaning': 'm'})
        self.assertEqual(test_verb.word_hash['Entry'], 'xyz')
        self.assertEqual(test_verb.word_hash['Used_case'], 'a')
        self.assertEqual(test_verb.word_hash['Preposition'], 'b')
        self.assertEqual(test_verb.word_hash['Separable'], 'c')
        self.assertEqual(test_verb.word_hash['Forms'], 'd')
        self.assertEqual(test_verb.word_hash['Examples'], 'e')
        self.assertEqual(test_verb.word_hash['Transitive'], 'e')
        self.assertEqual(test_verb.word_hash['Meaning'], 'm')

    def test_to_str(self):
        test_verb = Verb({'Entry': 'xyz', 'Used_case': 'a',
                          'Preposition': 'b', 'Separable': 'c',
                          'Forms': 'd', 'Examples': 'e',
                          'Transitive': 'e', 'Meaning': 'm'})
        self.assertEqual(str(test_verb),
                         (("Entry: xyz\nCase: a\nPreposition: b\nSeparable: c\n"
                           "Forms: d\nTransitive: e\nMeaning: m\nExamples: e")))

if __name__ == '__main__':
    unittest.main()
