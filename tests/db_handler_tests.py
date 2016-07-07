import unittest

from german_dictionary.db_handler import DatabaseHandler, DatabaseError
from german_dictionary.noun import Noun
from german_dictionary.verb import Verb
from german_dictionary.adjective import Adjective

DATABASE = 'tests/example.db'
HS_DB = 'tests/highscores.db'

class DatabaseHandlerTest(unittest.TestCase):
    def test_exists_entry(self):
        handler = DatabaseHandler()
        self.assertEqual(handler.exists_entry('xyz', DATABASE), False)
        self.assertEqual(handler.exists_entry('Hund', DATABASE), True)

    def test_add_noun_and_delete(self):
        handler = DatabaseHandler()
        test_noun = Noun({'Entry': 'xyz', 'Gender': 'das',
                          'Plural': 'Beispiele', 'Genetive': 'Beispieles',
                          'Meaning': 'example', 'Examples': 'Too lazy'})
        self.assertEqual(handler.exists_entry('xyz', DATABASE), False)
        handler.add_noun(test_noun, DATABASE)
        self.assertEqual(handler.exists_entry('xyz', DATABASE), True)
        handler.delete_entry('xyz', DATABASE)
        self.assertEqual(handler.exists_entry('xyz', DATABASE), False)

    def test_add_verb_and_delete(self):
        handler = DatabaseHandler()
        test_verb = Verb({'Entry': 'xyz', 'Used_case': 'a',
                          'Preposition': 'b', 'Separable': 'c',
                          'Forms': 'd', 'Examples': 'e',
                          'Transitive': 'e', 'Meaning': 'm'})
        self.assertEqual(handler.exists_entry('xyz', DATABASE), False)
        handler.add_verb(test_verb, DATABASE)
        self.assertEqual(handler.exists_entry('xyz', DATABASE), True)
        handler.delete_entry('xyz', DATABASE)
        self.assertEqual(handler.exists_entry('xyz', DATABASE), False)

    def test_add_adjective_and_delete(self):
        handler = DatabaseHandler()
        test_adj = Adjective({'Entry': 'xyz', 'Comparative': 'a',
                              'Superlative': 'b',
                              'Meaning': 'c', 'Examples': 'd'})
        self.assertEqual(handler.exists_entry('xyz', DATABASE), False)
        handler.add_adjective(test_adj, DATABASE)
        self.assertEqual(handler.exists_entry('xyz', DATABASE), True)
        handler.delete_entry('xyz', DATABASE)
        self.assertEqual(handler.exists_entry('xyz', DATABASE), False)

    def test_existing_extract_entry(self):
        handler = DatabaseHandler()
        expected_result = {'Entry': 'Lampe', 'Gender': 'die',
                           'Plural': 'Lampen', 'Genetive': 'Lampe',
                           'Meaning': 'lamp', 'Examples': '-'}
        self.assertEqual(handler.extract_entry('Lampe', DATABASE)[0], expected_result)

    def test_nonexisting_extract_entry(self):
        handler = DatabaseHandler()
        self.assertRaises(DatabaseError, handler.extract_entry,
                          'xyz', DATABASE)

    def test_edit_entry(self):
        handler = DatabaseHandler()
        self.assertEqual(handler.extract_entry('Hund', DATABASE)[0]['Gender'],
                         'der')
        handler.edit_entry('Hund', 'Gender', 'xyz', DATABASE)
        self.assertEqual(handler.extract_entry('Hund', DATABASE)[0]['Gender'],
                         'xyz')
        handler.edit_entry('Hund', 'Gender', 'der', DATABASE)
        self.assertEqual(handler.extract_entry('Hund', DATABASE)[0]['Gender'],
                         'der')

    def test_add_high_score(self):
        handler = DatabaseHandler()
        high_score = {'Name': 'Robert', 'Date': '07.08.2016 11:30:30',
                      'Score': '0.7', 'Questions': '7',
                      'Description': 'Nouns with Meaning'}
        handler.add_highscore(high_score, HS_DB)
        all_high_scores = handler.extract_all_high_scores(HS_DB)
        self.assertEqual(len(all_high_scores), 1)
        self.assertEqual(all_high_scores[0][0], 'Robert')
        handler.clear_database(HS_DB)

if __name__ == '__main__':
    unittest.main()
