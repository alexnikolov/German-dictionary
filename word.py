class Word:
    def __init__(self, db_hash):
        self.entry = db_hash['Entry']
        self.meaning = db_hash['Meaning']
        self.examples = db_hash['Examples']