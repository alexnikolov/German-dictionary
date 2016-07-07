import unittest

from german_dictionary.dictionary import Dictionary
from german_dictionary.db_handler import DatabaseError
from german_dictionary.noun import Noun
from german_dictionary.verb import Verb
from german_dictionary.adjective import Adjective


DATABASE = 'tests/example.db'

class DictionaryTest(unittest.TestCase):
    def test_extract_entry(self):
        dictionary = Dictionary(DATABASE)
        expected_result = {'Entry': 'Lampe', 'Gender': 'die',
                           'Plural': 'Lampen', 'Genetive': 'Lampe',
                           'Meaning': 'lamp', 'Examples': '-'}
        self.assertEqual(dictionary.extract_entry('Lampe').word_hash,
                         expected_result)

    def test_extract_non_existing_entry(self):
        dictionary = Dictionary(DATABASE)
        self.assertRaises(DatabaseError, dictionary.extract_entry, 'a')

    def test_exists_entry(self):
        dictionary = Dictionary(DATABASE)
        self.assertEqual(dictionary.exists_entry('Hund'), True)
        self.assertEqual(dictionary.exists_entry('a'), False)

    def test_add_noun_and_delete(self):
        dictionary = Dictionary(DATABASE)
        test_noun = Noun({'Entry': 'xyz', 'Gender': 'das',
                          'Plural': 'Beispiele', 'Genetive': 'Beispieles',
                          'Meaning': 'example', 'Examples': 'Too lazy'})
        self.assertEqual(dictionary.exists_entry('xyz'), False)
        dictionary.add_entry(test_noun)
        self.assertEqual(dictionary.exists_entry('xyz'), True)
        dictionary.delete_entry('xyz')
        self.assertEqual(dictionary.exists_entry('xyz'), False)

    def test_add_existing_noun(self):
        dictionary = Dictionary(DATABASE)
        test_noun = Noun({'Entry': 'Hund', 'Gender': 'a',
                          'Plural': 'b', 'Genetive': 'c',
                          'Meaning': 'd', 'Examples': 'e'})
        self.assertRaises(DatabaseError, dictionary.add_entry, test_noun)

    def test_add_verb_and_delete(self):
        dictionary = Dictionary(DATABASE)
        test_verb = Verb({'Entry': 'xyz', 'Used_case': 'a',
                          'Preposition': 'b', 'Separable': 'c',
                          'Forms': 'd', 'Examples': 'e',
                          'Transitive': 'e', 'Meaning': 'm'})
        self.assertEqual(dictionary.exists_entry('xyz'), False)
        dictionary.add_entry(test_verb)
        self.assertEqual(dictionary.exists_entry('xyz'), True)
        dictionary.delete_entry('xyz')
        self.assertEqual(dictionary.exists_entry('xyz'), False)

    def test_add_existing_verb(self):
        dictionary = Dictionary(DATABASE)
        test_verb = Verb({'Entry': 'singen', 'Used_case': 'a',
                          'Preposition': 'b', 'Separable': 'c',
                          'Forms': 'd', 'Examples': 'e',
                          'Transitive': 'e', 'Meaning': 'm'})
        self.assertRaises(DatabaseError, dictionary.add_entry, test_verb)

    def test_add_adjective_and_delete(self):
        dictionary = Dictionary(DATABASE)
        test_adj = Adjective({'Entry': 'xyz', 'Comparative': 'a',
                              'Superlative': 'b',
                              'Meaning': 'c', 'Examples': 'd'})
        self.assertEqual(dictionary.exists_entry('xyz'), False)
        dictionary.add_entry(test_adj)
        self.assertEqual(dictionary.exists_entry('xyz'), True)
        dictionary.delete_entry('xyz')
        self.assertEqual(dictionary.exists_entry('xyz'), False)

    def test_add_existing_adjective(self):
        dictionary = Dictionary(DATABASE)
        test_adj = Adjective({'Entry': 'kalt', 'Comparative': 'a',
                              'Superlative': 'b',
                              'Meaning': 'c', 'Examples': 'd'})
        self.assertRaises(DatabaseError, dictionary.add_entry, test_adj)

    def test_extract_no_entries_with_meaning(self):
        dictionary = Dictionary(DATABASE)
        self.assertEqual(dictionary.extract_entries_with_meaning('xyz'), [])

    def test_extract_one_entry_with_meaning(self):
        dictionary = Dictionary(DATABASE)
        entries_with_meaning = dictionary.extract_entries_with_meaning('dog')
        self.assertEqual(len(entries_with_meaning), 1)
        self.assertEqual(entries_with_meaning[0].word_hash['Entry'], 'Hund')

    def test_extract_two_entries_with_meaning(self):
        dictionary = Dictionary(DATABASE)
        entries_with_meaning = dictionary.extract_entries_with_meaning('lovely')
        self.assertEqual(len(entries_with_meaning), 2)
        first_entry = entries_with_meaning[0].word_hash['Entry']
        second_entry = entries_with_meaning[1].word_hash['Entry']
        self.assertEqual((first_entry, second_entry), ('schön', 'hübsch'))

    def test_edit_noun_field(self):
        dictionary = Dictionary(DATABASE)
        self.assertEqual(dictionary.extract_entry('Hund').word_hash['Gender'],
                    'der')
        dictionary.edit_entry('Hund', 'Gender', 'a')
        self.assertEqual(dictionary.extract_entry('Hund').word_hash['Gender'],
                    'a')
        dictionary.edit_entry('Hund', 'Gender', 'der')
        self.assertEqual(dictionary.extract_entry('Hund').word_hash['Gender'],
                    'der')

    def test_edit_verb_field(self):
        dictionary = Dictionary(DATABASE)
        self.assertEqual(dictionary.extract_entry('singen').\
                         word_hash['Used_case'], 'akk')
        dictionary.edit_entry('singen', 'Used_case', 'dat')
        self.assertEqual(dictionary.extract_entry('singen').\
                         word_hash['Used_case'], 'dat')
        dictionary.edit_entry('singen', 'Used_case', 'akk')
        self.assertEqual(dictionary.extract_entry('singen').\
                         word_hash['Used_case'], 'akk')

    def test_edit_adjective_field(self):
        dictionary = Dictionary(DATABASE)
        self.assertEqual(dictionary.extract_entry('kalt').\
                         word_hash['Meaning'], 'cold')
        dictionary.edit_entry('kalt', 'Meaning', 'hot')
        self.assertEqual(dictionary.extract_entry('kalt').\
                         word_hash['Meaning'], 'hot')
        dictionary.edit_entry('kalt', 'Meaning', 'cold')
        self.assertEqual(dictionary.extract_entry('kalt').\
                         word_hash['Meaning'], 'cold')

    def test_edit_noun_with_non_existing_field(self):
        dictionary = Dictionary(DATABASE)
        self.assertRaises(DatabaseError, dictionary.edit_entry,
                          'Hund', 'Superlative', 'a')

    def test_extract_entry_with_trie_enabled(self):
        dictionary = Dictionary(DATABASE, True)
        expected_result = {'Entry': 'Lampe', 'Gender': 'die',
                           'Plural': 'Lampen', 'Genetive': 'Lampe',
                           'Meaning': 'lamp', 'Examples': '-'}
        self.assertEqual(dictionary.extract_entry('Lampe').word_hash,
                         expected_result)

    def test_extract_non_existing_entry_with_trie_enabled(self):
        dictionary = Dictionary(DATABASE, True)
        self.assertRaises(DatabaseError, dictionary.extract_entry, 'a')

    def test_add_word_and_delete_with_trie_enabled(self):
        dictionary = Dictionary(DATABASE, True)
        test_noun = Noun({'Entry': 'xyz', 'Gender': 'das',
                          'Plural': 'Beispiele', 'Genetive': 'Beispieles',
                          'Meaning': 'example', 'Examples': 'Too lazy'})
        self.assertEqual(dictionary.exists_entry('xyz'), False)
        dictionary.add_entry(test_noun)
        self.assertEqual(dictionary.exists_entry('xyz'), True)
        dictionary.delete_entry('xyz')
        self.assertEqual(dictionary.exists_entry('xyz'), False)

    def test_add_existing_word_with_trie_enabled(self):
        dictionary = Dictionary(DATABASE, True)
        test_noun = Noun({'Entry': 'Hund', 'Gender': 'a',
                          'Plural': 'b', 'Genetive': 'c',
                          'Meaning': 'd', 'Examples': 'e'})
        self.assertRaises(DatabaseError, dictionary.add_entry, test_noun)

    def test_edit_word_field_with_trie_enabled(self):
        dictionary = Dictionary(DATABASE, True)
        self.assertEqual(dictionary.extract_entry('Hund').word_hash['Gender'],
                    'der')
        dictionary.edit_entry('Hund', 'Gender', 'a')
        self.assertEqual(dictionary.extract_entry('Hund').word_hash['Gender'],
                    'a')
        dictionary.edit_entry('Hund', 'Gender', 'der')
        self.assertEqual(dictionary.extract_entry('Hund').word_hash['Gender'],
                    'der')


if __name__ == '__main__':
    unittest.main()
