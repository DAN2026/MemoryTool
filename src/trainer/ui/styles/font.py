from pathlib import Path
from typing import ClassVar, Optional, Union
from trainer.ui.styles.base import BaseStyle
from loguru import logger
import dearpygui.dearpygui as dpg


class Fonts(BaseStyle):
    """
    `Fonts` manages the registration and application of Open Sans typography 
    within the Dear PyGui context.
    """

    FONTS_DIR: ClassVar[Path] = Path(__file__).parent / "fonts" / "Open_Sans" / "static"

    FONT_SIZE_16: ClassVar[int] = 16
    FONT_SIZE_18: ClassVar[int] = 18
    FONT_SIZE_20: ClassVar[int] = 20
    FONT_SIZE_22: ClassVar[int] = 22

    __slots__ = (
        "__font_16", "__font_18", "__font_20", "__font_22",
        "__font_bold_16", "__font_bold_18", "__font_bold_20", "__font_bold_22"
    )

    def __init__(self) -> None:
        self.__font_16: Optional[int] = None
        self.__font_18: Optional[int] = None
        self.__font_20: Optional[int] = None
        self.__font_22: Optional[int] = None

        self.__font_bold_16: Optional[int] = None
        self.__font_bold_18: Optional[int] = None
        self.__font_bold_20: Optional[int] = None
        self.__font_bold_22: Optional[int] = None

        super().__init__()

    def register(self) -> None:
        """
        Loads font files into the DPG font registry and binds the default application font.
        """
        reg_path: str = str(self.FONTS_DIR / "OpenSans-Regular.ttf")
        bold_path: str = str(self.FONTS_DIR / "OpenSans-Bold.ttf")

        with dpg.font_registry():
            self.__font_16 = dpg.add_font(reg_path, self.FONT_SIZE_16)
            self.__font_18 = dpg.add_font(reg_path, self.FONT_SIZE_18)
            self.__font_20 = dpg.add_font(reg_path, self.FONT_SIZE_20)
            self.__font_22 = dpg.add_font(reg_path, self.FONT_SIZE_22)

            self.__font_bold_16 = dpg.add_font(bold_path, self.FONT_SIZE_16)
            self.__font_bold_18 = dpg.add_font(bold_path, self.FONT_SIZE_18)
            self.__font_bold_20 = dpg.add_font(bold_path, self.FONT_SIZE_20)
            self.__font_bold_22 = dpg.add_font(bold_path, self.FONT_SIZE_22)

            logger.success("Registered Fonts — Open Sans Regular + Bold (16pt-22pt)")

        self.__set_global_font()

    def __set_global_font(self) -> None:
        """
        Binds the primary font size for the entire application.
        """
        dpg.bind_font(self.__font_16)

    @property
    def font_16(self) -> int:
        return self.__font_16

    @property
    def font_18(self) -> int:
        return self.__font_18

    @property
    def font_20(self) -> int:
        return self.__font_20

    @property
    def font_22(self) -> int:
        return self.__font_22

    @property
    def font_bold_16(self) -> int:
        return self.__font_bold_16

    @property
    def font_bold_18(self) -> int:
        return self.__font_bold_18

    @property
    def font_bold_20(self) -> int:
        return self.__font_bold_20

    @property
    def font_bold_22(self) -> int:
        return self.__font_bold_22

    def apply(self, component: Union[int, str], font: int) -> None:
        """
        Binds a specific font handle to a UI component.
        """
        dpg.bind_item_font(component, font)