import customtkinter as ctk
from CTkTable import *


class EditData(ctk.CTkFrame):
    def __init__(self, master, project_name):
        super().__init__(
            master, fg_color="#EBEBEB"
        )  # Create a frame inside the application window

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #starting values
        self.values = [["Name", "Data 1"], [project_name, ""]]
        self.rows = 2 
        self.columns = 2

        self.table = CTkTable(
            master=self, row=self.rows, column=self.columns, values=self.values, corner_radius=2, write=1
        )
        self.table.grid(row=0, column=0, sticky="nsew")

        self.row_add_button = ctk.CTkButton(self, text="+", command= lambda: self.row_remove('+'), width=40, fg_color="lightgray", 
                                            text_color="black", font=("Arial", 30), corner_radius=2, hover_color="darkgray",)
        self.row_add_button.grid(row=1, column=0, padx=(0, 50), pady=(5, 0), sticky="se")

        self.row_remove_button = ctk.CTkButton(self, text="-", command= lambda: self.row_remove('-'), width=40, fg_color="lightgray",
                                            text_color="black", font=("Arial", 30), corner_radius=2, hover_color="darkgray",)
        self.row_remove_button.grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="se")

        # ---For future implementation---
        # self.column_add_button = ctk.CTkButton(self, text="+", command= lambda: self.column_remove('+'), width=40, fg_color="lightgray", 
        #                                     text_color="black", font=("Arial", 30), corner_radius=2, hover_color="darkgray",)
        # self.column_add_button.grid(row=0, column=1, padx=(5, 0), pady=(0, 5), sticky="se")

        # self.column_remove_button = ctk.CTkButton(self, text="-", command= lambda: self.column_remove('-'), width=40, fg_color="lightgray",
        #                                     text_color="black", font=("Arial", 30), corner_radius=2, hover_color="darkgray",)
        # self.column_remove_button.grid(row=0, column=1, padx=(5, 0), pady=(0, 50), sticky="se")

        self.done_button = ctk.CTkButton(self, text="Done", command=self.on_done_click)
        self.done_button.grid(row=2, column=1, padx=10, pady=10, sticky="se")

        self.back_button = ctk.CTkButton(
            self, text="Go Back", command=self.on_back_click, fg_color="red"
        )
        self.back_button.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

    def on_done_click(self):  # TODO: Save the data to the json file
        from .start_frame import StartFrame

        self.master.change_frame(StartFrame)

    def on_back_click(self):
        from .start_frame import StartFrame

        self.master.change_frame(StartFrame)

    def row_remove(self, sign):
        if sign == '+': # add new row
            self.table.add_row(["", ""])
            self.rows += 1
        elif sign == '-': # remove last row
            self.table.delete_row(self.rows - 1)
            self.rows -= 1
    
    # ---For future implementation---
    # def column_remove(self, sign):
    #     if sign == '+': # add new column
    #         self.table.add_column([""])
    #         self.columns += 1
    #     elif sign == '-': # remove last column
    #         self.table.delete_column(self.columns - 1)
    #         self.columns -= 1