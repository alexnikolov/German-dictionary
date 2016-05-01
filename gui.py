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

        extract_entry_button = tk.Button(upper_frame, text="Extract entry",
            command=self.extract_entry_click)
        extract_entry_button.pack(side=tk.LEFT, padx=10, pady=10)

        add_word_button = tk.Button(upper_frame, text="Add word",
            command=self.add_word_click)
        add_word_button.pack(side=tk.LEFT)

    def extract_entry_click(self):
        child = tk.Toplevel(self)
        child.wm_title("Extract entry")
        child.geometry("400x300+500+500")
        child.resizable(0, 0)

        frame = tk.Frame(child)
        frame.pack(fill=tk.X)

        label = tk.Label(frame, text="Enter entry to extract:")
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