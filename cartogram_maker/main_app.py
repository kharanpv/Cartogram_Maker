import customtkinter as ctk


class MainApp(ctk.CTk):
    def __init__(self):
        from .start_frame import StartFrame

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

        self.main_frame = StartFrame(self)  # Change the frame to start_frame

    def change_frame(self, frame, then_run=None):
        self.main_frame.destroy()
        self.main_frame = frame(self)
        if then_run:
            then_run(self.main_frame)


def main():
    app = MainApp()
    app.mainloop()
