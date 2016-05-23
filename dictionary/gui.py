import tkinter as tk
import tkinter.messagebox as mbox

from dictionary import Dictionary
from db_handler import DatabaseError
from quiz import Quiz
#from ./lib import db_handler
#from ..lib import quiz
#from dictionary import *
#from db_handler import DatabaseError
#from quiz import Quiz
import sys


class DictionaryGUI(tk.Frame):
    def __init__(self, parent, database):
        self.dictionary = Dictionary(database)
        self.database = database
        tk.Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def create_frame(self, master):
        new_frame = tk.Frame(master)
        new_frame.pack(fill=tk.X)

        return new_frame

    def create_pack_button(self, master, text, command, width=0, center=0):
        w = max(len(text), width)
        new_button = tk.Button(master, text=text, command=command, width=w)

        if center is 0:
            new_button.pack(side=tk.LEFT, padx=10, pady=10)
        else:
            new_button.pack()

        return new_button

    def create_grid_button(self, master, text, command, row, column,
                           sticky=tk.W+tk.E+tk.S+tk.N):
        new_button = tk.Button(master, text=text, command=command)
        new_button.grid(row=row, column=column, sticky=sticky, padx=10,
                        pady=10)

        return new_button

    def create_window(self, master, title, width, height):
        child = tk.Toplevel(master)
        child.wm_title(title)
        child.geometry("{}x{}+500+500".format(width, height))
        child.resizable(0, 0)

        return child

    def create_pack_label(self, master, text, padx=0, pady=0):
        new_label = tk.Label(master, text=text)
        new_label.pack(side="left", padx=padx, pady=pady)

        return new_label

    def create_pack_label_with_stringvar(self, master, padx=0, text=0):
        label_content = tk.StringVar()
        if text is not 0:
            label_content.set(text)

        new_label = tk.Label(master, textvariable=label_content,
                             justify=tk.LEFT)
        new_label.pack(side="left", padx=padx)

        return (new_label, label_content)

    def create_grid_label(self, master, text, row, column,
                          sticky=tk.W+tk.E+tk.S+tk.N):
        new_label = tk.Label(master, text=text)
        new_label.grid(row=row, column=column, sticky=sticky)

        return new_label

    def create_pack_entry(self, master):
        new_entry = tk.Entry(master)
        new_entry.pack(side="left")

        return new_entry

    def create_pack_entry_with_stringvar(self, master):
        entry_content = tk.StringVar()
        new_entry = tk.Entry(master, textvariable=entry_content)
        new_entry.pack(side="left")

        return (new_entry, entry_content)

    def create_grid_entry(self, master, row, column,
                          sticky=tk.W+tk.E+tk.S+tk.N):
        new_entry = tk.Entry(master)
        new_entry.grid(row=row, column=column, sticky=sticky)

        return new_entry

    def create_grid_entry_with_stringvar(self, master, row, column,
                                         sticky=tk.W+tk.E+tk.S+tk.N):
        entry_content = tk.StringVar()
        new_entry = tk.Entry(master, textvariable=entry_content)
        new_entry.grid(row=row, column=column, sticky=sticky)

        return (new_entry, entry_content)

    def initUI(self):
        self.parent.title("German Dictionary")
        self.pack(fill=tk.BOTH, expand=True)
        '''
        upper_frame = self.create_frame(self)

        self.create_pack_button(upper_frame, "View word",
                                self.extract_entry_click)

        self.create_pack_button(upper_frame, "Add word", self.add_word_click)

        self.create_pack_button(upper_frame, "Delete word",
                                self.delete_entry_click)

        self.create_pack_button(upper_frame, "View words with meaning",
                                self.extract_with_meaning_click)

        self.create_pack_button(upper_frame, "Edit entry",
                                self.edit_entry_click)

        lower_frame = self.create_frame(self)

        self.create_pack_button(lower_frame, "Meaning quiz",
                                self.quiz_meaning_click, 0, 1)

        self.create_pack_button(lower_frame, "Nouns quiz",
                                self.quiz_nouns_click, 0, 1)

        self.create_pack_button(lower_frame, "Verbs quiz",
                                self.quiz_verbs_click, 0, 1)
        '''
        self.create_grid_button(self, "View word",
                                self.extract_entry_click, 0, 0)

        self.create_grid_button(self, "Add word", self.add_word_click, 0, 1)

        self.create_grid_button(self, "Delete word",
                                self.delete_entry_click, 0, 2)

        self.create_grid_button(self, "View words with meaning",
                                self.extract_with_meaning_click, 0, 3)

        self.create_grid_button(self, "Edit entry",
                                self.edit_entry_click, 0, 4)

        self.create_grid_button(self, "Meaning quiz",
                                self.quiz_meaning_click, 1, 1)

        self.create_grid_button(self, "Nouns quiz",
                                self.quiz_nouns_click, 1, 2)

        self.create_grid_button(self, "Verbs quiz",
                                self.quiz_verbs_click, 1, 3)

    def extract_entry_click(self):
        child = self.create_window(self, "Extract word", 400, 300)

        query_frame = self.create_frame(child)

        query_label = self.create_pack_label(query_frame,
                                             "Enter word to extract", 10)

        self.query_entry, self.query_content = self.\
            create_pack_entry_with_stringvar(query_frame)

        go_button = self.create_pack_button(query_frame, "Go",
                                            self.extract_entry_go_click)

        text_frame = self.create_frame(child)

        extract_results, self.results_var = self.\
            create_pack_label_with_stringvar(text_frame, 10)

    def extract_entry_go_click(self):
        desired_word = self.query_entry.get()

        try:
            extracted_word = self.dictionary.extract_entry(desired_word)
        except DatabaseError:
            self.results_var.set("")
            mbox.showerror("Word not found", "The word {} was not found.".
                           format(desired_word))
            self.query_content.set("")
        else:
            self.results_var.set(extracted_word)

    def add_word_click(self):
        self.child = self.create_window(self, "Add word", 450, 350)

        self.create_grid_label(self.child, "Enter word to add: ", 0, 0)

        self.new_word = self.create_grid_entry(self.child, 0, 1, tk.E+tk.W)

        self.word_type = tk.Listbox(self.child, height=3)
        self.word_type.grid(row=0, column=2)

        for item in ("Noun", "Verb", "Adjective"):
            self.word_type.insert(tk.END, item)

        self.create_grid_button(self.child, "Go", self.add_word_go_click, 0, 3,
                                tk.E+tk.W)

    def add_word_go_click(self):
        desired_word = self.new_word.get()

        if(self.dictionary.exists_entry(desired_word)):
            mbox.showerror("Word already added",
                           "The word {} has been already added {}".
                           format(desired_word, 'to the database.'))
        else:
            index = self.word_type.curselection()[0]
            selected_word_type = self.word_type.get(index)
            self.class_name = getattr(sys.modules[__name__],
                                      selected_word_type)
            self.fields = self.class_name.fields()[1:]

            self.create_add_word_field_widgets()

    def create_add_word_field_widgets(self):
        row = 1
        self.entry_fields = []
        for field in self.fields[:-1]:
            self.create_grid_label(self.child, field, row, 0, tk.W)
            new_entry = self.create_grid_entry(self.child, row, 1)

            self.entry_fields.append(new_entry)
            row = row + 1

        self.create_grid_label(self.child, "Examples", row, 0, tk.W+tk.N)

        meaning = tk.Text(self.child, width=15, height=3)
        meaning.grid(row=row, column=1)
        self.entry_fields.append(meaning)

        self.create_grid_button(self.child, "Add entry",
                                self.add_entry_button_click, row + 1, 1)

    def add_entry_button_click(self):
        word_hash = {}
        word_hash["Entry"] = self.new_word.get()

        for index, field in enumerate(self.fields[:-1]):
            word_hash[field] = self.entry_fields[index].get()

        word_hash["Examples"] = self.entry_fields[-1].get("1.0", tk.END)

        new_entry = self.class_name(word_hash)
        self.dictionary.add_entry(new_entry)

        mbox.showinfo("Word successfully added",
                      "The word {} has been successfully added {}".
                      format(word_hash["Entry"], 'to the database.'))
        self.clear_add_entry_fields()

    def clear_entry_fields(self):
        for row in self.child.grid_slaves():
            if int(row.grid_info()["row"]) > 0:
                row.grid_forget()

    def delete_entry_click(self):
        child = self.create_window(self, "Delete word", 450, 200)

        frame = self.create_frame(child)

        self.create_pack_label(frame, "Enter word to delete:", 10)

        self.delete_entry, self.entry_content = self.\
            create_pack_entry_with_stringvar(frame)

        self.create_pack_button(frame, "Go", self.delete_entry_go_click)

    def delete_entry_go_click(self):
        word_to_delete = self.delete_entry.get()

        if not self.dictionary.exists_entry(word_to_delete):
            mbox.showerror("Word not found",
                           "The word {} has not been found.".
                           format(word_to_delete))
        else:
            self.dictionary.delete_entry(word_to_delete)
            mbox.showinfo("Word successfully deleted",
                          ("The word {} has been successfully deleted"
                           " from the database.".format(word_to_delete)))

        self.entry_content.set("")

    def extract_with_meaning_click(self):
        child = self.create_window(self, "Extract with meaning", 450, 340)

        frame = self.create_frame(child)

        self.create_pack_label(frame, "Enter meaning:", 10, 10)

        self.meaning_entry, self.entry_content = self.\
            create_pack_entry_with_stringvar(frame)

        self.create_pack_button(frame, "Go",
                                self.extract_with_meaning_go_click)

        result_frame = self.create_frame(child)

        result_label, self.result_content = self.\
            create_pack_label_with_stringvar(result_frame)

    def extract_with_meaning_go_click(self):
        meaning = self.meaning_entry.get()

        found_words = self.dictionary.extract_entries_with_meaning(meaning)
        if len(found_words) == 0:
            mbox.showerror("No words found",
                           ("No words containing the meaning '{}' "
                            "have been found.".format(meaning)))
            self.result_content.set("")
        else:
            self.result_content.set("\n\n".join(map(str, found_words)))

    def edit_entry_click(self):
        self.child = self.create_window(self, "Edit entry", 450, 340)

        self.create_grid_label(self.child, "Enter word to edit:", 0, 0, tk.W)

        self.edit_word_entry, self.entry_content = self.\
            create_grid_entry_with_stringvar(self.child, 0, 1, tk.W)

        self.create_grid_button(self.child, "Go", self.edit_entry_go_click,
                                0, 2, tk.W)

    def edit_entry_go_click(self):
        desired_word = self.edit_word_entry.get()

        if not self.dictionary.exists_entry(desired_word):
            mbox.showerror("No word found",
                           "The word '{}' has not been found.".
                           format(desired_word))
            self.entry_content.set("")
        else:
            self.found_word = self.dictionary.extract_entry(desired_word)
            self.fields = self.found_word.__class__.fields()

            self.create_grid_label(self.child, "Choose field to edit:", 1, 0,
                                   tk.N+tk.W)

            self.fields_to_edit = tk.Listbox(self.child,
                                             height=len(self.fields))
            for field in self.fields:
                self.fields_to_edit.insert(tk.END, field)
            self.fields_to_edit.grid(row=1, column=1, sticky=tk.W)

            self.create_grid_button(self.child, "Edit",
                                    self.edit_entry_edit_click, 1, 2, tk.W)

    def edit_entry_edit_click(self):
        index = self.fields_to_edit.curselection()[0]
        self.selected_field = self.fields_to_edit.get(index)

        original_field_data = self.found_word.word_hash[self.selected_field]

        self.create_grid_label(self.child, "Edit chosen field:",
                               1 + len(self.fields), 0, tk.W)

        self.new_field_data = self.create_grid_entry(self.child,
                                                     1 + len(self.fields),
                                                     1, tk.W)
        self.new_field_data.insert(tk.END, original_field_data)

        self.create_grid_button(self.child, "Save changes",
                                self.edit_entry_save_click,
                                1 + len(self.fields), 2, tk.W)

    def edit_entry_save_click(self):
        new_field_data_content = self.new_field_data.get()

        self.dictionary.edit_entry(self.found_word.word_hash['Entry'],
                                   self.selected_field, new_field_data_content)

        mbox.showinfo("Entry successfully edited",
                      "Entry {} has been successfully edited".
                      format(self.found_word.word_hash['Entry']))

        self.clear_entry_fields()

    def quiz_meaning_click(self):
        self.quiz_template_click(['Nouns', 'Adjectives', 'Verbs'], ['Meaning'])

    def quiz_nouns_click(self):
        self.quiz_template_click(['Nouns'], ['Gender', 'Plural'])

    def quiz_verbs_click(self):
        self.quiz_template_click(['Verbs'], ['Forms'])

    def quiz_template_click(self, parts_of_speech, fields):
        self.child = self.create_window(self, "", 450, 340)

        self.parts_of_speech = parts_of_speech
        self.fields = fields
        self.started = False

        top_frame = self.create_frame(self.child)

        self.create_pack_button(top_frame, "Start", self.start_click, 15, 1)
        self.create_pack_button(top_frame, "Finish", self.finish_click, 15, 1)

    def start_click(self):
        if not self.started:
            self.started = True
            self.quiz = Quiz(self.database, self.parts_of_speech, self.fields)
            self.score_frame = self.create_frame(self.child)

            self.score_info, self.score = self.\
                create_pack_label_with_stringvar(self.score_frame, 0,
                    'Score: {}'.format(self.quiz.score))

            self.word_frame = self.create_frame(self.child)

            current_entry = self.quiz.current_word.word_hash['Entry']
            self.word_label, self.current_word = self.\
                create_pack_label_with_stringvar(self.word_frame, 0,
                    'Current word: {}'.format(current_entry))

            self.create_quiz_field_widgets()

            self.go_frame = self.create_frame(self.child)

            self.create_pack_button(self.go_frame, 'Check',
                                    self.check_click, 15, 1)

    def create_quiz_field_widgets(self):
        self.field_entries = []
        self.field_frames = []

        for field in self.fields:
            new_field_frame = self.create_frame(self.child)
            self.field_frames.append(new_field_frame)

            self.create_pack_label(new_field_frame, '{}: '.format(field))

            new_entry = self.create_pack_entry(new_field_frame)
            self.field_entries.append(new_entry)

    def finish_click(self):
        mbox.showinfo("Quiz finished", "Quiz finished, your score is {}".
                      format("%.2f" % (self.quiz.score * 100)))
        self.started = False

        self.score_frame.pack_forget()
        self.word_frame.pack_forget()
        for field_frame in self.field_frames:
            field_frame.pack_forget()
        self.go_frame.pack_forget()

    def check_click(self):
        suggestions = []
        for index, field in enumerate(self.fields):
            suggestions.append(self.field_entries[index].get())

        guess_results = self.quiz.guess(suggestions)
        answer_statement = self.quiz.answer_statements(guess_results)

        mbox.showinfo("", "{}".format(answer_statement))

        if len(self.quiz.words_to_guess) > 0:
            self.update_quiz_fields()
        else:
            self.finish_button_click()

    def update_quiz_fields(self):
        current_entry = self.quiz.current_word.word_hash['Entry']
        self.score.set('Score: {}%'.format("%.2f" % (self.quiz.score * 100)))
        self.current_word.set('Current word: {}'.format(current_entry))

        for field_entry in self.field_entries:
            field_entry.delete(0, 'end')


def main():
    root = tk.Tk()
    app = DictionaryGUI(root, './data/words.db')
    root.mainloop()


if __name__ == '__main__':
    main()
