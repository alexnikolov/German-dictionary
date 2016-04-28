import sqlite3
import db_handler
import noun
import verb
import adjective


class Dictionary:
    def __init__(self, database):
        self.database = database

    def extract_entry(self, word):
        return db_handler.DatabaseHandler.extract_entry(word, self.database)