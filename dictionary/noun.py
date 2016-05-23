from word import Word
from db_handler import DatabaseHandler


class Noun(Word):
    def __init__(self, db_hash):
        super(Noun, self).__init__(db_hash)

    def add_entry(self, database):
        db_handler.DatabaseHandler.add_noun(self, database)
    
    def __str__(self):
        return ("Entry: {}\nGender: {}\nPlural: {}\nGenetive: {}\nMeaning: {}"
                "\nExamples: {}".format(self.word_hash['Entry'], 
                                        self.word_hash['Gender'],
                                        self.word_hash['Plural'],
                                        self.word_hash['Genetive'],
                                        self.word_hash['Meaning'],
                                        self.word_hash['Examples']))

    @classmethod
    def fields(cls):
        return ('Entry', 'Gender', 'Plural', 'Genetive', 'Meaning',
                'Examples')