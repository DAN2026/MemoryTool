from typing import List, Optional, Union
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.styles import themes, fonts


class TextComponent(BaseComponent):
    """
    A customizable text component encapsulated within a `child_window`.

    Supports optional positioning; if no position is provided, it respects
    the layout flow of its parent container.
    """

    __slots__ = (
        "__tag",
        "__text",
        "__pos",
        "__width",
        "__height",
        "__y_indent",
        "__theme",
        "__font",
        "__color",
        "__show",
    )

    def __init__(
        self,
        tag: str,
        text: str,
        width: float,
        height: float,
        pos: Optional[List[float]] = None,
        y_indent: float = 0.0,
        show: bool = True,
        theme: Optional[Union[int, str]] = None,
        font: Optional[Union[int, str]] = None,
        color: Optional[List[int]] = None,
    ) -> None:
        """
        Initializes the TextComponent.
        """
        self.__tag: str = tag
        self.__text: str = text
        self.__pos: Optional[List[float]] = pos
        self.__width: float = width
        self.__height: float = height
        self.__y_indent: float = y_indent
        self.__show: bool = show
        self.__theme: Optional[Union[int, str]] = theme
        self.__font: Optional[Union[int, str]] = font
        self.__color: Optional[List[int]] = color

        super().__init__()

    def build(self) -> None:
        """
        Constructs the text element inside a child window.
        """
        try:
            with dpg.child_window(
                tag=self.__tag,
                width=self.__width,
                height=self.__height,
                border=False,
                no_scrollbar=True,
                no_scroll_with_mouse=True,
                show=self.__show,
            ) as container:

                if self.__pos is not None:
                    dpg.set_item_pos(container, self.__pos)

                if self.__theme:
                    themes.apply(container, self.__theme)

                text_item = dpg.add_text(
                    default_value=self.__text,
                    tag=f"{self.__tag}_label",
                    color=self.__color if self.__color else (-1, -1, -1, -1),
                )

                dpg.set_item_pos(text_item, [0, self.__y_indent])

                if self.__font:
                    fonts.apply(text_item, self.__font)

            super().build()

        except Exception as e:
            logger.error(f"Failed to build `TextComponent` [{self.__tag}]: {e}")
            raise e

    def tick(self) -> None:
        """
        Static visual component update logic.
        """
        pass

    def toggle(self, show: bool) -> None:
        """
        Updates the visibility of the component.
        """
        self.__show = show
        if dpg.does_item_exist(self.__tag):
            dpg.configure_item(self.__tag, show=show)

    def set_pos(self, pos: List[float]) -> None:
        """
        Updates the container position.
        """
        self.__pos = pos
        if dpg.does_item_exist(self.__tag):
            dpg.set_item_pos(self.__tag, pos)

    def set_y_indent(self, y_indent: float) -> None:
        """
        Updates the vertical offset of the text within the container.
        """
        self.__y_indent = y_indent
        label_tag = f"{self.__tag}_label"
        if dpg.does_item_exist(label_tag):
            dpg.set_item_pos(label_tag, [0, y_indent])

    def set_text(self, text: str) -> None:
        """
        Updates the internal text value.
        """
        self.__text = text
        label_tag = f"{self.__tag}_label"
        if dpg.does_item_exist(label_tag):
            dpg.set_value(label_tag, text)

    @property
    def tag(self) -> str:
        """
        Returns the unique tag identifier.
        """
        return self.__tag

    @property
    def pos(self) -> Optional[List[float]]:
        """
        Returns the current [x, y] position.
        """
        return self.__pos