import unittest

from german_dictionary.noun import Noun


class NounTest(unittest.TestCase):
    def test_word_hash(self):
        test_noun = Noun({'Entry': 'Beispiel', 'Gender': 'das',
                          'Plural': 'Beispiele', 'Genetive': 'Beispieles',
                          'Meaning': 'example', 'Examples': 'Too lazy'})
        self.assertEqual(test_noun.word_hash['Entry'], 'Beispiel')
        self.assertEqual(test_noun.word_hash['Gender'], 'das')
        self.assertEqual(test_noun.word_hash['Plural'], 'Beispiele')
        self.assertEqual(test_noun.word_hash['Genetive'], 'Beispieles')
        self.assertEqual(test_noun.word_hash['Meaning'], 'example')
        self.assertEqual(test_noun.word_hash['Examples'], 'Too lazy')

    def test_to_str(self):
        test_noun = Noun({'Entry': 'Beispiel', 'Gender': 'das',
                          'Plural': 'Beispiele', 'Genetive': 'Beispieles',
                          'Meaning': 'example', 'Examples': 'Too lazy'})
        self.assertEqual(str(test_noun),
                         ("Entry: Beispiel\nGender: das\nPlural: Beispiele\n"
                          "Genetive: Beispieles\nMeaning: example\n"
                          "Examples: Too lazy"))

if __name__ == '__main__':
    unittest.main()
