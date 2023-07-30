from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from pyautogui import size

from src.item_crafter.data_classes.models import ProgramData
from src.item_crafter.data_classes.item_search_modes import ItemSearchModes
from src.item_crafter.utils.poe_finder import POEFinder
from src.item_crafter.roller.roller import Roller


class MainFrame:
    def __init__(self, master: Tk | Frame | LabelFrame | ttk.Notebook):
        self._root = ttk.Frame(master)
        self._program_data = ProgramData()  # Потребуются все данные программы.
        self._create_textinput_frame()
        self._create_setting_frame()
        self._create_textinput()
        self._create_widgets_in_setting_frame()

    def _create_textinput_frame(self) -> None:
        self._textinput_frame = LabelFrame(self._root,
                                           text="Ввод свойств для поиска:")
        self._textinput_frame.grid(row=0, column=0, pady=5, sticky=N+E+S+W)

    def _create_setting_frame(self) -> None:
        self._setting_frame = LabelFrame(self._root,
                                         text="Настройка крафта:")
        self._setting_frame.grid(row=0, column=1, pady=5, sticky=N+E+S+W)

    def _create_textinput(self) -> None:
        self._textinput = ScrolledText(self._textinput_frame,
                                        relief=SUNKEN,
                                        width=20,
                                        height=16,
                                        padx=5,
                                        bd=3,
                                        font=("Arial", 10, ""),
                                        wrap=WORD)
        self._textinput.insert(INSERT, self._program_data.main_frame.text_of_textinput.get())
        print("Textinput:", self._program_data.main_frame.text_of_textinput.get())
        self._start_update_textinput_in_data()
        self._textinput.grid(row=0, column=0, padx=4)

    def _get_text_from_textinput(self) -> str:
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

    def _create_widgets_in_setting_frame(self) -> None:
        self._create_radiobuttons_for_choosing_item_search_modes()
        self._create_updatable_labes()
        self._start_reset_updatable_labels()
        self._create_checkbutton_for_clean_up_after_failed_roll()
        self._create_save_and_load_buttons()
        self._create_start_button()

    def _create_radiobuttons_for_choosing_item_search_modes(self) -> None:
        Radiobutton(self._setting_frame,
                    text="Найти все свойства",
                    variable=self._program_data.main_frame.item_search_mode,
                    value=ItemSearchModes.ALL.value
                    ).grid(row=0, column=0, sticky=W)

        Radiobutton(self._setting_frame,
                    text="Найти хотя бы одно",
                    variable=self._program_data.main_frame.item_search_mode,
                    value=ItemSearchModes.AT_LEAST_ONE.value
                    ).grid(row=1, column=0, sticky=W)

    def _create_updatable_labes(self) -> None:
        self._label_showing_current_resolution = Label(self._setting_frame,
                                                           text=f"Текущее разрешение экрана:\n{self._f_current_resolution}.",
                                                           fg="darkblue")
        self._label_showing_current_resolution.grid(row=2, column=0)

        self._poe_finder = POEFinder()
        self._label_showing_whether_poe_is_enabled = Label(self._setting_frame,
                                                           text=self._poe_finder.get_text_that_says_is_poe_enabled(),
                                                           fg=self._poe_finder.get_color_of_text_that_says_is_poe_enabled())
        self._label_showing_whether_poe_is_enabled.grid(row=3, column=0)

    def _create_checkbutton_for_clean_up_after_failed_roll(self) -> None:
        Checkbutton(self._setting_frame,
                    text="Очищать предмет после\nнеудачного ролла",
                    variable=self._program_data.main_frame.clean_item_after_failed_roll
                    ).grid(row=4, column=0, sticky=W)

    def _create_save_and_load_buttons(self) -> None:
        Button(self._setting_frame,
               text="Загрузить ручное сохранение",
               activeforeground="green",
               command=self._load_user_save_and_upload_text_in_textinput
               ).grid(row=6, column=0, sticky=W)

        Button(self._setting_frame,
               text="Сохранить текущие настройки",
               activeforeground="green",
               command=self._program_data.do_user_save
               ).grid(row=7, column=0, sticky=W)

    def _create_start_button(self) -> None:
        Button(self._setting_frame,
               text="СТАРТ!",
               font="bold",
               bg="orange",
               fg="red",
               activebackground="orange",
               activeforeground="green",
               height=3,
               command=self._start_craft
              ).grid(row=8, column=0, sticky=N+E+S+W)


    def _load_user_save_and_upload_text_in_textinput(self) -> None:
        try:
            self._program_data.load_user_save()

        except FileNotFoundError:
            self.root.bell()  # Издать звук.
            print("Нет пользовательского сохранения!")

        else:
            self._textinput.delete("1.0", END)
            self._textinput.insert(INSERT, self._program_data.main_frame.text_of_textinput.get())

    def _start_craft(self) -> None:
        print("СТАРТ ПРОГРАММЫ!")
        roller = Roller()
        roller.run_roll()


    @property
    def _f_current_resolution(self) -> str:
        current_resolution = size()
        return f"{current_resolution[0]}x{current_resolution[1]}"


    def _start_reset_updatable_labels(self) -> None:
        self._setting_frame.after(2 * 1000, self._start_reset_updatable_labels)
        self._update_updatable_labels()
    
    def _update_updatable_labels(self) -> None:
        self._label_showing_current_resolution.configure(
            text=f"Текущее разрешение экрана:\n{self._f_current_resolution}")
        self._label_showing_whether_poe_is_enabled.configure(text=self._poe_finder.get_text_that_says_is_poe_enabled(),
                                                             fg=self._poe_finder.get_color_of_text_that_says_is_poe_enabled())


    def _start_update_textinput_in_data(self) -> None:
        self._textinput_frame.after(1000, self._start_update_textinput_in_data)
        self._update_textinput_in_data()

    def _update_textinput_in_data(self) -> None:
        self._program_data.main_frame.text_of_textinput.set(self._get_text_from_textinput())

    @property
    def root(self) -> ttk.Frame:
        return self._root
