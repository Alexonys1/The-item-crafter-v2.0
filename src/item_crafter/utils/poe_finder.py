import time

import pyautogui as pag

from loguru import logger
from typing import Any
from random import uniform
from keyboard import wait

from src.item_crafter.utils.singleton import Singleton


class POEFinder(Singleton):
    """Класс, показывающий, включено ли POE."""

    def __init__(self):
        self._poe_coordinates = None

    @staticmethod
    def find_poe(function: callable) -> callable:
        """Обновляет self._poe_coordinates в классе."""
        def wrapper(self, *args, **kwargs) -> Any:
            # self._poe_coordinates: None | tuple[int, int, int, int]
            self._poe_coordinates = pag.locateOnScreen(image=self._name_of_poe_image, confidence=0.7)
            if self._poe_coordinates is None:
                logger.warning("POE не видно на экране!")
            return function(self, *args, **kwargs)

        return wrapper

    @property
    @find_poe
    def poe_coordinates(self) -> None | tuple[int, int, int, int]:
        return self._poe_coordinates

    @find_poe
    def open_poe(self) -> None:
        """
        Наводит мышку на иконку POE на
        панели задач и нажимает на неё.
        """
        pag.moveTo(self._poe_coordinates, duration=self._get_random_duration())
        time.sleep(0.1)  # Необходимая задержка, чтобы игра успела открыться.
        pag.click(button="left")

    def _get_random_duration(self) -> float:
        return uniform(0.1, 0.4)

    @find_poe
    def get_text_that_says_is_poe_enabled(self) -> str:
        """Получить текст, говорящий включено ли POE или нет."""
        if self._poe_coordinates:
            return "POE включено."
        else:
            return "POE выключено."

    def get_color_of_text_that_says_is_poe_enabled(self) -> str:
        """
        Получить цвет текста, который говорит, включено ли POE.
        ВНИМАНИЕ! Подразумевается, что этот метод будет вызван
        сразу после self.get_text_that_says_is_poe_enabled.
        Так сделано, чтобы не вызывать дважды декоратор find_poe
        и не замедлять работу программы.
        """
        if self._poe_coordinates:
            return "darkgreen"
        else:
            return "red"

    @property
    def _name_of_poe_image(self) -> str:
        return "..\\..\\images\\PoE.PNG"  # Следить за путём!!


if __name__ == '__main__':
    poe_finder = POEFinder()
    print("Чтобы проверить, включено ли POE, нажми \"F2\".")

    while True:
        wait("F2")
        text = poe_finder.get_text_that_says_is_poe_enabled()
        text_color = poe_finder.get_color_of_text_that_says_is_poe_enabled()
        print(f"{text} Цвет текста: {text_color}.")
        poe_finder.open_poe()
