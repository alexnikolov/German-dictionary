import word
import sqlite3
import db_handler


class Adjective(word.Word):
    def __init__(self, db_hash):
        super(Adjective, self).__init__(db_hash)

        self.comparative = db_hash['Comparative']
        self.superlative = db_hash['Superlative']

    def add_entry(self, database):
        db_handler.DatabaseHandler.add_verb(self, database)

    def __str__(self):
        return ("Entry: {}\nComparative: {}\nSuperlative: {}\nMeaning: {}\n"
                "Examples: {}".format(self.entry, self.comparative,
                                      self.superlative, self.meaning,
                                      self.examples))

    @classmethod
    def fields(cls):
        return ('Entry', 'Comparative', 'Superlative', 'Meaning', 'Examples')