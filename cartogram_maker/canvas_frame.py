import customtkinter as ctk
import random


def random_color():
    colors = ["#E40303", "#FF8C00", "#FFED00", "#008026", "#24408E", "#732982"]
    return random.choice(colors)


class CanvasFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master, fg_color="white"
        )  # Create a frame inside the application window

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=40, pady=(20, 0), sticky="nsew")

        self.undo_button = ctk.CTkButton(
            self,
            text="⤺",
            command=self.on_undo_click,
            width=40,
            fg_color="lightgray",
            text_color="black",
            font=("Arial", 30),
            corner_radius=2,
            hover_color="darkgray",
        )
        self.undo_button.grid(row=0, column=1, padx=(0, 5), pady=(5, 0), sticky="ne")

        self.plus_button = ctk.CTkButton(
            self,
            text="+",
            command=self.on_plus_click,
            width=40,
            fg_color="lightgray",
            text_color="black",
            font=("Arial", 30),
            corner_radius=2,
            hover_color="darkgray",
        )
        self.plus_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 50), sticky="se")

        self.minus_button = ctk.CTkButton(
            self,
            text="-",
            command=self.on_minus_click,
            width=40,
            fg_color="lightgray",
            text_color="black",
            font=("Arial", 30),
            corner_radius=2,
            hover_color="darkgray",
        )
        self.minus_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="se")

        self.point_buffer = []  # Buffer to store a pair of points
        self.polygon_list = []  # List to store all the polygons

        self.canvas = ctk.CTkCanvas(
            self, width=800, height=800, background="white", highlightthickness=0
        )  # Create a canvas inside the frame
        self.canvas.grid(
            row=0, column=0, padx=0, pady=0, sticky="nsew"
        )  # Add padding for the canvas
        self.canvas.bind("<Button-1>", self.create_click_event)

    def on_undo_click(self):
        # Handle the undo button click event
        if len(self.point_buffer) > 1:
            x1, y1 = self.point_buffer[-2]
            x2, y2 = self.point_buffer[-1]
            canvas_ids = self.canvas.find_overlapping(x1, y1, x2, y2)
            self.canvas.delete(canvas_ids[-2])  # delete the last point
            self.canvas.delete(canvas_ids[-1])  # delete the last line
            self.point_buffer.pop()  # remove the last point from the buffer

        elif len(self.point_buffer) == 1:
            x, y = self.point_buffer[-1]
            canvas_ids = self.canvas.find_overlapping(x - 2, y - 2, x + 2, y + 2)
            self.canvas.delete(canvas_ids[-1])  # delete the last point
            self.point_buffer.pop()  # remove the last point from the buffer

        elif (
            len(self.polygon_list) > 0
        ):  # If there are any polygons, delete the last one
            self.canvas.delete(self.polygon_list[-1][0])
            self.point_buffer = self.polygon_list[-1][1]
            self.polygon_list.pop()

            # delete the last point and line
            x1, y1 = self.point_buffer[-2]
            x2, y2 = self.point_buffer[-1]
            canvas_ids = self.canvas.find_overlapping(x1, y1, x2, y2)
            # self.canvas.delete(canvas_ids[-2]) #delete the last point
            self.canvas.delete(canvas_ids[-1])  # delete the last line
            self.point_buffer.pop()  # remove the last point from the buffer

        print("[DEBUG]: Undo button pressed")

    def on_plus_click(self):
        # Handle the plus button click event
        self.canvas.scale("all", 0, 0, 1.1, 1.1)  # Scale by 10%
        print("[DEBUG]: Plus button pressed")

    def on_minus_click(self):
        # Handle the minus button click event
        self.canvas.scale("all", 0, 0, 0.9, 0.9)
        print("[DEBUG]: Minus button pressed")

    # Function to handle the click event
    def create_click_event(self, event):
        self.click_event(event)

    def click_event(self, event):
        x = event.x
        y = event.y

        for i in range(
            0, len(self.point_buffer) - 1
        ):  # Check if the point is close to any of the points in the buffer
            if (
                abs(self.point_buffer[i][0] - x) < 10
                and abs(self.point_buffer[i][1] - y) < 10
            ):
                self.point_buffer.append(self.point_buffer[i])
                x1, y1 = self.point_buffer[-2]
                x2, y2 = self.point_buffer[-1]
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
                self.polygon_list.append(
                    [
                        self.canvas.create_polygon(
                            self.point_buffer, fill=random_color(), width=2
                        ),
                        self.point_buffer.copy(),
                    ]
                )  # Add the polygon to the list
                self.point_buffer.clear()
                return

        self.point_buffer.append((x, y))
        oval_id = self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
        print("[DEBUG]: ", oval_id)

        if (
            len(self.point_buffer) >= 2
        ):  # If the buffer has atleast 2 points, draw a line
            x1, y1 = self.point_buffer[-2]
            x2, y2 = self.point_buffer[-1]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
