from typing import Dict, List, Tuple, Callable, Union, Any
import dearpygui.dearpygui as dpg
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.animations.color import ColorTransition
from trainer.ui.styles import fonts, themes


class SliderRowComponent:
    """
    SliderRowComponent encapsulates a standardized UI row containing an icon,
    a label, and a float slider with built-in hover transitions.
    """

    __slots__ = (
        "__tag",
        "__key",
        "__label",
        "__min",
        "__max",
        "__default",
        "__callback",
        "__width",
        "__height",
        "__padding_left",
        "__padding_bottom",
        "__bg_color",
        "__hover_color",
    )

    DEFAULT_WIDTH: float = 400.0
    DEFAULT_HEIGHT: int = 45
    DEFAULT_PADDING_LEFT: float = 5.0
    DEFAULT_PADDING_BOTTOM: float = 5.0
    DEFAULT_BG: Tuple[int, int, int, int] = (16, 16, 16, 255)
    DEFAULT_HOVER: Tuple[int, int, int, int] = (28, 28, 28, 255)

    def __init__(
        self,
        key: str,
        label: str,
        v_min: float,
        v_max: float,
        default: float,
        callback: Callable[[Union[int, str], float], None],
        width: float = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        padding_left: float = DEFAULT_PADDING_LEFT,
        padding_bottom: float = DEFAULT_PADDING_BOTTOM,
        bg_color: Tuple[int, int, int, int] = DEFAULT_BG,
        hover_color: Tuple[int, int, int, int] = DEFAULT_HOVER,
    ) -> None:
        """
        Initializes the slider row with configurable range and styling.
        """
        self.__key: str = key
        self.__label: str = label
        self.__min: float = v_min
        self.__max: float = v_max
        self.__default: float = default
        self.__callback: Callable[[Union[int, str], float], None] = callback
        self.__width: float = width
        self.__height: int = height
        self.__padding_left: float = padding_left
        self.__padding_bottom: float = padding_bottom
        self.__bg_color: Tuple[int, int, int, int] = bg_color
        self.__hover_color: Tuple[int, int, int, int] = hover_color
        self.__tag: str = f"row_{key}"

    def build(self, transition_list: List[ColorTransition]) -> None:
        """
        Constructs the row elements and registers the animation transition.
        """
        icon_tag: str = f"icon_{self.__key}_row"
        text_tag: str = f"label_{self.__key}_row"
        slider_tag: str = f"{self.__key}_slider"

        with dpg.child_window(
            tag=self.__tag,
            width=self.__width,
            height=self.__height,
            border=False,
            no_scrollbar=True,
            indent=self.__padding_left,
        ):
            with dpg.group(horizontal=True):
                IconButtonComponent(
                    tag=icon_tag,
                    icon_name="folder",
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
                        width=250,
                        default_value=self.__default,
                        min_value=self.__min,
                        max_value=self.__max,
                        callback=self.__callback,
                    )
                    themes.apply(slider, themes.slider_float_theme)

        transition_list.append(
            ColorTransition(
                target=self.__tag,
                initial=self.__bg_color,
                final=self.__hover_color,
                related_items=[icon_tag, text_tag, slider_tag],
            )
        )
        dpg.add_spacer(height=self.__padding_bottom)