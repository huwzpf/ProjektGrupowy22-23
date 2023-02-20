import tkinter as tk
from playsound import playsound


class ListBoxWithButton(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.listbox.yview)

        self.buttons = {}

    def insert(self, index, name, audio_path):
        self.listbox.insert(index, name)

        button = tk.Button(self.listbox, text="Odsłuchaj", command=lambda idx=index: self.listen(audio_path))
        self.buttons[index] = button

        self.listbox.window_create(index, window=button)

    def listen(self, audio_path):
        playsound(audio_path)