from german_dictionary.db_handler import DatabaseHandler, DatabaseError
from german_dictionary.noun import Noun
from german_dictionary.verb import Verb
from german_dictionary.adjective import Adjective
from german_dictionary.trie import Trie
import sys


class Dictionary:
    def __init__(self, database, trie=False):
        self.database = database

        if trie:
            self.initialize_trie()

    def initialize_trie(self):
        self.trie = Trie()
        all_words = []

        for part_of_speech in ['Nouns', 'Verbs', 'Adjectives']:
            all_words_from_one_pos = DatabaseHandler.\
                extract_parts_of_speech([part_of_speech], self.database)

            class_name = getattr(sys.modules[__name__], part_of_speech[:-1])

            for word_hash in all_words_from_one_pos:
                all_words.append(class_name(word_hash))

        for word in all_words:
            self.trie.add_word(word)

    def extract_entry(self, word):
        try:
            found_entry = self.trie.search_for_word(word)
            if found_entry:
                return found_entry
            raise DatabaseError
        except AttributeError:
            entry_data = DatabaseHandler.extract_entry(word, self.database)
            class_name = getattr(sys.modules[__name__], entry_data[1][:-1])
            return class_name(entry_data[0])

    def add_entry(self, word):
        word.add_entry(self.database)

        try:
            self.trie.add_word(word)
        except AttributeError:
            return

    def exists_entry(self, word):
        try:
            return bool(self.trie.search_for_word(word))
        except AttributeError:
            return DatabaseHandler.exists_entry(word, self.database)

    def delete_entry(self, word):
        DatabaseHandler.delete_entry(word, self.database)

        try:
            self.trie.delete_word(word)
        except AttributeError:
            return

    def extract_entries_with_meaning(self, meaning):
        found_entries_data = DatabaseHandler.\
                             extract_with_meaning(meaning, self.database)
        found_entries = []

        for word_type in found_entries_data:
            for entry_data, part_of_speech in word_type:
                class_name = getattr(sys.modules[__name__], part_of_speech)
                found_entries.append(class_name(entry_data))

        return found_entries

    def edit_entry(self, entry, field, new_value):
        DatabaseHandler.edit_entry(entry, field, new_value, self.database)

        try:
            word_in_trie = self.trie.search_for_word(entry)

            if field == 'Entry':
                self.trie.delete_word(word_in_trie.word_hash['Entry'])
                word_in_trie.word_hash['Entry'] = new_value
                self.trie.add_word(word_in_trie)
            else:
                word_in_trie.word_hash[field] = new_value
        except AttributeError:
            return
