from keyboard import wait

from src.item_crafter.roller.screenshot_to_text import get_text_from_screenshot


class MatchChecker:
    """Класс, проверяющий, сколько раз текст повторился."""
    def __init__(self):
        self._match_counter = 0
        self._old_text = ""

    def set_text_to_check(self, text: str) -> None:
        """Отправить текст на проверку совпадения с предыдущим текстом."""
        self._raise_type_error_if_text_is_not_str(text)
        if self._old_text == text:
            self._match_counter += 1
        else:
            self._match_counter = 0

        self._old_text = text

    def _raise_type_error_if_text_is_not_str(self, text: str) -> None:
        if not isinstance(text, str):
            type_of_text = type(text).__name__
            raise TypeError(f"text должен быть str, а не {type_of_text}!")

    @property
    def number_of_matches(self) -> int:
        return self._match_counter


if __name__ == '__main__':
    button_to_press = "F2"

    print("Если текст на экране совпадёт 3 раза подряд, то программа сообщит об этом.")
    print(f"Нажми \"{button_to_press}\", чтобы сделать скриншот.\n")

    press_counter = 1
    match_checker = MatchChecker()
    while not match_checker.number_of_matches == 3:
        wait(button_to_press)
        match_checker.set_text_to_check(get_text_from_screenshot())
        print(f"Сделан скриншот №{press_counter}:", "состояние счётчика совпадений:",
              match_checker.number_of_matches)
        press_counter += 1

    print("\nОбнаружено 3 совпадения подряд.")
