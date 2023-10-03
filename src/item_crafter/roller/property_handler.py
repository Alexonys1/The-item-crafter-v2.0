import keyboard

from loguru import logger
from tkinter import IntVar, StringVar, Tk
from difflib import SequenceMatcher

from src.item_crafter.roller.screenshot_to_text import get_text_from_screenshot


class PropertyHandler:
    """
    Класс для обработки свойств предметов POE.
    """

    def __init__(self, text_with_pattern_properties: StringVar, property_match_percentage: IntVar):
        self._raise_type_error_if_text_with_pattern_properties_is_not_str(
            text=text_with_pattern_properties)
        self._text_with_pattern_properties = text_with_pattern_properties
        self._property_match_percentage = property_match_percentage

    def _raise_type_error_if_text_with_pattern_properties_is_not_str(self, text: StringVar) -> None:
        if not isinstance(text, StringVar):
            type_of_text = type(text).__name__
            raise TypeError(f"text_with_pattern_properties должен быть tkinter.StringVar, а не {type_of_text}!")

    def did_all_properties_match(self) -> bool:
        """Показывает, совпали все свойства."""
        for pattern_property, value_of_pattern_property in self._pattern_properties.items():
            for current_property, value_of_current_property in self._current_properties.items():
                # Если это нужное свойство:
                if value_of_current_property is not None:  # Если программа не находит в свойстве числовые значения,
                                                           # то она ставит None, которое нужно проверять.
                    if self._similar (pattern_property, current_property) >= self._match_percentage:
                        if value_of_current_property < value_of_pattern_property: # По решению Димы.
                            return False
        return True

    def did_at_least_one_property_match(self) -> bool:
        """Показывает, совпало ли хотя бы одно свойство."""
        for pattern_property, value_of_pattern_property in self._pattern_properties.items():
            for current_property, value_of_current_property in self._current_properties.items():
                # Если это нужное свойство:
                if value_of_current_property is not None:  # Если программа не находит в свойстве числовые значения,
                                                           # то она ставит None, которое нужно проверять.
                    similar = self._similar(pattern_property, current_property)
                    logger.info(f"[{pattern_property} ({value_of_pattern_property})] [{current_property} ({value_of_current_property})] -> {similar}%")
                    if similar >= self._match_percentage:
                        if value_of_current_property >= value_of_pattern_property:  # По решению Димы.
                            return True  # Если есть хотя бы одно.
        return False  # Если ничего не совпало.

    def _similar(self, a: str, b: str) -> int:
        """Возвращает сходство a и b в процентах от 0 до 100."""
        self._check_str(a, "a")
        self._check_str(b, "b")
        similarity_coefficient: float = SequenceMatcher(a=a, b=b).ratio()
        return round(similarity_coefficient * 100)

    def _check_str(self, string: str, arg_name: str) -> None:
        if not isinstance(string, str):
            type_of_string = type(string).__name__
            raise TypeError(f"Аргумент {arg_name} должен быть str, а не {type_of_string}!")

    @property
    def _match_percentage(self) -> int:
        """Получить минимальный процент сходства свойств."""
        return self._property_match_percentage.get()

    def set_properties(self, text: str) -> None:
        """Сохранитьить свойства в классе для дальнейшей обработки."""
        self._prepare_pattern_properties()  # На тот случай, если пользователь напишет новые свойства,
        self._prepare_current_properties(text)  # с которыми нужно будет сравнивать текущие.

    def _prepare_pattern_properties(self) -> None:
        self._pattern_properties = {}
        for one_property in self._text_with_pattern_properties.get().upper().replace('\n', '').split(';'):
            self._add_property_to(one_property, self._pattern_properties)

    def _prepare_current_properties(self, properties: str) -> None:
        self._current_properties = {}
        for one_property in properties.upper().split('\n'):  # Всё ставлю в верхний регистр.
            self._add_property_to(one_property, self._current_properties)

    def _add_property_to(self, one_property: str, to: dict) -> None:
        list_property = []
        for word in one_property.split():
            if not self._is_number(word):
                list_property.append(word)
        key = ' '.join(list_property)
        value = self._get_last_number(one_property)
        to[key] = value

    def _is_number(self, string: str) -> bool:
        self._check_str(string, "string")
        if string.replace('.', '', 1).isdigit():
            return True
        else:
            return False

    def _get_last_number(self, string: str) -> float | None:
        numbers = []
        number_in_string = ''
        there_is_dot = False
        for symbol in string:
            if symbol.isdigit():
                number_in_string += symbol

            elif symbol == '.' and not there_is_dot:
                number_in_string += symbol
                there_is_dot = True

            else:
                if self._is_number(number_in_string):
                    numbers.append(float(number_in_string))
                number_in_string = ''
                there_is_dot = False

        if len(numbers):
            return numbers[-1]
        else:
            return None


if __name__ == "__main__":
    window = Tk()
    button_name = "F2"

    while True:
        text_input = input("Введи свойства, которые нужно искать через запиточку: ")
        user_properties = StringVar(value=text_input)

        property_handler = PropertyHandler(user_properties, IntVar(value=84))

        print(f"Нажми {button_name}, чтобы сделать скриншот.")
        keyboard.wait(button_name)

        screenshot_text = get_text_from_screenshot((110, 220, 380, 130))

        property_handler.set_properties(screenshot_text)

        print("Весь текст с экрана:", screenshot_text, sep='\n')
        print('=' * 50)
        print(property_handler._pattern_properties)
        print(property_handler._current_properties)

        print()
        print("Все свойства совпадают:", property_handler.did_all_properties_match())
        print("Хотя бы одно свойство совпадает:", property_handler.did_at_least_one_property_match())

        print('*' * 50)
        print('*' * 50)
        print()
        print()
