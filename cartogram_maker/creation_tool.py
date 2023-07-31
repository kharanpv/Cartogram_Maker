import customtkinter as ctk
import json
import os


class CreationTool(ctk.CTkFrame):
    def __init__(self, master):
        from .canvas_frame import CanvasFrame

        super().__init__(
            master, fg_color="#EBEBEB"
        )  # Call the parent class constructor

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )  # TODO: Figure out why adding this here makes it work

        self.canvas_frame = CanvasFrame(
            self
        )  # Create a frame inside the application window

        self.generate_button = ctk.CTkButton(
            self, text="Generate", command=self.generate
        )  # Create the Generate button
        self.generate_button.grid(
            row=1, column=0, padx=10, pady=10, sticky="se"
        )  # Position the button in the bottom right corner

        self.save_button = ctk.CTkButton(
            self, text="Save", command=self.save
        )  # Create the Save button
        self.save_button.grid(
            row=1,
            column=0,
            # CTkButton default width is 140, add 20 to account for the padx of the save button and that of the generate button
            padx=self.generate_button._current_width + 20,
            pady=10,
            sticky="se",
        )  # Position the button in the bottom center

        self.exit_button = ctk.CTkButton(
            self, text="Go Back", command=self.go_back, fg_color="red"
        )  # Create the Exit button
        self.exit_button.grid(
            row=1, column=0, padx=10, pady=10, sticky="sw"
        )  # Position the Exit button in the bottom left corner

    def generate(self):  # placeholder for future Generate button functionality
        print("[DEBUG]: Generate button pressed")

    def save(self):  # placeholder for future Save button functionality
        file_name = ctk.CTkInputDialog(
            text="Enter a file name", title="File Name"
        ).get_input()
        json.dump(
            self.canvas_frame.get_list_of_polygons(),
            open(os.path.join("projects", f"{file_name}.json"), "w"),
        )

    def go_back(self):
        from .start_frame import StartFrame

        # call main_app to change frame
        self.master.change_frame(StartFrame)

    def drag(event, canvas):  # Drag around the canvas when zooming in
        # canvas.scan_dragto(event.x, event.y, gain=1)
        print("[DEBUG]: Dragging the canvas")
