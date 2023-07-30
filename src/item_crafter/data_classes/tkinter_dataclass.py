import json

from typing import Any, Callable
from tkinter import *

from src.item_crafter.data_classes.meta_data import MetaData


class TkinterDataclass (metaclass=MetaData):
    """
    Класс, специально предназначенный для наследования и
    для хранения tkinter-переменных и экземпляров этого же
    класса или его наследников.
    """
    def __new__(cls, *args, **kwargs):
        # Нужно обязательно вызвать __new__ родителя.
        instance = super().__new__(cls, *args, **kwargs)
        for key, attr in cls.__annotations__.items():
            if issubclass(attr, (Variable, TkinterDataclass)):
                # Все атрибуты класса - наследники tkinter.Variable
                # или TkinterData.
                setattr(instance, key, attr())
            else:
                class_name = instance.__class__.__name__
                type_of_attr = attr.__name__
                raise TypeError(f"{key} должен быть наследником tkinter.Variable, а не {type_of_attr}!\n" +\
                                f"Все атрибуты {class_name} должны быть наследниками tkinter.Variable.")
        return instance


    def get_as_dict(self) -> dict[str, int | float | str | bool]:
        """Получить значения всех пользовательских атрибутов класса."""
        output = {}
        for key, value in self._user_attrs.items():
            if isinstance(value, Variable):
                output[key] = value.get()  # Так как value - это tkinter-переменная.

            elif isinstance(value, TkinterDataclass):
                output[key] = value.get_as_dict()  # Да здравствует рекурсия!

            elif isinstance(value, (property, Callable)):
                # Функции или свойства, созданные программистом
                # не следует сохранять
                pass

            else:
                class_name = __class__.__name__
                type_of_value = type(value).__name__
                raise TypeError(f"{key} должен быть {class_name} или наследником tkinter.Variable, а не {type_of_value}!")
        return output


    def print_all_data(self) -> None:
        """
        Вывести значения всех пользовательских
        атрибутов класса в консоль.
        """
        for key, value in self.get_as_dict().items():
            print(key, value, sep=" = ")


    def save(self, file_name: str) -> None:
        """
        Сохранить значения всех пользовательских
        атрибутов класса в указанный файл.
        """
        with open(file_name, 'w') as file:
            save = self.get_as_dict()
            json.dump(save, file)

    def do_auto_save(self) -> None:
        """Сделать сохранение в файл self._file_name_of_auto_save."""
        file_name = self._file_name_of_auto_save
        self.save(file_name)

    def do_user_save(self) -> None:
        """Сделать сохранение в файл self._file_name_of_user_save."""
        file_name = self._file_name_of_user_save
        self.save(file_name)


    def load(self, file_name: str) -> None:
        """
        Обновить значения всех пользовательских
        атрибутов класса, загрузив сохранение
        из указанного файла.
        ОБЯЗАТЕЛЬНО обработать возможную ошибку
        FileNotFoundError!
        """
        with open(file_name, 'r') as file:
            save: dict = json.load(file)
            self._update_all_attrs(save, self.__dict__)

    def load_auto_save(self) -> None:
        """Загрузить сохранение из файла self._file_name_of_auto_save."""
        file_name = self._file_name_of_auto_save
        self.load(file_name)

    def load_user_save(self) -> None:
        """Загрузить сохранение из файла self._file_name_of_user_save."""
        file_name = self._file_name_of_user_save
        self.load(file_name)


    @property
    def _file_name_of_auto_save(self) -> str:
        return r"C:\Users\Public\Documents\The auto-save of The Item Crafter.json" # Проследить за путями!!

    @property
    def _file_name_of_user_save(self) -> str:
        return r"C:\Users\Public\Documents\The user save of The Item Crafter.json" # Проследить за путями!!

    @property
    def _user_attrs(self) -> dict[str, Variable]:
        """Получить все пользовательские атрибуты класса."""
        filtred_attrs = filter(
            lambda x: not x[0].startswith("__"),
            self.__dict__.items()
        )
        return dict(filtred_attrs)

    def _update_all_attrs(self, attrs: int | float | str | bool | \
                             dict[str, int | float | str | bool],
                                to: dict[str, Any]) -> None:
        """
        Обновляет все указанные атрибуты в
        указанном словаре.
        """
        for key, value in attrs.items():
            if isinstance(to[key], Variable):
                to[key].set(value)

            elif isinstance(to[key], TkinterDataclass):
                self._update_all_attrs(attrs[key], to[key])

            else:
                raise TypeError

    def __getitem__(self, key: str) -> Variable:
        return self._user_attrs[key]
