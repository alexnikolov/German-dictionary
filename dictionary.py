import sqlite3
from db_handler import DatabaseHandler
from noun import Noun
from verb import Verb
from adjective import Adjective
import sys


class Dictionary:
    def __init__(self, database):
        self.database = database

    def extract_entry(self, word):
        entry_data = DatabaseHandler.extract_entry(word, self.database)
        class_name = getattr(sys.modules[__name__], entry_data[1][:-1])
        return class_name(entry_data[0])

    def add_entry(self, word):
        word.add_entry(self.database)

    def exists_entry(self, word):
        return DatabaseHandler.exists_entry(word, self.database)

    def delete_entry(self, word):
        DatabaseHandler.delete_entry(word, self.database)

    def extract_entries_with_meaning(self, meaning):
        found_entries_data = DatabaseHandler.\
                             extract_with_meaning(meaning, self.database)
        found_entries = []

        for word_type in found_entries_data:
            for entry_data, part_of_speech in word_type:
                class_name = getattr(sys.modules[__name__], part_of_speech)
                found_entries.append(class_name(entry_data))

        return found_entries
