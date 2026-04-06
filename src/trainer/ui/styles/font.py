from pathlib import Path
from typing import ClassVar
import ctypes
import win32gui
import win32con
import dearpygui.dearpygui as dpg
from trainer.ui.styles.base import BaseStyle

class Fonts(BaseStyle):
    

    FONTS_DIR: ClassVar[Path] = Path(__file__).parent / "fonts" / "Roboto" / "static"
    FONT_REGULAR: ClassVar[str] = "Roboto-Regular.ttf"
    FONT_BOLD: ClassVar[str] = "Roboto-Bold.ttf"
    FONT_MEDIUM: ClassVar[str] = "Roboto-Medium.ttf"

    FONT_SIZE_SM: ClassVar[int] = 12
    FONT_SIZE_MD: ClassVar[int] = 15
    FONT_SIZE_LG: ClassVar[int] = 20


    def __init__(self):
        
        self.__register_fonts()
        self.__set_global_font()
        super().__init__()

    def __register_fonts(self) -> None:
        
        with dpg.font_registry():
            
            self.__font_sm = dpg.add_font(str(self.FONTS_DIR / self.FONT_REGULAR), self.FONT_SIZE_SM)
            self.__font_md = dpg.add_font(str(self.FONTS_DIR / self.FONT_REGULAR), self.FONT_SIZE_MD)
            self.__font_lg = dpg.add_font(str(self.FONTS_DIR / self.FONT_REGULAR), self.FONT_SIZE_LG)
            
    def __set_global_font(self) -> None: dpg.bind_font(self.__font_md)


    @property
    def font_sm(self) -> int:
        return self.__font_sm

    @property
    def font_md(self) -> int:
        return self.__font_md

    @property
    def font_lg(self) -> int:
        return self.__font_lg

    def apply(self, component: int | str, font: int) -> None:
        dpg.bind_item_font(component, font)