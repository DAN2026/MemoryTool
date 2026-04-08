from typing import ClassVar, Tuple, List, Union, Any, Callable, Optional
import dearpygui.dearpygui as dpg
from trainer.ui.components.base import BaseComponent
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.animations.color import ColorTransition
from trainer.ui.styles import fonts, themes


class SliderRowComponent(BaseComponent):
    """
    `SliderRowComponent` provides a reusable UI row featuring an icon,
    a label, and a float slider with built-in hover animations.
    """

    __slots__ = (
        "__tag",
        "__label",
        "__icon",
        "__default_val",
        "__min_val",
        "__max_val",
        "__callback",
        "__transition",
    )

    __ROW_HEIGHT: ClassVar[int] = 45
    __WIDTH_OFFSET: ClassVar[int] = 25
    __SLIDER_WIDTH: ClassVar[int] = 250
    __BG_THIRD: ClassVar[Tuple[int, int, int, int]] = (16, 16, 16, 255)
    __BG_HOVER: ClassVar[Tuple[int, int, int, int]] = (28, 28, 28, 255)

    def __init__(
        self,
        tag: str,
        label: str,
        icon: str,
        default_value: float,
        min_value: float,
        max_value: float,
        callback: Callable[[Union[int, str], float], None],
        parent_width: float,
    ) -> None:
        """
        Initializes the slider row with configuration and state tracking.
        """
        self.__tag: str = tag
        self.__label: str = label
        self.__icon: str = icon
        self.__default_val: float = default_value
        self.__min_val: float = min_value
        self.__max_val: float = max_value
        self.__callback: Callable = callback
        self.__parent_width: float = parent_width
        self.__transition: Optional[ColorTransition] = None
        super().__init__()

    def build(self) -> None:
        """
        Constructs the row layout and initializes the color transition.
        """
        icon_tag: str = f"icon_{self.__tag}"
        text_tag: str = f"label_{self.__tag}"
        slider_tag: str = f"{self.__tag}_slider"

        with dpg.child_window(
            tag=self.__tag,
            width=self.__parent_width - self.__WIDTH_OFFSET,
            height=self.__ROW_HEIGHT,
            border=False,
            no_scrollbar=True,
            indent=5.0,
        ):
            with dpg.group(horizontal=True):
                IconButtonComponent(
                    tag=icon_tag,
                    icon_name=self.__icon,
                    width=40,
                    height=40,
                    icon_size=22,
                    x_indent=9,
                    y_indent=9,
                    theme=themes.visuals_item,
                ).build()

                TextComponent(
                    tag=text_tag,
                    text=self.__label,
                    width=60,
                    height=40,
                    y_indent=10,
                    font=fonts.font_bold_18,
                    theme=themes.visuals_item,
                ).build()

                with dpg.group():
                    dpg.add_spacer(height=7.5)
                    slider = dpg.add_slider_float(
                        tag=slider_tag,
                        width=self.__SLIDER_WIDTH,
                        default_value=self.__default_val,
                        min_value=self.__min_val,
                        max_value=self.__max_val,
                        callback=self.__callback,
                    )
                    themes.apply(slider, themes.slider_float_theme)

        self.__transition = ColorTransition(
            target=self.__tag,
            initial=self.__BG_THIRD,
            final=self.__BG_HOVER,
            related_items=[icon_tag, text_tag, slider_tag],
        )

    def tick(self) -> None:
        """
        Updates the hover transition animation.
        """
        if self.__transition:
            self.__transition.tick()