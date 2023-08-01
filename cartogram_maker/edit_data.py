import customtkinter as ctk
import os
from json import load
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

        # starting values
        self.values = [["Name", "Weight"]]
        self.rows = 1
        self.columns = 2

        self.project_name = project_name

        self.table = CTkTable(
            master=self,
            row=self.rows,
            column=self.columns,
            values=self.values,
            corner_radius=2,
            write=1,
        )
        self.table.grid(row=0, column=0, sticky="nsew")

        self.row_add_button = ctk.CTkButton(
            self,
            text="+",
            command=lambda: self.row_remove("+"),
            width=40,
            fg_color="lightgray",
            text_color="black",
            font=("Arial", 30),
            corner_radius=2,
            hover_color="darkgray",
        )
        self.row_add_button.grid(
            row=1, column=0, padx=(0, 50), pady=(5, 0), sticky="se"
        )

        self.row_remove_button = ctk.CTkButton(
            self,
            text="-",
            command=lambda: self.row_remove("-"),
            width=40,
            fg_color="lightgray",
            text_color="black",
            font=("Arial", 30),
            corner_radius=2,
            hover_color="darkgray",
        )
        self.row_remove_button.grid(
            row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="se"
        )

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

        self.generate_button = ctk.CTkButton(self, text="Generate", command=self.generate)
        self.generate_button.grid(row=2, column=2, padx=10, pady=10, sticky="se")

    def on_done_click(self):
        from .start_frame import StartFrame
        import os
        import json

        folder_path = os.path.join("projects", self.project_name)

        with open(folder_path) as project_file:
            project_json = load(project_file)
            project_json = list(project_json.items())

            table = self.table.get()
            for i in range(1, self.rows):
                key, values = project_json[i - 1]
                values["name"] = table[i][0]
                values["weight"] = float(table[i][1])

        json.dump(dict(project_json), open(folder_path, "w"))

        self.master.change_frame(StartFrame)

    def on_back_click(self):
        from json import load
        from .view_frame import ViewFrame

        def update_frame(json):
            return lambda frame: frame.set_list_of_polygons(json)

        folder_path = os.path.join("projects", self.project_name)

        if os.path.getsize(folder_path) != 0:
            with open(folder_path) as project_file:
                project_json = load(project_file)
                self.destroy()
                view_frame_partial = lambda new_master: ViewFrame(
                    master=new_master, project_name=self.project_name
                )
                self.master.change_frame(
                    view_frame_partial, then_run=update_frame(project_json)
                )
        else:
            print(f"{self.project_name} is empty")

    def row_remove(self, sign):
        if sign == "+":  # add new row
            self.table.add_row(["", ""])
            self.rows += 1
        elif sign == "-":  # remove last row
            if self.rows > 1:
                self.table.delete_row(self.rows - 1)
                self.rows -= 1

    def update_table(self, project_name):
        folder_path = os.path.join("projects", project_name)

        if os.path.getsize(folder_path) != 0:
            with open(folder_path) as project_file:
                project_json = load(project_file)

                for _, values in project_json.items():
                    weight = values["weight"]
                    name = values["name"]
                    self.table.add_row([name, weight])
                    self.rows += 1
        else:
            self.table.add_row(["", ""])
            self.rows += 1

    def generate(self):  # placeholder for future Generate button functionality
        def color_tuple_to_hex(color: tuple[int, int, int]) -> str:
            # since we know that PIL will give a valid color, we can forego clamping these values
            return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}".upper()

        from .start_frame import json_to_image
        from .generate import cartogram
        import numpy as np
        import os
        import json

        folder_path = os.path.join("projects", self.project_name)

        with open(folder_path) as project_file:
            project_json = load(project_file)
            project_json = list(project_json.items())

            table = self.table.get()
            for i in range(1, self.rows):
                key, values = project_json[i - 1]
                values["name"] = table[i][0]
                values["weight"] = float(table[i][1])

        json.dump(dict(project_json), open(folder_path, "w"))

        folder_path = os.path.join("projects", self.project_name)

        if os.path.getsize(folder_path) != 0:
            with open(folder_path) as project_file:
                image = load(project_file)

        # image = self.canvas_frame.get_list_of_polygons()
        color_to_weight = {
            substructure["color"]: substructure["weight"]
            for _, substructure in image.items()
        }
        weight_average = sum(v for _, v in color_to_weight.items()) / len(
            color_to_weight
        )
        im = json_to_image(image)

        w, h = im.width, im.height

        print(f"{w}, {h}")

        z = np.zeros((h, w))

        print(color_to_weight)

        for i in range(w):
            for j in range(h):
                hex_color = color_tuple_to_hex(pc := im.getpixel((i, j)))
                z[j, i] = color_to_weight.get(hex_color, weight_average)

        im = cartogram(im, z)

        im.show()

    # ---For future implementation---
    # def column_remove(self, sign):
    #     if sign == '+': # add new column
    #         self.table.add_column([""])
    #         self.columns += 1
    #     elif sign == '-': # remove last column
    #         self.table.delete_column(self.columns - 1)
    #         self.columns -= 1
