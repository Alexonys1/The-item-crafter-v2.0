from loguru import logger
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from src.item_crafter.data_classes.models import ProgramData


class NotebookFrame:
    def __init__(self, master: Tk | Frame | LabelFrame | ttk.Notebook):
        self._root = ttk.Frame(master)
        self._notebook = ProgramData().notebook
        self._create_textinput_in_root()
        self.update_text_in_textinput()
        self._start_update_text_of_textinput_in_data()

    def _create_textinput_in_root(self) -> None:
        self._textinput = ScrolledText(self._root,
                                       relief=SUNKEN,
                                       width=48,
                                       height=19,
                                       padx=5,
                                       bd=3,
                                       font=("Arial", 10, ""),
                                       wrap=WORD)
        self._textinput.grid(row=0, column=0, padx=4)

    def update_text_in_textinput(self) -> None:
        self._textinput.delete("1.0", END)
        self._textinput.insert(INSERT, self._notebook.text.get())
        logger.info(f"Содержимое блокнота: {self._notebook.text.get()}")

    def _start_update_text_of_textinput_in_data(self) -> None:
        self._root.after(1000, self._start_update_text_of_textinput_in_data)
        self._update_text_of_textinput_in_data()

    def _update_text_of_textinput_in_data(self) -> None:
        self._notebook.text.set(self._get_text_from_text_input())

    def _get_text_from_text_input(self) -> str:
        ZERO_SYMBOL_OF_FIRST_STRING = "1.0"
        # Это означает, что начать следует ^^
        # с нулевого символа первой строки
        END_OF_TEXT_WIDGET_OF_TKINTER = "end-1c"
        # Мы не знаем, где находится конец текста tkinter-виджета,
        # но у нас есть константа END (tkinter.END), которая знает это.
        # Но она добавляет лишний символ в строку.
        # Чтобы его убрать нужно прописать "end-1c".
        return self._textinput.get(ZERO_SYMBOL_OF_FIRST_STRING,
                                   END_OF_TEXT_WIDGET_OF_TKINTER)

    @property
    def root(self) -> ttk.Frame:
        return self._root
