import tkinter as tk
import tkinter.messagebox as mbox
from dictionary import *
from db_handler import DatabaseError
import sys


class DictionaryGUI(tk.Frame):
    def __init__(self, parent, database):
        self.dictionary = Dictionary(database)
        tk.Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("German Dictionary")
        self.pack(fill=tk.BOTH, expand=True)
        
        upper_frame = tk.Frame(self)
        upper_frame.pack(fill=tk.X)

        extract_entry_button = tk.Button(upper_frame, text="View word",
            command=self.extract_entry_click)
        extract_entry_button.pack(side=tk.LEFT, padx=10, pady=10)

        add_word_button = tk.Button(upper_frame, text="Add word",
            command=self.add_word_click)
        add_word_button.pack(side=tk.LEFT, padx=10, pady=10)

        delete_entry_button = tk.Button(upper_frame, text="Delete word",
            command=self.delete_entry_click)
        delete_entry_button.pack(side=tk.LEFT, padx=10, pady=10)

        extract_with_meaning_button = tk.Button(upper_frame,
            text="View words with meaning",
            command=self.extract_with_meaning_click)
        extract_with_meaning_button.pack(side=tk.LEFT, padx=10, pady=10)

        edit_entry_button = tk.Button(upper_frame, text="Edit entry",
            command=self.edit_entry_click)
        edit_entry_button.pack(side=tk.LEFT, padx=10, pady=10)

    def extract_entry_click(self):
        child = tk.Toplevel(self)
        child.wm_title("View word")
        child.geometry("400x300+500+500")
        child.resizable(0, 0)

        frame = tk.Frame(child)
        frame.pack(fill=tk.X)

        label = tk.Label(frame, text="Enter word to extract:")
        label.pack(side="left", fill="both", padx=10)

        self.text_box = tk.Entry(frame)
        self.text_box.pack(side="left")

        go_button = tk.Button(frame, text="Go", 
            command=self.extract_entry_go_click)
        go_button.pack(side="left")

        text_frame = tk.Frame(child)
        text_frame.pack(fill=tk.X)

        self.word_info = tk.StringVar()
        word_info_text = tk.Label(text_frame, textvariable=self.word_info,
            justify=tk.LEFT)
        word_info_text.pack(side="left", padx=10)

        child.mainloop()

    def extract_entry_go_click(self):
        desired_word = self.text_box.get()

        try:
            extracted_word = self.dictionary.extract_entry(desired_word)
        except DatabaseError:
            self.word_info.set("")
            mbox.showerror("Word not found", "The word {} was not found.".\
                format(desired_word))
        else:
            self.word_info.set(extracted_word)

    def add_word_click(self):
        self.child = tk.Toplevel(self)
        self.child.wm_title("Add word")
        self.child.geometry("450x340+500+500")
        self.child.resizable(0, 0)

        label = tk.Label(self.child, text="Enter word to add:")
        label.grid(row=0, column=0, padx=10)

        self.new_word = tk.Entry(self.child)
        self.new_word.grid(row=0, column=1)

        self.word_type = tk.Listbox(self.child, height=3)
        self.word_type.grid(row=0, column=2)

        for item in ("Noun", "Verb", "Adjective"):
            self.word_type.insert(tk.END, item)

        go_button = tk.Button(self.child, text="Go",
            command=self.add_word_go_click)
        go_button.grid(row=0, column=3)

        self.child.mainloop()

    def add_word_go_click(self):
        desired_word = self.new_word.get()

        if(self.dictionary.exists_entry(desired_word)):
            mbox.showerror("Word already added", 
                "The word {} has been already added to the database.".\
                format(desired_word))
        else:
            index = self.word_type.curselection()[0]
            selected_word_type = self.word_type.get(index)
            self.class_name = getattr(sys.modules[__name__], selected_word_type)
            self.fields = self.class_name.fields()[1:]

            row = 1
            self.entry_fields = []
            for field in self.fields[:-1]:
                tk.Label(self.child, text=field).grid(row=row, column=0, 
                                                      sticky=tk.W)
                new_entry = tk.Entry(self.child)
                self.entry_fields.append(new_entry)
                new_entry.grid(row=row, column=1)
                row = row + 1

            tk.Label(self.child, text="Examples").grid(row=row, column=0,
                                                       sticky=tk.W+tk.N)
            meaning = tk.Text(self.child, width=15, height=3)
            meaning.grid(row=row, column=1)
            self.entry_fields.append(meaning)

            add_entry_button = tk.Button(self.child, text="Add entry",
                width=15, command=self.add_entry_button_click)
            add_entry_button.grid(row=row + 1, column=1)

    def add_entry_button_click(self):
        word_hash = {}
        word_hash["Entry"] = self.new_word.get()

        for index, field in enumerate(self.fields[:-1]):
            word_hash[field] = self.entry_fields[index].get()

        word_hash["Examples"] = self.entry_fields[-1].get("1.0", tk.END)

        new_entry = self.class_name(word_hash)
        self.dictionary.add_entry(new_entry)

        mbox.showinfo("Word successfully added", 
                "The word {} has been successfully added to the database.".\
                format(word_hash["Entry"]))

    def delete_entry_click(self):
        child = tk.Toplevel(self)
        child.wm_title("Delete word")
        child.geometry("450x200+500+500")
        child.resizable(0, 0)

        frame = tk.Frame(child)
        frame.pack(fill=tk.X)

        label = tk.Label(frame, text="Enter word to delete:", padx=10, 
                         pady=10)
        label.pack(side="left")

        self.entry_content = tk.StringVar()
        self.delete_entry_field = tk.Entry(frame, 
            textvariable=self.entry_content)
        self.delete_entry_field.pack(side="left")

        go_button = tk.Button(frame, text="Go",
                              command=self.delete_entry_go_click)
        go_button.pack(side="left")

        child.mainloop()

    def delete_entry_go_click(self):
        word_to_delete = self.delete_entry_field.get()

        if not self.dictionary.exists_entry(word_to_delete):
            mbox.showerror("Word not found", 
                "The word {} has not been found.".format(word_to_delete))
        else:
            self.dictionary.delete_entry(word_to_delete)
            mbox.showinfo("Word successfully deleted", 
                ("The word {} has been successfully deleted"
                 " from the database.".\
                format(word_to_delete)))

        self.entry_content.set("")

    def extract_with_meaning_click(self):
        child = tk.Toplevel(self)
        child.wm_title("Delete word")
        child.geometry("450x340+500+500")
        child.resizable(0, 0)

        frame = tk.Frame(child)
        frame.pack(fill=tk.X)

        label = tk.Label(frame, text="Enter meaning:", padx=10, 
                         pady=10)
        label.pack(side="left")

        self.entry_content = tk.StringVar()
        self.delete_entry_field = tk.Entry(frame, 
            textvariable=self.entry_content)
        self.delete_entry_field.pack(side="left")

        go_button = tk.Button(frame, text="Go",
                              command=self.extract_with_meaning_go_click)
        go_button.pack(side="left")

        result_frame = tk.Frame(child)
        result_frame.pack(fill=tk.X)

        self.result_content = tk.StringVar()
        result_label = tk.Label(result_frame, justify="left",
            textvariable=self.result_content)
        result_label.pack(side="left")

        child.mainloop()

    def extract_with_meaning_go_click(self):
        meaning = self.delete_entry_field.get()

        found_words = self.dictionary.extract_entries_with_meaning(meaning)
        if len(found_words) == 0:
            mbox.showerror("No words found", 
                "No words containing the meaning '{}' have been found.".\
                format(meaning))
            self.result_content.set("")
        else:
            self.result_content.set("\n\n".join(map(str, found_words)))

    def edit_entry_click(self):
        self.child = tk.Toplevel(self)
        self.child.wm_title("Delete word")
        self.child.geometry("450x340+500+500")
        self.child.resizable(0, 0)

        label = tk.Label(self.child, text="Enter word to edit:", padx=10,
                         pady=10)
        label.grid(row=0, column=0, sticky=tk.W)

        self.entry_content = tk.StringVar()
        self.edit_word_field = tk.Entry(self.child, 
            textvariable=self.entry_content)
        self.edit_word_field.grid(row=0, column=1, sticky=tk.W)

        go_button = tk.Button(self.child, text="Go",
                              command=self.edit_entry_go_click)
        go_button.grid(row=0, column=2, sticky=tk.W)

    def edit_entry_go_click(self):
        desired_word = self.edit_word_field.get()

        if not self.dictionary.exists_entry(desired_word):
            mbox.showerror("No word found", 
                "The word '{}' has not been found.".format(desired_word))
            self.result_content.set("")
        else:
            self.found_word = self.dictionary.extract_entry(desired_word)
            self.fields = self.found_word.__class__.fields()

            tk.Label(self.child, text="Choose field to edit:", padx=10,
                pady=10).grid(row=1, column=0, sticky=tk.N+tk.W)

            self.fields_to_edit = tk.Listbox(self.child, height=len(self.fields))
            for field in self.fields:
                self.fields_to_edit.insert(tk.END, field)
            self.fields_to_edit.grid(row=1, column=1, sticky=tk.W)

            edit_button = tk.Button(self.child, text="Edit",
                command=self.edit_entry_edit_click)
            edit_button.grid(row=1, column=2, sticky=tk.W)

    def edit_entry_edit_click(self):
        index = self.fields_to_edit.curselection()[0]
        self.selected_field = self.fields_to_edit.get(index)

        original_field_data = self.found_word.word_hash[self.selected_field]

        tk.Label(self.child, text="Edit chosen field:", padx=10, pady=10).\
            grid(row=1 + len(self.fields), column=0,sticky=tk.W)

        self.new_field_data = tk.Entry(self.child, 
            textvariable=original_field_data)
        self.new_field_data.grid(row=1 + len(self.fields), column=1,
            sticky=tk.W)

        save_changes_button = tk.Button(self.child, text="Save changes",
            command=self.edit_entry_save_click)
        save_changes_button.grid(row=1 + len(self.fields), column=2,
            sticky=tk.W)

    def edit_entry_save_click(self):
        new_field_data_content = self.new_field_data.get()

        self.dictionary.edit_entry(self.found_word.word_hash['Entry'],
            self.selected_field, new_field_data_content)

        mbox.showinfo("Entry successfully edited",
            "Entry {} has been successfully edited".\
            format(self.found_word.word_hash['Entry']))

    def centerWindow(self):
        w = 800
        h = 600

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    root = tk.Tk()
    app = DictionaryGUI(root, 'words.db')
    root.mainloop()


if __name__ == '__main__':
    main()