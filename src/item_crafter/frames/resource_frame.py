import keyboard

from tkinter import *
from tkinter import ttk
from pyautogui import position

from src.item_crafter.data_classes.models import ProgramData, Point


class ResourceFrame:
    def __init__(self, master: Tk | Frame | LabelFrame | ttk.Notebook):
        self._root = ttk.Frame(master)
        program_data = ProgramData()
        self._resources = program_data.resources
        self._orbs_of_scouring = program_data.orbs_of_scouring
        self._create_small_main_resouce_frame()
        self._create_labels_in_small_main_resouces_frame()
        self._create_small_frame_of_orbs_of_scouring()
        self._create_labels_in_small_frame_of_orbs_of_scouring()
        self._reset_labels()

    def _create_small_main_resouce_frame(self) -> None:
        self._small_main_resouces_frame = LabelFrame(self._root,
                                                     text="Где брать ресурсы:")
        self._small_main_resouces_frame.grid(row=0,
                                             column=0,
                                             padx=5,
                                             pady=5,
                                             sticky=W
                                             )

    def _create_labels_in_small_main_resouces_frame(self) -> None:
        Label(self._small_main_resouces_frame,
              text="Точка сбора ресурсов:"
              ).grid(row=0, column=0)

        self._label_with_resource_collection_point = Label(
            self._small_main_resouces_frame,
            fg="blue",
            text=self._resources.f_point_coordinates
        )
        self._label_with_resource_collection_point.grid(row=0, column=1)

        Label(self._small_main_resouces_frame,
              text="Расброс в координатах:"
              ).grid(row=1, column=0)

        self._dispersion_scale = Scale(
            self._small_main_resouces_frame,
            variable=self._resources.dispersion,
            orient=HORIZONTAL,
            from_=0, to=20,
            tickinterval=5,
            resolution=1,
            length=80
        )
        self._dispersion_scale.set(self._resources.dispersion.get())
        self._dispersion_scale.grid(row=1, column=1)

        Button(self._small_main_resouces_frame,
               text="Настроить",
               bg="light sky blue",  # См. спец. таблицу.
               activebackground="khaki",
               command=self._set_place_of_resources
               ).grid(row=2, column=0, sticky=N+E+S+W)

        Label(self._small_main_resouces_frame,
              text=f"\"{self._setting_button_of_keyboard}\" для\nсоздания точки",
              fg="darkred"
              ).grid(row=2, column=1)

    def _create_small_frame_of_orbs_of_scouring(self) -> None:
        self._small_frame_of_orbs_of_scouring = LabelFrame(self._root,
                                                           text="Где брать сферы очищения:")
        self._small_frame_of_orbs_of_scouring.grid(row=1,
                                                   column=0,
                                                   padx=5,
                                                   pady=5,
                                                   sticky=W
                                                   )

    def _create_labels_in_small_frame_of_orbs_of_scouring(self) -> None:
        Label(self._small_frame_of_orbs_of_scouring,
              text="Точка сбора сфер очищения:"
              ).grid(row=0, column=0)

        self._label_with_collection_point_of_orbs_of_scouring = Label(
            self._small_frame_of_orbs_of_scouring,
            fg="blue",
            text=self._orbs_of_scouring.f_point_coordinates
        )
        self._label_with_collection_point_of_orbs_of_scouring.grid(row=0, column=1)

        Label(self._small_frame_of_orbs_of_scouring,
              text="Расброс в координатах:"
              ).grid(row=1, column=0)

        self._dispersion_scale = Scale(
            self._small_frame_of_orbs_of_scouring,
            variable=self._orbs_of_scouring.dispersion,
            orient=HORIZONTAL,
            from_=0, to=20,
            tickinterval=5,
            resolution=1,
            length=80
        )
        self._dispersion_scale.set(self._orbs_of_scouring.dispersion.get())
        self._dispersion_scale.grid(row=1, column=1)

        Button(self._small_frame_of_orbs_of_scouring,
               text="Настроить",
               bg="light sky blue",  # См. спец. таблицу.
               activebackground="khaki",
               command=self._set_place_of_orbs_of_scouring
               ).grid(row=2, column=0, sticky=N + E + S + W)

        Label(self._small_frame_of_orbs_of_scouring,
              text=f"\"{self._setting_button_of_keyboard}\" для\nсоздания точки",
              fg="darkred"
              ).grid(row=2, column=1)

    @property
    def _setting_button_of_keyboard(self) -> str:
        return "F2"

    def _set_place(self, data: Point) -> None:
        keyboard.wait(self._setting_button_of_keyboard)
        x_mouse_coordinate, y_mouse_coordinate = position()
        data.x.set(x_mouse_coordinate)
        data.y.set(y_mouse_coordinate)
        print(f"Current mouse position: ({x_mouse_coordinate}; {y_mouse_coordinate})")

    def _set_place_of_resources(self) -> None:
        self._set_place(self._resources)

    def _set_place_of_orbs_of_scouring(self) -> None:
        self._set_place(self._orbs_of_scouring)

    def _reset_labels(self) -> None:
        self._root.after(1000, self._reset_labels)
        self._label_with_resource_collection_point.configure(
            text=self._resources.f_point_coordinates)
        self._label_with_collection_point_of_orbs_of_scouring.configure(
            text=self._orbs_of_scouring.f_point_coordinates)

    @property
    def root(self) -> ttk.Frame:
        return self._root
