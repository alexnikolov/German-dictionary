from word import Word
from db_handler import DatabaseHandler


class Adjective(Word):
    def __init__(self, db_hash):
        super(Adjective, self).__init__(db_hash)

    def add_entry(self, database):
        DatabaseHandler.add_verb(self, database)

    def __str__(self):
        return ("Entry: {}\nComparative: {}\nSuperlative: {}\nMeaning: {}\n"
                "Examples: {}".format(self.word_hash['Entry'],
                                      self.word_hash['Comparative'],
                                      self.word_hash['Superlative'],
                                      self.word_hash['Meaning'],
                                      self.word_hash['Examples']))

    @classmethod
    def fields(cls):
        return ('Entry', 'Comparative', 'Superlative', 'Meaning', 'Examples')
