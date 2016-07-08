from german_dictionary.db_handler import DatabaseHandler
from german_dictionary.word import Word
from random import randint


class Quiz:
    def __init__(self, database, parts_of_speech, fields_to_be_guessed):
        self.database = database
        self.parts_of_speech = parts_of_speech
        self.fields_to_be_guessed = fields_to_be_guessed

        self.score = 0
        self.answers = 0
        self.words_to_guess = DatabaseHandler.\
            extract_parts_of_speech(parts_of_speech, self.database)
        self.words_to_guess = list(map(lambda x: Word(x), self.words_to_guess))
        self.current_word = self.\
            words_to_guess[randint(0, len(self.words_to_guess) - 1)]

    def guess(self, suggestions):
        suggestions_with_fields = zip(suggestions, self.fields_to_be_guessed)
        guess_results = []

        for suggestion in suggestions_with_fields:
            correct_answer = self.current_word.word_hash[suggestion[1]]
            guess_results.append(self.evaluate_answer(suggestion,
                                 self.split_answers_to_set(correct_answer)))

        self.update_score(guess_results)
        self.pick_new_current_word()
        return guess_results

    def pick_new_current_word(self):
        self.words_to_guess.remove(self.current_word)
        if len(self.words_to_guess) > 0:
            self.current_word = self.\
                words_to_guess[randint(0, len(self.words_to_guess) - 1)]

    def update_score(self, guess_results):
        field_scores = list(map(lambda result: result[0], guess_results))
        word_score = sum(field_scores) / len(field_scores)
        self.score = (self.answers * self.score + word_score) / \
                     (self.answers + 1)
        self.answers += 1

    def split_answers_to_set(self, answers):
        split_answers = answers.split(',')
        stripped_answers = map(lambda a: a.lstrip().rstrip(), split_answers)
        return set(stripped_answers)

    def evaluate_answer(self, suggestion_with_field, correct_answers):
        suggested_answers = self.split_answers_to_set(suggestion_with_field[0])

        if suggested_answers == correct_answers:
            return [1, 'Correct']
        elif len(suggested_answers & correct_answers) is 0:
            return [0, correct_answers]
        else:
            return [len(correct_answers & suggested_answers) /
                    len(correct_answers), correct_answers]

    def answer_statements(self, guess_results):
        answer_statement = ''
        for index, field in enumerate(guess_results):
            if field[1] is 'Correct':
                answer_statement += '{} guessed correctly\n'.\
                    format(self.fields_to_be_guessed[index])
            elif field[0] > 0:
                answer_statement += 'Almost, this is the full answer: {}\n'.\
                    format(', '.join(field[1]))
            else:
                answer_statement += 'Nope, this is the correct answer: {}\n'.\
                    format(', '.join(field[1]))

        return answer_statement

    def hint(self, field):
        if field == 'Meaning':
            meaning = self.current_word.word_hash['Meaning']

            if len(self.split_answers_to_set(meaning)) > 1:
                return "Hint: One meaning starts with '{}'".format(meaning[0])
            return "Hint: It starts with '{}'".format(meaning[0])
        return 'Hints are not available for this quiz.'
