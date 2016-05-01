class Word:
    def __init__(self, db_hash):
        #self.entry = db_hash['Entry']
        #self.meaning = db_hash['Meaning']
        #self.examples = db_hash['Examples']
        self.word_hash = db_hash

    def word_hash(self):
        return self.word_hash