import sqlite3


class DatabaseError(Exception):
    pass


class DatabaseHandler:
    @classmethod
    def dict_factory(cls, cursor, row):
        dictionary = {}
        for index, column in enumerate(cursor.description):
            dictionary[column[0]] = row[index]
        return dictionary

    @classmethod
    def add_noun(cls, noun, database):
        con = sqlite3.connect(database)

        if cls.exists_entry(noun.word_hash['Entry'], database):
            raise DatabaseError

        with con:
            c = con.cursor()

            c.execute(("INSERT INTO Nouns VALUES('{en}', '{gnd}', '{pl}',"
                       "'{gnt}', '{m}', '{ex}')".
                       format(en=noun.word_hash['Entry'],
                              gnd=noun.word_hash['Gender'],
                              pl=noun.word_hash['Plural'],
                              gnt=noun.word_hash['Genetive'],
                              m=noun.word_hash['Meaning'],
                              ex=noun.word_hash['Examples'])))

    @classmethod
    def add_verb(cls, verb, database):
        con = sqlite3.connect(database)

        if cls.exists_entry(verb.word_hash['Entry'], database):
            raise DatabaseError

        with con:
            c = con.cursor()

            c.execute(("INSERT INTO Verbs VALUES('{en}', '{cs}', '{prep}',"
                       "'{sep}', '{frm}', '{tran}', '{m}', '{ex}')".
                       format(en=verb.word_hash['Entry'],
                              cs=verb.word_hash['Used_case'],
                              prep=verb.word_hash['Preposition'],
                              sep=verb.word_hash['Separable'],
                              frm=verb.word_hash['Forms'],
                              tran=verb.word_hash['Transitive'],
                              m=verb.word_hash['Meaning'],
                              ex=verb.word_hash['Examples'])))

    @classmethod
    def add_adjective(cls, adj, database):
        con = sqlite3.connect(database)

        if cls.exists_entry(adj.word_hash['Entry'], database):
            raise DatabaseError

        with con:
            c = con.cursor()

            c.execute(("INSERT INTO Adjectives VALUES('{en}', '{cmp}',"
                       "'{sup}', '{m}', '{ex}')".
                       format(en=adj.word_hash['Entry'],
                              cmp=adj.word_hash['Comparative'],
                              sup=adj.word_hash['Superlative'],
                              m=adj.word_hash['Meaning'],
                              ex=adj.word_hash['Examples'])))

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
                    len(c.execute("SELECT * FROM {tb} WHERE Entry = '{w}'".
                                  format(tb=table, w=word)).fetchall()) > 0]

    @classmethod
    def extract_from_concrete_table(cls, word, database, table):
        con = sqlite3.connect(database)

        with con:
            con.row_factory = cls.dict_factory
            c = con.cursor()
            c.execute("SELECT * FROM {tb} WHERE Entry = '{w}'".
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
            c.execute("DELETE FROM {tb} WHERE Entry = '{w}'".
                      format(tb=tables_found[0], w=word))

    @classmethod
    def extract_with_meaning(cls, meaning, database):
        con = sqlite3.connect(database)

        with con:
            con.row_factory = cls.dict_factory
            c = con.cursor()
            words_with_meaning = []

            for table in ('Nouns', 'Verbs', 'Adjectives'):
                c.execute(("SELECT * FROM {tb} WHERE Meaning LIKE '% {m} %'"
                           " OR Meaning LIKE '% {m},%' OR Meaning LIKE '%{m}'"
                           " OR Meaning LIKE '%{m},%'".
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

        try:
            with con:
                c = con.cursor()
                c.execute("UPDATE {tb} SET {f} = '{n_v}' WHERE Entry = '{en}'".
                          format(tb=tables_found[0], f=field, n_v=new_value,
                                 en=entry))
        except sqlite3.OperationalError:
            raise DatabaseError

    @classmethod
    def extract_parts_of_speech(cls, parts_of_speech, database):
        con = sqlite3.connect(database)

        with con:
            con.row_factory = cls.dict_factory
            c = con.cursor()
            extracted_words = []

            for part_of_speech in parts_of_speech:
                c.execute("SELECT * FROM {pos}".format(pos=part_of_speech))
                extracted_words += c.fetchall()

            return extracted_words

    @classmethod
    def add_highscore(cls, high_score, database):
        con = sqlite3.connect(database)

        with con:
            c = con.cursor()

            c.execute(("INSERT INTO Highscores VALUES('{n}', '{dt}',"
                       "'{sc}', '{q}', '{desc}')".
                       format(n=high_score['Name'],
                              dt=high_score['Date'],
                              sc="{}%".format(str(high_score['Score'] * 100)),
                              q=high_score['Questions'],
                              desc=high_score['Description'])))

    @classmethod
    def extract_all_high_scores(cls, database):
        con = sqlite3.connect(database)

        with con:
            c = con.cursor()

            c.execute("SELECT * FROM Highscores")
            return c.fetchall()

    @classmethod
    def clear_database(cls, database):
        con = sqlite3.connect(database)

        with con:
            c = con.cursor()

            c.execute("DELETE FROM Highscores")
