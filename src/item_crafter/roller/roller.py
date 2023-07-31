import time
import keyboard
import pyautogui as pag

from random import randint, uniform
from typing import NoReturn, Any

from src.item_crafter.data_classes.models import ProgramData
from src.item_crafter.data_classes.item_search_modes import ItemSearchModes
from src.item_crafter.utils.poe_finder import POEFinder
from src.item_crafter.utils.sounds import *
from src.item_crafter.exceptions import ResourcesHaveRunOut
from src.item_crafter.roller.screenshot_to_text import get_text_from_screenshot
from src.item_crafter.roller.property_handler import PropertyHandler
from src.item_crafter.roller.match_checker import MatchChecker


class Roller:
    """Класс для ролла свойств: для крафта предметов."""

    def __init__(self):
        self._program_data = ProgramData()  # Нужны все данные программы.
        self._match_checker = MatchChecker()
        self._property_handler = PropertyHandler(
            text_with_pattern_properties=self._program_data.main_frame.text_of_textinput)

    def run_roll(self) -> None:
        try:
            self._open_poe()
            self._move_to_resource_collection_point()
            self._press_shift()
            self._press_right_mouse_button()
            self._move_to_craft_region()
            self._run_roll_loop()

        except ResourcesHaveRunOut:
            play_sound_meaning_that_system_has_failed()

        except pag.FailSafeException: # Если навести мышку в любой угол экрана, то поднимется это исключение.
            keyboard.release("shift")  # pag.keyUp поднимет не shift, а pag.FailSafeException.
            print("Пользователь сам остановил программу.", end="\n\n\n")

        else:
            play_sound_meaning_that_property_has_been_found()

        finally:
            self._release_shift()


    def _open_poe(self) -> None:
        poe_finder = POEFinder()
        poe_finder.open_poe()
        time.sleep(0.4)  # Задержка, чтобы POE успело открыться.

    def _move_to_resource_collection_point(self) -> None:
        resources = self._program_data.resources
        x_coordinate = resources.x.get()
        y_coordinate = resources.y.get()
        dispersion = resources.dispersion.get()

        x_coordinate += randint(-dispersion, dispersion)
        y_coordinate += randint(-dispersion, dispersion)

        self._move_to(x_coordinate, y_coordinate)

    def _move_to(self, x_coordinate: int, y_coordinate: int, dispersion: int = 0) -> None:
        x_coordinate += randint(-dispersion, dispersion)
        y_coordinate += randint(-dispersion, dispersion)
        random_duration = self._get_random_duration()  # Чтобы значения всегда были разными.
        pag.moveTo(x_coordinate, y_coordinate, duration=random_duration)

    def _get_random_duration(self) -> float:
        return uniform(0.1, 0.4)

    # Лучше использовать keyboard для удержания
    # клавиш на клавиатуре, так как keyboard-функции не поднимут
    # потенциально опасное исключение pag.FailSafeException.
    def _press_shift(self) -> None:
        keyboard.press("shift")

    def _release_shift(self) -> None:
        keyboard.release("shift")

    def _press_right_mouse_button(self) -> None:
        pag.click(button="right")

    def _press_left_mouse_button(self) -> None:
        pag.click(button="left")

    def _move_to_craft_region(self) -> None:
        craft_region = self._program_data.craft_region
        x_of_left_top_corner = craft_region.x_of_left_top_corner.get()
        y_of_left_top_corner = craft_region.y_of_left_top_corner.get()
        width = craft_region.width.get()
        height = craft_region.height.get()

        random_x_of_craft_region = randint(x_of_left_top_corner, x_of_left_top_corner + width)
        random_y_of_craft_region = randint(y_of_left_top_corner, y_of_left_top_corner + height)

        self._move_to(random_x_of_craft_region, random_y_of_craft_region)
        time.sleep(0.2)

    def _run_roll_loop(self) -> None | NoReturn:
        self._is_first_click = True
        while self._whether_to_roll:

            if self._need_to_clean_items_after_roll:
                self._release_shift()
                self._press_left_mouse_button_if_first_click()
                self._clean_item_using_orb_of_scouring()
                self._move_to_resource_collection_point()
                self._press_right_mouse_button()
                self._move_to_craft_region()

            if self._match_checker.number_of_matches >= 3:
                # Если текст повторяется, значит нет ресурсов для крафта
                # или просто очень-очень повезло.
                raise ResourcesHaveRunOut("Закончились ресурсы!")

            else:
                self._press_left_mouse_button()
                self._random_micro_sleep()

    @property
    def _whether_to_roll(self) -> bool:
        """
        Показывает, нужно ли роллить.
        Если нужное свойство(-а) НЕ найдено(-ы),
        значит нужно роллить дальше.
        Если найдено(-ы), значит программа завершает
        свою работу и роллить больше не нужно.
        """
        self._read_properties()
        match self._program_data.main_frame.item_search_mode.get():
            case ItemSearchModes.ALL.value:
                return not self._property_handler.did_all_properties_match()

            case ItemSearchModes.AT_LEAST_ONE.value:
                return not self._property_handler.did_at_least_one_property_match()

            case _:
                raise ValueError("Неправильное значение item_search_mode!")

    def _read_properties(self) -> None:
        properties_in_string: str = self._get_text_from_region_of_reading_properties()
        self._match_checker.set_text_to_check(properties_in_string)
        self._property_handler.set_properties(properties_in_string)

    def _get_text_from_region_of_reading_properties(self) -> str:
        return get_text_from_screenshot(self._region_of_reading_properties)

    @property
    def _region_of_reading_properties(self) -> tuple[int, int, int, int]:
        read_region = self._program_data.read_region
        return (read_region.x_of_left_top_corner.get(),
                read_region.y_of_left_top_corner.get(),
                read_region.width.get(),
                read_region.height.get()
                )

    @property
    def _need_to_clean_items_after_roll(self) -> bool:
        return self._program_data.main_frame.clean_item_after_failed_roll.get()

    def _clean_item_using_orb_of_scouring(self) -> None:
        self._move_to_orbs_of_scouring()
        self._press_right_mouse_button()
        self._move_to_craft_region()
        self._press_left_mouse_button()

    def _move_to_orbs_of_scouring(self) -> None:
        orbs_of_scouring = self._program_data.orbs_of_scouring
        x_coordinate = orbs_of_scouring.x.get()
        y_coordinate = orbs_of_scouring.y.get()
        dispersion = orbs_of_scouring.dispersion.get()
        self._move_to(x_coordinate, y_coordinate, dispersion)

    def _press_left_mouse_button_if_first_click(self):
        if self._is_first_click:
            self._is_first_click = False
            self._press_left_mouse_button()

    def _random_micro_sleep(self) -> None:
        random_seconds = uniform(0.1, 0.2)
        time.sleep(random_seconds)
