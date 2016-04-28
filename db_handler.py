import sqlite3
import noun
import verb
import adjective


class DatabaseError(Exception):
    pass

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

            c.execute(("INSERT INTO Adjective VALUES('{en}', '{cmp}',"
                       "'{sup}', '{m}', '{ex}')".\
                       format(en=adj.entry, cmp=adj.comparative,
                              sup=adj.superlative, m=verb.meaning,
                              ex=verb.examples)))

    @classmethod
    def extract_entry(cls, word, database):
        tables_found = cls.locate_table_for_entry(word, database)

        if len(tables_found) == 0:
            raise DatabaseError('Entry not found')
        elif len(tables_found) >= 2:
            raise DatabaseError('Multiple entries found')

        return cls.extract_from_concrete_table(word, database, tables_found[0])

    @classmethod
    def locate_table_for_entry(cls, word, database):
        con = sqlite3.connect(database)

        with con:
            c = con.cursor()
            return [table for table in ['Nouns', 'Verbs', 'Adjectives'] if
                    len(c.execute("SELECT * FROM {tb} WHERE Entry = '{w}'".\
                                  format(tb=table, w=word)).fetchall()) > 0]

    @classmethod
    def extract_from_concrete_table(cls, word, database, table):
        con = sqlite3.connect(database)

        with con:
            con.row_factory = sqlite3.Row
            c = con.cursor()
            c.execute("SELECT * FROM {tb} WHERE Entry = '{w}'".\
                      format(tb=table, w=word))
            found_entry = c.fetchall()[0]

            print(found_entry['Entry'])
            if table == 'Nouns':
                return noun.Noun(found_entry)
            elif table == 'Verbs':
                return verb.Verb(found_entry)
            elif table == 'Adjectives':
                return adjective.Adjective(found_entry)
