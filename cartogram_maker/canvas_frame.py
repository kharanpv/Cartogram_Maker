import customtkinter as ctk
import random
from .point import Point


def random_color():
    colors = ["E40303", "FF8C00", "FFED00", "008026", "24408E", "732982"]
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
        self.line_buffer = {}
        self.polygon_list = []  # List to store all the polygons
        self.colors = {}
        self.weights = {}  # list to store all the weights of polygons
        self.names = {}  # list to store all the names of polygons

        self.canvas = ctk.CTkCanvas(
            self, width=800, height=800, background="white", highlightthickness=0
        )  # Create a canvas inside the frame
        self.canvas.grid(
            row=0, column=0, padx=0, pady=0, sticky="nsew"
        )  # Add padding for the canvas
        self.canvas.bind("<Button-1>", self.create_click_event)

    def get_list_of_polygons(self):
        return {
            id: {
                "color": self.colors[id],
                "vertices": [(x, y) for (x, y, _) in polygon],
                "weight": self.weights[id],
                "name": self.names[id],
            }
            for id, polygon in self.polygon_list
        }

    def set_list_of_polygons(self, structure):
        # Temporary function to draw all points as ovals on the canvas and return as a `Point`
        def func(x, y):
            # draws as oval on canvas and converts to the `Point` `NamedTuple`
            return Point(
                x, y, self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
            )

        for _, substructure in structure.items():
            # convert the vertex buffer (List[List[int]] -> List[Point])
            # also draw to canvas with `func`
            point_buffer = [func(x, y) for x, y in substructure["vertices"]]

            # zip(a, a[1:]) -> [(a[0], a[1]), (a[1], a[2]), ..., (a[n - 1], a[n])]
            for (x1, y1, id1), (x2, y2, id2) in zip(point_buffer, point_buffer[1:]):
                # creating lines from every value in the point buffer
                self.line_buffer[(id1, id2)] = self.canvas.create_line(
                    x1, y1, x2, y2, fill="black", width=2
                )

            # creating a new polygon and appending it to the polygon list
            # storing the polygon id with the walrus operator (PEP 572)
            self.polygon_list.append(
                (
                    id := self.canvas.create_polygon(
                        [(x, y) for (x, y, _) in point_buffer],
                        fill=substructure["color"],
                        width=2,
                    ),
                    point_buffer[:],
                )
            )

            # assigning the color associated to the id
            self.colors[id] = substructure["color"]
            # assigning the weight associate to the id
            self.weights[id] = substructure["weight"]
            # assigning the name associate to the id
            self.names[id] = substructure["name"]

    def generate(self):  # placeholder for future Generate button functionality
        def color_tuple_to_hex(color: tuple[int, int, int]) -> str:
            # since we know that PIL will give a valid color, we can forego clamping these values
            return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}".upper()

        from .start_frame import json_to_image
        from .generate import cartogram
        import numpy as np

        image = self.get_list_of_polygons()
        color_to_weight = {
            substructure["color"]: substructure["weight"]
            for _, substructure in image.items()
        }
        weight_average = sum(v for _, v in color_to_weight.items()) / len(
            color_to_weight
        )
        im = json_to_image(image)

        w, h = im.width, im.height

        z = np.zeros((h, w))

        for i in range(w):
            for j in range(h):
                hex_color = color_tuple_to_hex(im.getpixel((i, j)))
                z[j, i] = color_to_weight.get(hex_color, weight_average)

        im = cartogram(im, z)

        im.show()

    def on_undo_click(self):
        # Handle the undo button click event
        if len(self.point_buffer) > 1:
            *_, id1 = self.point_buffer[-2]
            *_, id2 = self.point_buffer[-1]
            self.canvas.delete(id2)  # delete the last point
            self.canvas.delete(self.line_buffer.pop((id1, id2)))  # delete the last line
            self.point_buffer.pop()  # remove the last point from the buffer

        elif len(self.point_buffer) == 1:
            *_, id = self.point_buffer[-1]
            self.canvas.delete(id)  # delete the last point
            self.point_buffer.pop()  # remove the last point from the buffer

        elif (
            len(self.polygon_list) > 0
        ):  # If there are any polygons, delete the last one
            self.canvas.delete(self.polygon_list[-1][0])
            self.point_buffer = self.polygon_list[-1][1]
            self.polygon_list.pop()

            # delete the last point and line
            *_, id1 = self.point_buffer[-2]
            *_, id2 = self.point_buffer[-1]
            self.canvas.delete(id2)  # delete the last point
            self.canvas.delete(self.line_buffer.pop((id1, id2)))  # delete the last line
            self.point_buffer.pop()  # remove the last point from the buffer

    def on_plus_click(self):
        # Handle the plus button click event
        self.canvas.scale("all", 0, 0, 1.1, 1.1)  # Scale by 10%

    def on_minus_click(self):
        # Handle the minus button click event
        self.canvas.scale("all", 0, 0, 0.9, 0.9)

    # Function to handle the click event
    def create_click_event(self, event):
        self.click_event(event)

    def click_event(self, event):
        from .polygon_input_dialog import PolygonInputDialog

        x = event.x
        y = event.y

        # Check if the point is close to any of the points in the buffer
        for i in range(0, len(self.point_buffer) - 1):
            if (
                abs(self.point_buffer[i][0] - x) < 10
                and abs(self.point_buffer[i][1] - y) < 10
            ):
                self.point_buffer.append(self.point_buffer[i])
                x1, y1, id1 = self.point_buffer[-2]
                x2, y2, id2 = self.point_buffer[-1]
                self.line_buffer[(id1, id2)] = self.canvas.create_line(
                    x1, y1, x2, y2, fill="black", width=2
                )
                dialog = PolygonInputDialog(
                    title="Polygon Data",
                    text={
                        "color": ("Fill in the Color", str),
                        "name": ("Fill in the Name", str),
                        "weight": ("Fill in the Weight", float),
                    },
                )
                dialog_result = dialog.get_input()
                self.polygon_list.append(
                    (
                        id := self.canvas.create_polygon(
                            [(x, y) for (x, y, _) in self.point_buffer],
                            fill=(color := f"#{dialog_result['color']}".upper()),
                            width=2,
                        ),
                        self.point_buffer[:],
                    )
                )  # Add the polygon to the list
                self.colors[id] = color
                self.weights[id] = dialog_result["weight"]
                self.names[id] = dialog_result["name"]

                self.point_buffer.clear()
                return

        self.point_buffer.append(
            Point(
                x,
                y,
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black"),
            )
        )

        if (
            len(self.point_buffer) >= 2
        ):  # If the buffer has atleast 2 points, draw a line
            x1, y1, id1 = self.point_buffer[-2]
            x2, y2, id2 = self.point_buffer[-1]
            self.line_buffer[(id1, id2)] = self.canvas.create_line(
                x1, y1, x2, y2, fill="black", width=2
            )
