import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import shutil, os
from pathlib import Path

class Application(tk.Frame):
    split_limit = 2
    working_dir = ""

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        self.open_dir = tk.Button(self)
        self.open_dir["text"] = "Open directory"
        self.open_dir["command"] = self.open_directory_browser
        self.open_dir.pack(side="top")

        self.limit_setter = tk.Button(self)
        self.limit_setter["text"] = "Current limit: " + str(self.split_limit)
        self.limit_setter["command"] = self.open_limit_settings
        self.limit_setter.pack(side="top")

        self.sort_into_directories = tk.Button(self)
        self.sort_into_directories["text"] = "SORT!"
        self.sort_into_directories["command"] = self.sort
        self.sort_into_directories.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def open_directory_browser(self):
        target_dir = filedialog.askdirectory(mustexist=True, initialdir=self.working_dir)

        if target_dir != "":
            self.working_dir = target_dir
            self.open_dir["text"] = "Opened directory: \n" + self.working_dir
        elif self.working_dir != "":
            self.open_dir["text"] = "Open directory"

    def open_limit_settings(self):
        new_limit = simpledialog.askinteger("Input", "Enter new split limit", parent=root, minvalue=1, maxvalue=50)
        if new_limit is not None:
            self.split_limit = new_limit
            self.limit_setter["text"] = "Current limit: " + str(self.split_limit)
        else:
            messagebox.showwarning("Invalid value entered")

    def sort(self):
        if self.working_dir != "":
            with os.scandir(self.working_dir) as entries:
                current_directory_index = 0
                moved_files = 0
                working_path = Path(self.working_dir)
                for index, entry in enumerate(entries):
                    target_directory = Path(working_path / str(current_directory_index))

                    if target_directory.exists() is not True:
                        os.mkdir(os.path.join(working_path, str(current_directory_index)))

                    if entry.is_file():
                        shutil.move(entry.path, os.path.join(target_directory, entry.name))
                        moved_files += 1
                        if index % self.split_limit - 1 == 0 and index != 0:
                            current_directory_index += 1

            success_message = "Successfully moved: " + str(moved_files) + " files!"
            messagebox.showinfo(title="Finished", message=success_message)
        else:
            messagebox.showinfo(title="Notice!", message="No path selected!")
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()