import customtkinter as ctk
from CTkTable import *

class edit_data(ctk.CTkFrame):

    def __init__(self, master, project_name):
        super().__init__(master, fg_color="#EBEBEB")  # Create a frame inside the application window

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.values = [["Name","Data 1"],
                       [project_name,""]]
        self.table = CTkTable(master=self, row=2, column=2, values=self.values, corner_radius=2, write=1)
        self.table.grid(row=0, column=0, sticky="nsew")

        self.done_button = ctk.CTkButton(self, text="Done", command=self.on_done_click)
        self.done_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        self.back_button = ctk.CTkButton(self, text="Go Back", command=self.on_back_click, fg_color="red")
        self.back_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

    def on_done_click(self): #TODO: Save the data to the json file
        from .start_frame import start_frame
        self.master.change_frame(start_frame)

        print("[DEBUG]: Done button pressed")
    
    def on_back_click(self):
        from .start_frame import start_frame
        self.master.change_frame(start_frame)

        print("[DEBUG]: Go Back button pressed")
