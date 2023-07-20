import customtkinter as ctk


class main_app(ctk.CTk):
    def __init__(self):
        from .start_frame import start_frame
        from .edit_data import edit_data

        super().__init__()

        self.title("Cartogram Maker")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a frame inside the application window
        self.main_frame = ctk.CTkFrame(self, fg_color="#EBEBEB")
        self.main_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.main_frame = start_frame(self) # Change the frame to start_frame

    def change_frame(self, frame):
        self.main_frame.destroy()
        self.main_frame = frame(self)

        print("[DEBUG]: Frame successfully changed")

def main():
    app = main_app()
    app.mainloop()
