from tkinter import Tk

from src.item_crafter.main_window.tabs import TabController
from src.item_crafter.data_classes.models import ProgramData


class MainWindow:
    def __init__(self):
        self._create_root()
        self._create_tab_controller()
        self._run_tab_controller()

    def _create_root(self) -> None:
        self._root = Tk()
        self._root.title("The item crafter")
        self._root.iconbitmap("..\\..\\images\\icon.ico")
        self._root.geometry("380x355")
        self._root.resizable(width=False, height=False)

    def _create_tab_controller(self) -> None:
        # Перед созданием всех рамок нужно загрузить
        # предыдущее автосохранение.
        self._load_auto_save()
        self.tabs = TabController(self._root)

    def _run_tab_controller(self) -> None:
        self.tabs.run()

    def _load_auto_save(self) -> None:
        try:
            program_data = ProgramData()  # Singleton.
            program_data.load_auto_save()

        except FileNotFoundError:
            # Значения по умолчанию загрузятся автоматически.
            print("Не найден файл с автосохранением!")

    def run(self) -> None:
        self._root.mainloop()
