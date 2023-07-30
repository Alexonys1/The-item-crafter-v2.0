import pyautogui as pag
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "..\\..\\Tesseract-OCR\\tesseract.exe"

from typing import Optional
from PIL import Image
from keyboard import wait


def get_text_from_screenshot(region: Optional[tuple[int, int, int, int]] = None) -> str:
    """Получить текст из указанной области экрана в ВЕРХНЕМ РЕГИСТРЕ."""
    screenshot: Image = pag.screenshot(region=region)
    black_and_white_screenshot = _make_black_and_white_screenshot(screenshot)
    return pytesseract.image_to_string(black_and_white_screenshot, lang="rus").upper()


def _make_black_and_white_screenshot(screenshot: Image) -> Image:
    thresh = 70  # До какого значения всё делать белым.
    la = lambda x: 255 if x > thresh else 0
    return screenshot.convert('L').point(la, mode='1')


if __name__ == "__main__":
    button_name = "F2"
    print(f"Нажми \"{button_name}\" для прочтения текста со всего экрана.", end="\n\n")
    while True:
        wait(button_name)
        print(get_text_from_screenshot())
        print()
