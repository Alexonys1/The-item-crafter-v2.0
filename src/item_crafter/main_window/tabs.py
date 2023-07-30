from tkinter import ttk

from src.item_crafter.data_classes.models import ProgramData
from src.item_crafter.frames.main_frame import MainFrame
from src.item_crafter.frames.resource_frame import ResourceFrame
from src.item_crafter.frames.craft_frame import CraftFrame
from src.item_crafter.frames.notebook_frame import NotebookFrame


class TabController:
    def __init__(self, root):
        self._root = ttk.Notebook(root)
        self._bind_root()
        self._add_main_frame()
        self._add_resource_frame()
        self._add_craft_frame()
        self._add_notebook_frame()

    def _bind_root(self) -> None:
        self._root.bind("<Destroy>", self._do_auto_save)

    def _do_auto_save(self, event) -> None:
        program_data = ProgramData() # Singleton.
        program_data.do_auto_save()

    def _add_main_frame(self) -> None:
        self._main_frame = MainFrame(self._root)
        self._root.add(self._main_frame.root, text="Главная")

    def _add_resource_frame(self) -> None:
        self._resource_frame = ResourceFrame(self._root)
        self._root.add(self._resource_frame.root,
                       text="Ресурсы")

    def _add_craft_frame(self) -> None:
        self._craft_frame = CraftFrame(self._root)
        self._root.add(self._craft_frame.root,
                       text="Где крафтить и читать свойства")

    def _add_notebook_frame(self) -> None:
        self._notebook_frame = NotebookFrame(self._root)
        self._root.add(self._notebook_frame.root,
                       text="Блокнот")

    def run(self) -> None:
        # Нужно уточнить информацию по этому поводу
        self._root.pack(expand=True, fill="both")
