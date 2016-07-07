import unittest

from german_dictionary.quiz import Quiz

DATABASE = 'tests/quiz.db'

class QuizTest(unittest.TestCase):
    def test_guess_meaning_one_answer(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        quiz.guess(['a'])
        self.assertEqual(quiz.score, 0.25)

    def test_guess_meaning_some_answer(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        quiz.guess(['a, c'])
        self.assertEqual(quiz.score, 0.5)

    def test_guess_meaning_all_answers(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        quiz.guess(['a, d, b, c'])
        self.assertEqual(quiz.score, 1)

    def test_answers_meaning_one_answer(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        self.assertEqual(quiz.evaluate_answer(['a', 'Meaning'], 
                                              set(['a', 'b', 'c', 'd'])),
                         [0.25, {'a', 'b', 'c', 'd'}])

    def test_answers_meaning_some_answers(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        self.assertEqual(quiz.evaluate_answer(['a, c', 'Meaning'], 
                                              set(['a', 'b', 'c', 'd'])),
                         [0.5, {'a', 'b', 'c', 'd'}])

    def test_answers_meaning_all_answers(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        self.assertEqual(quiz.evaluate_answer(['a, c, d, b', 'Meaning'], 
                                              set(['a', 'b', 'c', 'd'])),
                         [1, 'Correct'])

    def test_hint_with_multiple_answers(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        self.assertEqual(quiz.hint('Meaning'), "Hint: One meaning starts with 'a'")

    def test_hint_with_single_answer(self):
        quiz = Quiz(DATABASE, ['Verbs'], ['Meaning'])
        self.assertEqual(quiz.hint('Meaning'), "Hint: It starts with 'o'")

    def test_hint_with_no_meaning(self):
        quiz = Quiz(DATABASE, ['Nouns'], ['Meaning'])
        self.assertEqual(quiz.hint('Gender'), 'Hints are not available for this quiz.')


if __name__ == '__main__':
    unittest.main()
