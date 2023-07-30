from src.item_crafter.main_window.main_window import MainWindow



# Так как это точка входа,
# то все открытия файлов нужно
# производить относительно
# этого файла!
main_window = MainWindow()
main_window.run()