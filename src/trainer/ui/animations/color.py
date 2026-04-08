from typing import List, Tuple, Optional, Union
import time
import dearpygui.dearpygui as dpg

class ColorTransition:
    """
    `ColorTransition` synchronizes background interpolation for nested UI components
    by targeting the parent container while monitoring children for interaction.
    """

    __slots__ = (
        "__target", "__initial", "__final", "__duration",
        "__t", "__last", "__theme", "__color_items", "__related_items"
    )

    def __init__(
        self,
        target: Union[str, int],
        initial: Tuple[int, int, int, int],
        final: Tuple[int, int, int, int],
        duration: float = 0.15,
        related_items: Optional[List[Union[str, int]]] = None
    ) -> None:
        self.__target: Union[str, int] = target
        self.__initial: Tuple[int, int, int, int] = initial
        self.__final: Tuple[int, int, int, int] = final
        self.__duration: float = duration
        self.__related_items: List[Union[str, int]] = related_items or []
        self.__t: float = 0.0
        self.__last: float = time.time()
        self.__color_items: List[int] = []

        with dpg.theme() as self.__theme:
            with dpg.theme_component(dpg.mvAll):
                for slot in [
                    dpg.mvThemeCol_ChildBg, 
                    dpg.mvThemeCol_Header, 
                    dpg.mvThemeCol_FrameBg
                ]:
                    item = dpg.add_theme_color(
                        slot, 
                        initial, 
                        category=dpg.mvThemeCat_Core
                    )
                    self.__color_items.append(item)

                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)

        dpg.bind_item_theme(self.__target, self.__theme)

    def tick(self) -> None:
        now: float = time.time()
        delta: float = now - self.__last
        self.__last = now

        is_hovered: bool = dpg.is_item_hovered(self.__target)
        if not is_hovered:
            for item in self.__related_items:
                if dpg.does_item_exist(item) and dpg.is_item_hovered(item):
                    is_hovered = True
                    break

        direction: int = 1 if is_hovered else -1

        if (direction == 1 and self.__t < 1.0) or (direction == -1 and self.__t > 0.0):
            self.__t += direction * (delta / self.__duration)
            self.__t = max(0.0, min(1.0, self.__t))

            new_color: List[float] = [
                self.__initial[i] + (self.__final[i] - self.__initial[i]) * self.__t
                for i in range(4)
            ]

            for color_item in self.__color_items:
                dpg.set_value(color_item, new_color)