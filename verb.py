import word
import sqlite3
import db_handler


class Verb(word.Word):
    def __init__(self, db_hash):
        super(Verb, self).__init__(db_hash)

        #self.forms = db_hash['Forms']
        #self.transitive = db_hash['Transitive']
        #self.case = db_hash['Used_case']
        #self.preposition = db_hash['Preposition']
        #self.separable = db_hash['Separable']

    def add_entry(self, database):
        db_handler.DatabaseHandler.add_verb(self, database)

    def __str__(self):
        return ("Entry: {}\nCase: {}\nPreposition: {}\nSeparable: {}\n"
                "Forms: {}\nTransitive: {}\nMeaning: {}\nExamples: {}".\
                format(self.word_hash['Entry'], self.word_hash['Used_case'],
                       self.word_hash['Preposition'],
                       self.word_hash['Separable'],
                       self.word_hash['Forms'],
                       self.word_hash['Transitive'],
                       self.word_hash['Meaning'],
                       self.word_hash['Examples']))

    @classmethod
    def fields(cls):
        return ('Entry', 'Case', 'Preposition', 'Separable', 'Forms',
                'Transitive', 'Meaning', 'Examples')