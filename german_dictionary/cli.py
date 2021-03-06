from german_dictionary.dictionary import Dictionary, Noun, Verb, Adjective
from german_dictionary.db_handler import DatabaseError
from german_dictionary.quiz import Quiz
from german_dictionary.highscore import HighScore
import re
import sys


class DictionaryCLI:
    def __init__(self, database, hs_database, trie_on):
        self.database = database
        self.trie_on = trie_on
        self.dictionary = Dictionary(database, trie_on)
        self.hs_database = hs_database

    def mainloop(self):
        while True:
            user_input = input('> ')

            self.evaluate_user_input(user_input)

            if user_input is 'q':
                break

    def evaluate_user_input(self, user_input):
        self.check_view_match(user_input)
        self.check_add_match(user_input)
        self.check_delete_match(user_input)
        self.check_edit_match(user_input)
        self.check_meaning_match(user_input)

        self.check_quiz_match(user_input)
        self.check_view_hs_match(user_input)
        self.check_trie_match(user_input)

        help_match = re.search('\s*help\s*', user_input)
        if help_match:
            self.print_help()

    def print_help(self):
        print("'view *word*' -> extracts the word from the dictionary")
        print("'add *word*' -> adds word to the dictionary")
        print("'delete *word*' -> deletes words from the dictionary")
        print("'edit *word*' -> edits words from the dictionary")
        print("'cm *word*' -> extracts words with a common meaning (cm)")
        print("'quiz m' -> starts the interactive meanings quiz for all words")
        print("'quiz nouns' -> starts the interactive nouns quiz")
        print("'quiz verbs' -> starts the interactive verbs quiz")
        print("'hs' -> views all recorded high scores")
        print("'toggle trie' -> toggles trie searching")

    def check_view_match(self, user_input):
        view_match = re.search('\s*view\s+([a-zA-Z]+)\s*', user_input)
        if view_match:
            try:
                word = self.dictionary.extract_entry(view_match.group(1))
            except DatabaseError:
                print("\nError: The word '{}' was not found.".
                      format(view_match.group(1)))
            else:
                print('\n{}'.format(word))

    def check_add_match(self, user_input):
        add_match = re.search('\s*add\s+([a-zA-Z]+)\s*', user_input)
        if add_match:
            if self.dictionary.exists_entry(add_match.group(1)):
                print("\nError: The word '{}' is already in the database.".
                      format(add_match.group(1)))
            else:
                while True:
                    part_of_speech = input('\nPart of speech: ')

                    if re.search('\s*(n|noun|Noun)\s*', part_of_speech):
                        self.add_word('Noun', add_match.group(1))
                        break
                    elif re.search('\s*(adj|adjective|Adjective)\s*',
                                   part_of_speech):
                        self.add_word('Adjective', add_match.group(1))
                        break
                    elif re.search('\s*(v|verb|Verb)\s*', part_of_speech):
                        self.add_word('Verb', add_match.group(1))
                        break
                    else:
                        print('Error: Please enter a valid part of speech.')

    def add_word(self, part_of_speech, new_entry):
        class_name = getattr(sys.modules[__name__], part_of_speech)
        word_hash = {'Entry': new_entry}

        for field in class_name.fields()[1:]:
            field_data = input('{}: '.format(field))
            word_hash[field] = field_data

        new_word = class_name(word_hash)
        self.dictionary.add_entry(new_word)
        print("\nEntry '{}' added successfully.".format(new_entry))

    def check_delete_match(self, user_input):
        delete_match = re.search('\s*delete\s+([a-zA-Z]+)\s*', user_input)
        if delete_match:
            if not self.dictionary.exists_entry(delete_match.group(1)):
                print("\nError: The word '{}' was not found.".
                      format(delete_match.group(1)))
            else:
                self.dictionary.delete_entry(delete_match.group(1))
                print('\nEntry successfully deleted from the database.')

    def check_edit_match(self, user_input):
        edit_match = re.search('\s*edit\s+([a-zA-Z]+)\s*', user_input)
        if edit_match:
            if not self.dictionary.exists_entry(edit_match.group(1)):
                print("\nError: The word '{}' was not found.".
                      format(edit_match.group(1)))
            else:
                found_word = self.dictionary.extract_entry(edit_match.group(1))

                while True:
                    field = input(('Enter one of the following fields to edit:'
                                   '\n{}\n').format(', '.join(type(found_word).
                                                    fields())))

                    if field in type(found_word).fields():
                        break

                print('\nOld value: {}'.format(found_word.word_hash[field]))
                new_value = input('New value: ')

                self.dictionary.edit_entry(edit_match.group(1), field,
                                           new_value)
                print('Word edited successfully.')

    def check_meaning_match(self, user_input):
        meaning_match = re.search('\s*cm\s+([a-zA-Z]+)\s*', user_input)
        if meaning_match:
            found_entries = self.dictionary.\
                extract_entries_with_meaning(meaning_match.group(1))
            if len(found_entries) is 0:
                print("\nNo entries with the meaning '{}'' found.".
                      format(meaning_match.group(1)))
            else:
                for entry in found_entries:
                    print('\n{}'.format(entry))

    def check_quiz_match(self, user_input):
        quiz_match = re.search('\s*quiz\s+([a-zA-Z]+)\s*', user_input)
        if quiz_match:
            if quiz_match.group(1) == 'm':
                self.initiate_quiz(['Nouns', 'Adjectives', 'Verbs'],
                                   ['Meaning'])
            elif quiz_match.group(1) == 'nouns':
                self.initiate_quiz(['Nouns'], ['Gender', 'Plural'])
            elif quiz_match.group(1) == 'verbs':
                self.initiate_quiz(['Verbs'], ['Forms'])

    def initiate_quiz(self, parts_of_speech, fields):
        quiz = Quiz(self.database, parts_of_speech, fields)

        while len(quiz.words_to_guess) > 0:
            current_word = quiz.current_word

            print('Score: {}%'.format("%.2f" % (quiz.score * 100)))
            print('Current word: {}\n'.format(current_word.word_hash['Entry']))

            guesses = []

            for field in fields:
                current_guess = input('{}: '.format(field))

                while current_guess == 'h':
                    print(quiz.hint(field), '\n')
                    current_guess = input('{}: '.format(field))

                if current_guess == 'q':
                    self.initiate_quiz_ending(quiz)
                    self.mainloop()

                guesses.append(current_guess)

            guess_results = quiz.guess(guesses)
            answer_statement = quiz.answer_statements(guess_results)

            print('\n{}'.format(answer_statement))

        self.initiate_quiz_ending(quiz)

    def initiate_quiz_ending(self, quiz):
        print('Final score: {}%'.format("%.2f" % (quiz.score * 100)), '\n')

        name = input('Enter name for high score: ')
        high_score = HighScore(name, quiz)
        high_score.add_high_score(self.hs_database)

    def check_view_hs_match(self, user_input):
        view_hs_match = re.search('\s*hs\s*', user_input)
        if view_hs_match:
            all_high_scores = HighScore.\
                              extract_all_high_scores(self.hs_database)
            all_high_scores.sort(reverse=True)

            for high_score in all_high_scores:
                print('; '.join(str(x) for x in high_score))

    def check_trie_match(self, user_input):
        check_trie_on = re.search('\s*toggle\s+tree\s*', user_input)
        if check_trie_on:
            self.dictionary.toggle_trie()

            if self.dictionary.tree_on:
                print('Trie searching turned successfully on.\n')
            else:
                print('Trie searching turned successfully off.\n')


def main():
    app = DictionaryCLI('./data/words.db', './data/highscores.db', False)
    app.mainloop()


if __name__ == '__main__':
    main()
