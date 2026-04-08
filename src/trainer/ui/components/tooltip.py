from typing import Optional, List
import dearpygui.dearpygui as dpg
from trainer.ui.components.base import BaseComponent


class TooltipComponent(BaseComponent):
    """
    `TooltipComponent` creates a contextual information window linked to a parent item.
    """

    __slots__ = (
        "__tag",
        "__parent",
        "__text",
        "__width",
        "__height",
        "__theme",
        "__font",
    )

    def __init__(
        self,
        tag: str,
        parent: str,
        text: str,
        width: float,
        height: float,
        theme: Optional[int] = None,
        font: Optional[int] = None,
    ) -> None:
        """
        Initializes the tooltip component properties linked to a parent tag.
        """
        self.__tag: str = tag
        self.__parent: str = parent
        self.__text: str = text
        self.__width: float = width
        self.__height: float = height
        self.__theme: Optional[int] = theme
        self.__font: Optional[int] = font
        super().__init__()

    def build(self) -> None:
        """
        Constructs the tooltip as a child of the parent item to respect its bounds.
        """
        with dpg.tooltip(parent=self.__parent, tag=self.__tag):
            with dpg.group(horizontal=False):
                dpg.add_text(
                    self.__text, 
                    tag=f"{self.__tag}_text", 
                    wrap=int(self.__width) - 10
                )

        if self.__theme:
            dpg.bind_item_theme(self.__tag, self.__theme)

        if self.__font:
            dpg.bind_item_font(f"{self.__tag}_text", self.__font)

        dpg.configure_item(self.__tag, width=self.__width, height=self.__height)
        super().build()

    def set_text(self, text: str) -> None:
        """
        Updates the text content of the tooltip.
        """
        dpg.set_value(f"{self.__tag}_text", text)

    def toggle(self, show: bool) -> None:
        """
        Manually triggers tooltip visibility.
        """
        if show:
            dpg.show_item(self.__tag)
        else:
            dpg.hide_item(self.__tag)

    def tick(self) -> None:
        """
        Reserved for frame-based logic.
        """
        pass