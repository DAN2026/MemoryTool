from pathlib import Path
from typing import ClassVar
from trainer.ui.styles.base import BaseStyle
from loguru import logger
import dearpygui.dearpygui as dpg


class Fonts(BaseStyle):

    FONTS_DIR: ClassVar[Path] = Path(__file__).parent / "fonts" / "Open_Sans" / "static"

    FONT_SIZE_8:  ClassVar[int] = 8
    FONT_SIZE_9:  ClassVar[int] = 9
    FONT_SIZE_10: ClassVar[int] = 10
    FONT_SIZE_11: ClassVar[int] = 11
    FONT_SIZE_12: ClassVar[int] = 12
    FONT_SIZE_13: ClassVar[int] = 13
    FONT_SIZE_14: ClassVar[int] = 14
    FONT_SIZE_15: ClassVar[int] = 15
    FONT_SIZE_16: ClassVar[int] = 16
    FONT_SIZE_18: ClassVar[int] = 18
    FONT_SIZE_20: ClassVar[int] = 20
    FONT_SIZE_22: ClassVar[int] = 22

    def __init__(self):
        self.__font_8:   None = None
        self.__font_9:   None = None
        self.__font_10:  None = None
        self.__font_11:  None = None
        self.__font_12:  None = None
        self.__font_13:  None = None
        self.__font_14:  None = None
        self.__font_15:  None = None
        self.__font_16:  None = None
        self.__font_18:  None = None
        self.__font_20:  None = None
        self.__font_22:  None = None
        self.__font_bold_8:   None = None
        self.__font_bold_9:   None = None
        self.__font_bold_10:  None = None
        self.__font_bold_11:  None = None
        self.__font_bold_12:  None = None
        self.__font_bold_13:  None = None
        self.__font_bold_14:  None = None
        self.__font_bold_15:  None = None
        self.__font_bold_16:  None = None
        self.__font_bold_18:  None = None
        self.__font_bold_20:  None = None
        self.__font_bold_22:  None = None

        super().__init__()

    def register(self) -> None:
        with dpg.font_registry():
            self.__font_8   = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_8)
            self.__font_9   = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_9)
            self.__font_10  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_10)
            self.__font_11  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_11)
            self.__font_12  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_12)
            self.__font_13  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_13)
            self.__font_14  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_14)
            self.__font_15  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_15)
            self.__font_16  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_16)
            self.__font_18  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_18)
            self.__font_20  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_20)
            self.__font_22  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Regular.ttf"), self.FONT_SIZE_22)


            self.__font_bold_8   = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_8)
            self.__font_bold_9   = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_9)
            self.__font_bold_10  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_10)
            self.__font_bold_11  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_11)
            self.__font_bold_12  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_12)
            self.__font_bold_13  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_13)
            self.__font_bold_14  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_14)
            self.__font_bold_15  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_15)
            self.__font_bold_16  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_16)
            self.__font_bold_18  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_18)
            self.__font_bold_20  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_20)
            self.__font_bold_22  = dpg.add_font(str(self.FONTS_DIR / "OpenSans-Bold.ttf"), self.FONT_SIZE_22)


            logger.success("Registered Fonts — Open Sans Regular + Bold")
        self.__set_global_font()

    def __set_global_font(self) -> None: dpg.bind_font(self.__font_15)

    @property
    def font_8(self)  -> int: return self.__font_8
    @property
    def font_9(self)  -> int: return self.__font_9
    @property
    def font_10(self) -> int: return self.__font_10
    @property
    def font_11(self) -> int: return self.__font_11
    @property
    def font_12(self) -> int: return self.__font_12
    @property
    def font_13(self) -> int: return self.__font_13
    @property
    def font_14(self) -> int: return self.__font_14
    @property
    def font_15(self) -> int: return self.__font_15
    @property
    def font_16(self) -> int: return self.__font_16
    @property
    def font_18(self) -> int: return self.__font_18
    @property
    def font_20(self) -> int: return self.__font_20
    @property
    def font_22(self) -> int: return self.__font_22

    @property
    def font_bold_8(self)  -> int: return self.__font_bold_8
    @property
    def font_bold_9(self)  -> int: return self.__font_bold_9
    @property
    def font_bold_10(self) -> int: return self.__font_bold_10
    @property
    def font_bold_11(self) -> int: return self.__font_bold_11
    @property
    def font_bold_12(self) -> int: return self.__font_bold_12
    @property
    def font_bold_13(self) -> int: return self.__font_bold_13
    @property
    def font_bold_14(self) -> int: return self.__font_bold_14
    @property
    def font_bold_15(self) -> int: return self.__font_bold_15
    @property
    def font_bold_16(self) -> int: return self.__font_bold_16
    @property
    def font_bold_18(self) -> int: return self.__font_bold_18
    @property
    def font_bold_20(self) -> int: return self.__font_bold_20
    @property
    def font_bold_22(self) -> int: return self.__font_bold_22


    def apply(self, component: int | str, font: int) -> None:
        dpg.bind_item_font(component, font)