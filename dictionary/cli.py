from dictionary import Dictionary
from db_handler import DatabaseError
import re


class DictionaryCLI:
    def __init__(self, database):
        self.database = database
        self.dictionary = Dictionary(database)

    def mainloop(self):
        while True:
            user_input = input('> ')

            self.evaluate_user_input(user_input)

            if user_input is 'q':
                break

    def evaluate_user_input(self, user_input):
        view_match = re.search('\s*view\s+([a-zA-Z]+)\s*', user_input)
        if view_match:
            try:
                word = self.dictionary.extract_entry(view_match.group(1))
            except DatabaseError:
                print("Error: The word '{}' was not found.".
                      format(view_match.group(1)))
            else:
                print(word)

        help_match = re.search('\s*help\s*', user_input)
        if help_match:
            self.print_help()

    def print_help(self):
        print("'view *word*' -> extracts words from the dictionary")


def main():
    app = DictionaryCLI('words.db')
    app.mainloop()


if __name__ == '__main__':
    main()