import sqlite3
import sys


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
        cls.check_single_table_found(tables_found)

        return cls.extract_from_concrete_table(word, database, tables_found[0])

    @classmethod
    def check_single_table_found(cls, tables_found):
        if len(tables_found) == 0:
            raise DatabaseError('Entry not found')
        elif len(tables_found) >= 2:
            raise DatabaseError('Multiple entries found')

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

            return (found_entry, table)

    @classmethod
    def exists_entry(cls, word, database):
        return len(cls.locate_table_for_entry(word, database)) > 0

    @classmethod
    def delete_entry(cls, word, database):
        tables_found = cls.locate_table_for_entry(word, database)
        cls.check_single_table_found(tables_found)

        con = sqlite3.connect(database)

        with con:
            c = con.cursor()
            c.execute("DELETE FROM {tb} WHERE Entry = '{w}'".\
                      format(tb=tables_found[0], w=word))

    @classmethod
    def extract_with_meaning(cls, meaning, database):
        con = sqlite3.connect(database)

        with con:
            con.row_factory = sqlite3.Row
            c = con.cursor()
            words_with_meaning = []

            for table in ('Nouns', 'Verbs', 'Adjectives'):
                c.execute(("SELECT * FROM {tb} WHERE Meaning LIKE '% {m} %'"
                           " OR Meaning LIKE '% {m},%' OR Meaning LIKE '%{m}'"
                           " OR Meaning LIKE '%{m},%'".\
                           format(tb=table, m=meaning)))
                from_one_table = c.fetchall()
                from_one_table = zip(from_one_table,
                                     [table[:-1]] * len(from_one_table))
                words_with_meaning.append(from_one_table)

            return words_with_meaning

    @classmethod
    def edit_entry(cls, entry, field, new_value, database):
        tables_found = cls.locate_table_for_entry(entry, database)
        cls.check_single_table_found(tables_found)

        con = sqlite3.connect(database)

        with con:
            c = con.cursor()
            c.execute("UPDATE {tb} SET {f} = '{n_v}' WHERE Entry = '{en}'".\
                      format(tb=tables_found[0], f=field, n_v=new_value,
                             en=entry))


