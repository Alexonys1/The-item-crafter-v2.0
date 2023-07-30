from tkinter import StringVar, IntVar, BooleanVar, Tk

from src.item_crafter.data_classes.tkinter_dataclass import TkinterDataclass
from src.item_crafter.utils.singleton import Singleton


class Point(TkinterDataclass):
    x: IntVar
    y: IntVar
    dispersion: IntVar

    @property
    def f_point_coordinates(self) -> str:
        """Получить координаты точки в виде (x = 9; y = 9)."""
        x = self.x.get()
        y = self.y.get()
        return f"({x = }; {y = })"


class Region(TkinterDataclass):
    x_of_left_top_corner: IntVar
    y_of_left_top_corner: IntVar
    width: IntVar
    height: IntVar

    @property
    def f_coordinates_of_left_top_corner(self) -> str:
        x = self.x_of_left_top_corner.get()
        y = self.y_of_left_top_corner.get()
        return f"({x = }; {y = })"


class Main(TkinterDataclass):
    item_search_mode: StringVar
    clean_item_after_failed_roll: BooleanVar
    text_of_textinput: StringVar


class Notebook(TkinterDataclass):
    text: StringVar


class ProgramData(Singleton, TkinterDataclass):
    main_frame: Main
    resources: Point
    craft_region: Region
    read_region: Region
    orbs_of_scouring: Point
    notebook: Notebook


if __name__ == "__main__":
    root = Tk()  # Чтобы можно было запустить.

    data_handler = ProgramData()
    data_handler.load_auto_save()
    data_handler.print_all_data()
    print()
