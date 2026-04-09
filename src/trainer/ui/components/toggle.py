from typing import Callable, Optional, List, Tuple, Any, Union
import dearpygui.dearpygui as dpg
import time
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.common.math import Math


class Toggle(BaseComponent):
    """
    A custom animated toggle switch component.
    Supports specific callbacks for true and false states.
    """

    __slots__ = (
        "__parent",
        "__label",
        "__is_enabled",
        "__animation_progress",
        "__animation_duration",
        "__last_frame_time",
        "__on_change_callback",
        "__on_true_callback",
        "__on_false_callback",
        "__width",
        "__height",
        "__knob_start_x",
        "__knob_end_x",
        "__knob_radius",
        "__drawlist_tag",
        "__track_tag",
        "__knob_tag",
        "__handler_registry",
        "__pos",
    )

    __TRACK_OFF_COLOR: Tuple[int, int, int, int] = (40, 40, 40, 255)
    __TRACK_ON_COLOR: Tuple[int, int, int, int] = (1, 180, 240, 255)
    __KNOB_COLOR: Tuple[int, int, int, int] = (255, 255, 255, 255)

    def __init__(
        self,
        parent: Union[str, int],
        label: str = "",
        default_state: bool = False,
        animation_duration: float = 0.15,
        callback: Optional[Callable[[bool], None]] = None,
        on_true: Optional[Callable[[], None]] = None,
        on_false: Optional[Callable[[], None]] = None,
        width: int = 44,
        height: int = 24,
        pos: Optional[Union[List[float], Tuple[float, float], float]] = None,
    ) -> None:
        """
        Args:
            on_true: Callback triggered when toggle state becomes True.
            on_false: Callback triggered when toggle state becomes False.
        """
        super().__init__()

        self.__parent: Union[str, int] = parent
        self.__label: str = label
        self.__is_enabled: bool = default_state
        self.__animation_progress: float = 1.0 if default_state else 0.0
        self.__animation_duration: float = animation_duration
        self.__last_frame_time: float = time.time()
        self.__on_change_callback: Optional[Callable[[bool], None]] = callback
        self.__on_true_callback: Optional[Callable[[], None]] = on_true
        self.__on_false_callback: Optional[Callable[[], None]] = on_false
        self.__width: int = width
        self.__height: int = height
        self.__pos: Optional[Union[List[float], Tuple[float, float], float]] = pos

        padding: int = 3
        self.__knob_start_x: float = float(padding)
        self.__knob_end_x: float = float(width - height + padding)
        self.__knob_radius: float = (height / 2.0) - padding

    def build(self) -> None:
        """
        Constructs the visual primitives.
        """
        with dpg.group(parent=self.__parent):
            if isinstance(self.__pos, (list, tuple)) and len(self.__pos) >= 2:
                if self.__pos[1] > 0:
                    dpg.add_spacer(height=self.__pos[1])

            with dpg.group(horizontal=True):
                if isinstance(self.__pos, (int, float)):
                    dpg.add_spacer(width=self.__pos)
                elif isinstance(self.__pos, (list, tuple)) and len(self.__pos) >= 1:
                    if self.__pos[0] > 0:
                        dpg.add_spacer(width=self.__pos[0])

                self.__drawlist_tag = dpg.add_drawlist(
                    width=self.__width, height=self.__height
                )

                self.__track_tag = dpg.draw_rectangle(
                    pmin=(0, 0),
                    pmax=(self.__width, self.__height),
                    color=(0, 0, 0, 0),
                    fill=self.__TRACK_ON_COLOR
                    if self.__is_enabled
                    else self.__TRACK_OFF_COLOR,
                    rounding=self.__height / 2.0,
                    parent=self.__drawlist_tag,
                )

                initial_knob_x: float = (
                    self.__knob_end_x if self.__is_enabled else self.__knob_start_x
                ) + self.__knob_radius

                self.__knob_tag = dpg.draw_circle(
                    center=(initial_knob_x, self.__height / 2.0),
                    radius=self.__knob_radius,
                    color=(0, 0, 0, 0),
                    fill=self.__KNOB_COLOR,
                    parent=self.__drawlist_tag,
                )

        self.__handler_registry = dpg.add_item_handler_registry()
        dpg.add_item_clicked_handler(
            parent=self.__handler_registry, callback=self.__handle_interaction
        )
        dpg.bind_item_handler_registry(self.__drawlist_tag, self.__handler_registry)

        super().build()

    def __handle_interaction(self, *args: Any) -> None:
        """
        Handles state changes and routes callbacks.
        """
        self.value = not self.__is_enabled
        logger.debug(f"Toggle `{self.__label}` switched to: {self.__is_enabled}")

        if self.__on_change_callback:
            self.__on_change_callback(self.__is_enabled)

        if self.__is_enabled and self.__on_true_callback:
            self.__on_true_callback()
        elif not self.__is_enabled and self.__on_false_callback:
            self.__on_false_callback()

    def tick(self) -> None:
        """
        Handles animation updates.
        """
        current_time: float = time.time()
        delta_time: float = current_time - self.__last_frame_time
        self.__last_frame_time = current_time

        target_progress: float = 1.0 if self.__is_enabled else 0.0

        if abs(self.__animation_progress - target_progress) > 0.001:
            step: int = 1 if self.__animation_progress < target_progress else -1
            self.__animation_progress += step * (delta_time / self.__animation_duration)
            self.__animation_progress = max(0.0, min(1.0, self.__animation_progress))

            current_track_color = Math.lerp_color(
                self.__TRACK_OFF_COLOR,
                self.__TRACK_ON_COLOR,
                self.__animation_progress,
            )
            dpg.configure_item(self.__track_tag, fill=current_track_color)

            current_knob_x = Math.lerp(
                self.__knob_start_x + self.__knob_radius,
                self.__knob_end_x + self.__knob_radius,
                self.__animation_progress,
            )
            dpg.configure_item(
                self.__knob_tag, center=(current_knob_x, self.__height / 2.0)
            )

    @property
    def value(self) -> bool:
        """
        Returns the current enabled state.
        """
        return self.__is_enabled

    @value.setter
    def value(self, new_state: bool) -> None:
        """
        Sets the enabled state.
        """
        if self.__is_enabled != new_state:
            self.__is_enabled = new_state