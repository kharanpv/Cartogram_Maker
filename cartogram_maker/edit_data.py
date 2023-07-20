import customtkinter as ctk
from CTkTable import *

class edit_data(ctk.CTkFrame):
    def __init__(self, master, project_name):
        super().__init__(master, fg_color="#EBEBEB")  # Create a frame inside the application window

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.values = [["Name","Data 1"],
                       [project_name,""]]
        self.table = CTkTable(master=self, row=2, column=2, values=self.values)
        self.table.grid(row=0, column=0, sticky="nsew")

        