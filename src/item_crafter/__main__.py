from loguru import logger

from src.item_crafter.main_window.main_window import MainWindow


logger.add(
    "..\\..\\logs.log",
    format="[{time: HH:mm:ss} {level}]: {message}",
    level="INFO",
    rotation="5:00"
)


# Так как это точка входа,
# то все открытия файлов нужно
# производить относительно
# этого файла!
main_window = MainWindow()
main_window.run()
