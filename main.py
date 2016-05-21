import sqlite3
import noun
import verb
import dictionary
import quiz

conn = sqlite3.connect('words.db')
c = conn.cursor()


#c.execute("SELECT * FROM {db} WHERE {en}='{w}'".\
#       format(db="Adjectives", en="Meaning", w="Hand"))



print(len(c.execute('SELECT * FROM {db} WHERE Meaning LIKE "% {meaning} %" OR Meaning LIKE "% {meaning},%" OR Meaning LIKE "%{meaning}" OR Meaning LIKE "%{meaning},%"'.\
        format(db="Adjectives", meaning="lovely")).fetchall()))

all_words = c.fetchall()
print(len(all_words))
print(all_words)

n = noun.Noun({'Entry': 'A', 'Gender': 'B', 'Plural': 'C', 'Genetive': 'D', 'Meaning': 'E', 'Examples': 'F'})
v = verb.Verb({'Entry': 'A', 'Used_case': 'B', 'Preposition': 'C', 'Separable': 'D', 'Forms': 'E',
               'Transitive': 'F', 'Meaning': 'G', 'Examples': 'H'})
#n.add_entry('words.db')
#v.add_entry('words.db')

#d = dictionary.Dictionary('words.db')
#x = d.extract_entry('Hund')
#print(x)

#print(d.exists_entry("Sandwich"))
#print(d.delete_entry("A"))

#s = d.extract_entries_with_meaning("lovely")
#for word in s:
  #print(word)

#d.edit_entry("A", 'Gender', 'XYZ')

q = quiz.Quiz('wordzzz.db', ['Adjectives'], ['Meaning', 'Comparative'])
print(q.guess(['great', 'abc']), q.score)