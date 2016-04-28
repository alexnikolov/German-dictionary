import sqlite3

class DatabaseHandler:
    @classmethod
    def add_noun(cls, noun, database):
        con = sqlite3.connect(database)

        with con:
            c = con.cursor()

            c.execute(("INSERT INTO Nouns VALUES('{en}', '{gnd}', '{pl}',"
                       "'{gnt}', '{m}', '{ex}')".\
                       format(en=noun.entry, gnd=noun.gender, pl=noun.plural,
                              gnt=noun.genetive, m=noun.meaning, 
                              ex=noun.examples)))

    @classmethod
    def add_verb(cls, verb, database):
        con = sqlite3.connect(database)

        with con:
            c = con.cursor()

            c.execute(("INSERT INTO Verbs VALUES('{en}', '{cs}', '{prep}',"
                       "'{sep}', '{frm}', '{tran}', '{m}', '{ex}')".\
                       format(en=verb.entry, cs=verb.case, 
                              prep=verb.preposition, sep=verb.separable,
                              frm=verb.forms, tran=verb.transitive,
                              m=verb.meaning, ex=verb.examples)))

    @classmethod
    def add_adjective(cls, adj, database):
        con = sqlite3.connect(database)

        with con:
            c = con.cursor()
            ['Entry', 'Comparative', 'Superlative', 'Meaning', 'Examples']
            c.execute(("INSERT INTO Adjective VALUES('{en}', '{cmp}',"
                       "'{sup}', '{m}', '{ex}')".\
                       format(en=adj.entry, cmp=adj.comparative,
                              sup=adj.superlative, m=verb.meaning,
                              ex=verb.examples)))
