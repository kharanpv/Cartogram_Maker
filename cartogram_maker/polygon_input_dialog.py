import customtkinter as ctk
from collections.abc import Callable
from typing import Any


class PolygonInputDialog(ctk.CTkToplevel):
    def __init__(
        self,
        title: str = "Input Dialog",
        text: dict[str, (str, Callable[[Any], Any])] = None,
    ):
        super().__init__()

        self._user_input: dict[str, Any] | None = None
        self._running: bool = False
        self._title: str = title
        self._text = text

        self.title(self._title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(
            10, self._create_widgets
        )  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

    def _create_widgets(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._entry: dict[str, (ctk.CTkEntry, Callable[[Any], Any])] = {}
        self._entry_list: list[ctk.CTkEntry] = []

        i = 0
        for k, (text, callback) in self._text.items():
            self._label = ctk.CTkLabel(
                master=self,
                width=300,
                wraplength=300,
                fg_color="transparent",
                text=text,
            )
            self._label.grid(
                row=i, column=0, columnspan=2, padx=20, pady=20, sticky="ew"
            )

            self._current_entry = ctk.CTkEntry(master=self, width=230)
            self._current_entry.grid(
                row=i + 1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew"
            )
            self._entry[k] = (self._current_entry, callback)
            self._entry_list.append(self._current_entry)

            i += 2

        self._ok_button = ctk.CTkButton(
            master=self, width=100, border_width=0, text="Ok", command=self._ok_event
        )
        self._ok_button.grid(
            row=i, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew"
        )

        self._cancel_button = ctk.CTkButton(
            master=self,
            width=100,
            border_width=0,
            text="Cancel",
            command=self._cancel_event,
        )
        self._cancel_button.grid(
            row=i, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew"
        )

        self.after(
            150, lambda: self._entry_list[0].focus()
        )  # set focus to entry with slight delay, otherwise it won't work

        for c, n in zip(self._entry_list, self._entry_list[1:]):
            c.bind("<Return>", lambda _, entry=n: entry.focus_set())

        self._entry_list[-1].bind("<Return>", self._ok_event)

    def _ok_event(self, _=None):
        self._user_input = {k: callback(entry.get()) for k, (entry, callback) in self._entry.items()}
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input
