import word
import sqlite3
import db_handler


class Noun(word.Word):
    def __init__(self, db_hash):
        super(Noun, self).__init__(db_hash)

        self.gender = db_hash['Gender']
        self.plural = db_hash['Plural']
        self.genetive = db_hash['Genetive']

    def add_entry(self, database):
        db_handler.DatabaseHandler.add_noun(self, database)
    
    def __str__(self):
        return ("Entry: {}\nGender: {}\nPlural: {}\nGenetive: {}\nMeaning: {}"
                "\nExamples: {}".format(self.entry, self.gender, self.plural,
                                        self.genetive, self.meaning,
                                        self.examples))

    def fields(self):
        return ('Entry', 'Gender', 'Plural', 'Genetive', 'Meaning',
                'Examples')