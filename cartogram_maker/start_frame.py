import customtkinter as ctk
import os
from datetime import datetime
from .cartogram_dialogbox import CartogramDialogBox
from .edit_data import EditData


class StartFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master, fg_color="#EBEBEB"
        )  # Create a frame inside the application window

        # configure the grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # create button
        self.create_button = ctk.CTkButton(
            self, text="Create", command=self.on_create_click
        )
        self.create_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # project list frame
        self.project_list = ctk.CTkFrame(self, fg_color="white")
        self.project_list.grid(row=0, column=1, padx=10, pady=10, sticky="new")

        # configure grid layout for project list
        self.project_list.grid_columnconfigure(0, weight=3)
        self.project_list.grid_columnconfigure(1, weight=2)
        self.project_list.grid_columnconfigure(2, weight=1)
        self.project_list.grid_columnconfigure(3, weight=2)

        # Table headings for the project list
        self.project_name = ctk.CTkLabel(
            self.project_list, text="Name", text_color="black"
        )
        self.project_name.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nsw")

        self.last_modified = ctk.CTkLabel(
            self.project_list, text="Last Modified", text_color="black"
        )
        self.last_modified.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="nsw")

        self.project_size = ctk.CTkLabel(
            self.project_list, text="Size", text_color="black"
        )
        self.project_size.grid(row=0, column=2, padx=10, pady=(5, 0), sticky="nsw")

        # divider line between table headings and project list
        self.divider = ctk.CTkFrame(self.project_list, fg_color="black", height=1)
        self.divider.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        # the project list is updated on demand
        self.bind("<Configure>", self.display_project_list)
        self.display_project_list()

        self.cartogram_dialogbox = None  # cartogram_dialogbox instance

    def get_project_list(self, folder_path):
        project_list = []

        # get the list of projects in the projects folder
        for file in os.listdir(folder_path):
            if file.endswith(".json"):
                project_list.append(
                    [
                        file,
                        datetime.fromtimestamp(
                            os.path.getmtime(os.path.join(folder_path, file))
                        ).replace(microsecond=0),
                        os.path.getsize(os.path.join(folder_path, file)),
                    ]
                )

        return project_list

    def display_project_list(self, event=None):
        folder_path = os.path.join("projects")
        project_list = self.get_project_list(folder_path)

        row_num = 2  # starting row number for the project list
        for project in project_list:
            # appending the project name, last modified date and size to the project list
            project_name = ctk.CTkLabel(
                self.project_list, text=project[0], text_color="black"
            )
            project_name.grid(row=row_num, column=0, padx=10, pady=(5, 0), sticky="nsw")

            project_last_modified = ctk.CTkLabel(
                self.project_list, text=project[1], text_color="black"
            )
            project_last_modified.grid(
                row=row_num, column=1, padx=10, pady=(5, 0), sticky="nsw"
            )

            project_size = ctk.CTkLabel(
                self.project_list, text=project[2], text_color="black"
            )
            project_size.grid(row=row_num, column=2, padx=10, pady=(5, 0), sticky="nsw")

            # create a frame for the buttons
            button_frame = ctk.CTkFrame(self.project_list, fg_color="transparent")
            button_frame.grid(
                row=row_num, column=3, padx=(5, 0), pady=(5, 0), sticky="nsw"
            )

            curr_project = project[0]

            # view button
            view_button = ctk.CTkButton(
                button_frame,
                text="View",
                command=self.create_on_view(curr_project),
                fg_color="transparent",
                text_color="black",
                width=30,
                hover_color="#EBEBEB",
            )
            view_button.grid(row=0, column=0, padx=(0, 5), pady=(5, 0), sticky="nsw")

            # edit button
            edit_button = ctk.CTkButton(
                button_frame,
                text="Edit",
                command=self.create_on_edit(curr_project),
                fg_color="transparent",
                text_color="black",
                width=30,
                hover_color="#EBEBEB",
            )
            edit_button.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="nsw")

            # Download button
            download_button = ctk.CTkButton(
                button_frame,
                text="Download",
                command=self.create_on_download(curr_project),
                fg_color="transparent",
                text_color="black",
                width=60,
                hover_color="#EBEBEB",
            )
            download_button.grid(
                row=0, column=2, padx=(5, 0), pady=(5, 0), sticky="nsw"
            )

            row_num += 1  # increment the row number

    def on_create_click(self):
        if (
            self.cartogram_dialogbox is None
            or not self.cartogram_dialogbox.winfo_exists()
        ):  # if cartogram_dialogbox does not exist create a new instance
            self.cartogram_dialogbox = CartogramDialogBox(self)
            self.cartogram_dialogbox.lift()  # lift the cartogram_dialogbox to the top
        else:
            self.cartogram_dialogbox.focus()  # else focus on the existing instance
            self.cartogram_dialogbox.lift()

    def create_on_view(self, name):
        return lambda: self.on_view_click(name)
    
    def create_on_edit(self, name):
        return lambda: self.on_edit_click(name)

    def create_on_download(self, name):
        return lambda: self.on_download_click(name)

    def on_edit_click(self, project_name):
        from json import load
        from .view_frame import ViewFrame
        
        def update_frame(json):
            return lambda frame: frame.set_list_of_polygons(json)
        
        folder_path = os.path.join("projects", project_name)

        if os.path.getsize(folder_path) != 0:
            with open(folder_path) as project_file:
                project_json=load(project_file)
                self.destroy()
                view_frame_partial = lambda new_master: ViewFrame(
                    master=new_master, project_name=project_name
                    )
                self.master.change_frame(view_frame_partial, then_run=update_frame(project_json))
        else:
            print(f"{project_name} is empty")

    # ---Old implementation---
    # def on_edit_click(self, project_name):
    #     edit_data_partial = lambda new_master: EditData(
    #         master=new_master, project_name=project_name
    #     )
    #     self.master.change_frame(edit_data_partial)

    def on_view_click(self, project_name):
        from json import load

        folder_path = os.path.join("projects", project_name)

        if os.path.getsize(folder_path) != 0:
            with open(folder_path) as project_file:
                project_json=load(project_file)
                im = json_to_image(project_json)
                im.show()
        else:
            print(f"{project_name} is empty")

    def on_download_click(self, project_name):
        from json import load

        folder_path = os.path.join("projects", project_name)

        if os.path.getsize(folder_path) != 0:
            with open(folder_path) as project_file:
                project_json=load(project_file)
                im = json_to_image(project_json)
                project_name_without_json = project_name.split(".")[0]
                im.save(os.path.join("downloads", f"{project_name_without_json}.png"), quality=85)
        else:
            print(f"{project_name} is empty")


def json_to_image(structure):
    from PIL import Image, ImageDraw

    im = Image.new('RGB', (800, 500), color="white")
    d = ImageDraw.Draw(im)

    for _, substructure in structure.items():
        point_buffer = substructure['vertices']

        for (x, y) in point_buffer:
            d.ellipse([(x - 2, y - 2), (x + 2, y + 2)], fill="black")

        for (x1, y1), (x2, y2) in zip(point_buffer, point_buffer[1:]):
            d.line([(x1, y1), (x2, y2)], fill="black", width=2)

        d.polygon([(x, y) for x, y in point_buffer], fill=substructure['color'], outline="black", width=2)

    return im
    
