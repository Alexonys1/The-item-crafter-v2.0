import keyboard

from tkinter import *
from tkinter import ttk

from pyautogui import position

from src.item_crafter.data_classes.models import ProgramData, Region


class CraftFrame:
    def __init__(self, master: Tk | Frame | LabelFrame | ttk.Notebook):
        self._root = ttk.Frame(master)
        program_data = ProgramData()
        self._read_region = program_data.read_region
        self._craft_region = program_data.craft_region
        self._create_small_frame_for_reading_properties()
        self._create_labels_in_small_frame_for_reading_properties()
        self._create_small_frame_for_setting_roll()
        self._create_labels_in_small_frame_for_setting_roll()
        self._reset_labels()

    def _create_small_frame_for_reading_properties(self) -> None:
        self._small_frame_for_reading_properties = LabelFrame(self._root,
                                                              text="Где читать свойства:")
        self._small_frame_for_reading_properties.grid(row=0,
                                                      column=0,
                                                      padx=5,
                                                      pady=5,
                                                      sticky=W
                                                      )

    def _create_labels_in_small_frame_for_reading_properties(self) -> None:
        Label(self._small_frame_for_reading_properties,
              text="Верхний левый угол\nобласти чтения свойств:"
              ).grid(row=0, column=0)

        self._label_with_left_top_point_of_read_region = Label(
            self._small_frame_for_reading_properties,
            fg="blue",
            text=self._read_region.f_coordinates_of_left_top_corner
        )
        self._label_with_left_top_point_of_read_region.grid(row=0, column=1)

        Label(self._small_frame_for_reading_properties,
              text="Ширина области:"
              ).grid(row=1, column=0)

        Label(self._small_frame_for_reading_properties,
              text="Высота области:"
              ).grid(row=2, column=0)

        self._label_with_width_of_read_region = Label(
            self._small_frame_for_reading_properties,
            text=self._read_region.width.get(),
            fg="blue"
        )
        self._label_with_width_of_read_region.grid(row=1, column=1)

        self._label_with_height_of_read_region = Label(
            self._small_frame_for_reading_properties,
            text=self._read_region.height.get(),
            fg="blue"
        )
        self._label_with_height_of_read_region.grid(row=2, column=1)

        Button(self._small_frame_for_reading_properties,
               text="Отметить верхний левый угол",
               bg="light sky blue",  # См. спец. таблицу.
               activebackground="khaki",  # См. спец. таблицу.
               command=self._set_left_top_corner_of_read_region
               ).grid(row=3, column=0, sticky=N + E + S + W)

        Button(self._small_frame_for_reading_properties,
               text="Отметить нижний правый угол",
               bg="light sky blue",  # См. спец. таблицу.
               activebackground="khaki",  # См. спец. таблицу.
               command=self._set_right_bottom_corner_of_read_region
               ).grid(row=4, column=0, sticky=N + E + S + W)

        Label(self._small_frame_for_reading_properties,
              text=f"\"{self._setting_button_of_keyboard}\" для\nсоздания\nточки",
              fg="darkred",
              relief=SUNKEN
              ).grid(row=3, column=1, rowspan=2, padx=2, pady=3)

    def _create_small_frame_for_setting_roll(self) -> None:
        self._small_frame_for_setting_roll = LabelFrame(self._root,
                                                        text="Где крафтить:")
        self._small_frame_for_setting_roll.grid(row=1,
                                                column=0,
                                                padx=5,
                                                pady=5,
                                                sticky=W
                                                )

    def _create_labels_in_small_frame_for_setting_roll(self) -> None:
        Label(self._small_frame_for_setting_roll,
              text="Верхний левый угол\nобласти крафта:"
              ).grid(row=0, column=0)

        self._label_with_left_top_point_of_roll_region = Label(
            self._small_frame_for_setting_roll,
            fg="blue",
            text=self._craft_region.f_coordinates_of_left_top_corner
        )
        self._label_with_left_top_point_of_roll_region.grid(row=0, column=1)

        Label(self._small_frame_for_setting_roll,
              text="Ширина области:"
              ).grid(row=1, column=0)

        Label(self._small_frame_for_setting_roll,
              text="Высота области:"
              ).grid(row=2, column=0)

        self._label_with_width_of_roll_region = Label(
            self._small_frame_for_setting_roll,
            text=self._craft_region.width.get(),
            fg="blue"
        )
        self._label_with_width_of_roll_region.grid(row=1, column=1)

        self._label_with_height_of_roll_region = Label(
            self._small_frame_for_setting_roll,
            text=self._craft_region.height.get(),
            fg="blue"
        )
        self._label_with_height_of_roll_region.grid(row=2, column=1)

        Button(self._small_frame_for_setting_roll,
               text="Отметить верхний левый угол",
               bg="light sky blue",  # См. спец. таблицу.
               activebackground="khaki",  # См. спец. таблицу.
               command=self._set_left_top_corner_of_roll_region
               ).grid(row=3, column=0, sticky=N + E + S + W)

        Button(self._small_frame_for_setting_roll,
               text="Отметить нижний правый угол",
               bg="light sky blue",  # См. спец. таблицу.
               activebackground="khaki",  # См. спец. таблицу.
               command=self._set_right_bottom_corner_of_roll_region
               ).grid(row=4, column=0, sticky=N + E + S + W)

        Label(self._small_frame_for_setting_roll,
              text=f"\"{self._setting_button_of_keyboard}\" для\nсоздания\nточки",
              fg="darkred",
              relief=SUNKEN
              ).grid(row=3, column=1, rowspan=2, padx=2, pady=3)

    @property
    def _setting_button_of_keyboard(self) -> str:
        return "F2"

    def _set_left_top_corner(self, data: Region) -> None:
        keyboard.wait(self._setting_button_of_keyboard)
        current_x_mouse_coordinate, current_y_mouse_coordinate = position()
        data.x_of_left_top_corner.set(current_x_mouse_coordinate)
        data.y_of_left_top_corner.set(current_y_mouse_coordinate)
        print(f"Current mouse position: ({current_x_mouse_coordinate}; {current_y_mouse_coordinate})")

    def _set_left_top_corner_of_roll_region(self) -> None:
        self._set_left_top_corner(self._craft_region)

    def _set_left_top_corner_of_read_region(self) -> None:
        self._set_left_top_corner(self._read_region)

    def _set_right_bottom_corner(self, data: Region) -> None:
        keyboard.wait(self._setting_button_of_keyboard)
        current_x_coordinate_of_right_bottom_corner, current_y_coordinate_of_right_bottom_corner = position()
        current_x_cordinate_of_left_top_corner = data.x_of_left_top_corner.get()
        current_y_cordinate_of_left_top_corner = data.y_of_left_top_corner.get()
        new_width_of_read_place = current_x_coordinate_of_right_bottom_corner - current_x_cordinate_of_left_top_corner
        new_height_of_read_place = current_y_coordinate_of_right_bottom_corner - current_y_cordinate_of_left_top_corner

        if new_width_of_read_place <= 0 or new_height_of_read_place <= 0:
            self._small_frame_for_reading_properties.bell()  # Пропищать.
        else:
            data.width.set(new_width_of_read_place)
            data.height.set(new_height_of_read_place)
        print(
            f"Current mouse position: ({current_x_coordinate_of_right_bottom_corner}; " +\
            f"{current_y_coordinate_of_right_bottom_corner})")

    def _set_right_bottom_corner_of_roll_region(self) -> None:
        self._set_right_bottom_corner(self._craft_region)

    def _set_right_bottom_corner_of_read_region(self) -> None:
        self._set_right_bottom_corner(self._read_region)

    def _reset_labels(self) -> None:
        self._root.after(1000, self._reset_labels)
        self._label_with_left_top_point_of_read_region.configure(
            text=self._read_region.f_coordinates_of_left_top_corner)
        self._label_with_width_of_read_region.configure(
            text=self._read_region.width.get())
        self._label_with_height_of_read_region.configure(
            text=self._read_region.height.get())

        self._label_with_left_top_point_of_roll_region.configure(
            text=self._craft_region.f_coordinates_of_left_top_corner)
        self._label_with_width_of_roll_region.configure(
            text=self._craft_region.width.get())
        self._label_with_height_of_roll_region.configure(
            text=self._craft_region.height.get())

    @property
    def root(self) -> ttk.Frame:
        return self._root
