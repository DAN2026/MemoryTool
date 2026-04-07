from loguru import logger
from trainer.ui.components.base import BaseComponent
from trainer.ui.common.math import Math
import dearpygui.dearpygui as dpg
import time

class Toggle(BaseComponent):

    __TRACK_OFF = (60, 60, 60, 255)
    __TRACK_ON = (0, 149, 255, 255)
    __KNOB_COL = (255, 255, 255, 255)

    def __init__(
        self,
        parent: str | int,
        label: str = "",
        default: bool = False,
        duration: float = 0.15,
        callback: callable = None,
        width: int = 44,
        height: int = 24,
    ):
        super().__init__()
        
        self.__parent = parent
        self.__label = label
        self.__state = default
        self.__t = 1.0 if default else 0.0
        self.__duration = duration
        self.__last = time.time()
        self.__callback = callback
        self.__width = width
        self.__height = height

        padding = 3
        self.__knob_min = padding
        self.__knob_max = width - height + padding
        self.__knob_r = (height / 2) - padding

    def build(self) -> None:
        """Constructs the UI elements and handlers"""
        
        with dpg.group(horizontal=True, parent=self.__parent):
            
            self.__drawlist = dpg.add_drawlist(width=self.__width, height=self.__height)

            self.__track = dpg.draw_rectangle(
                pmin=(0, 0),
                pmax=(self.__width, self.__height),
                color=(0, 0, 0, 0),
                fill=self.__TRACK_ON if self.__state else self.__TRACK_OFF,
                rounding=self.__height / 2,
                parent=self.__drawlist,
            )

            knob_cx = (self.__knob_max if self.__state else self.__knob_min) + self.__knob_r
            
            self.__knob = dpg.draw_circle(
                center=(knob_cx, self.__height / 2),
                radius=self.__knob_r,
                color=(0, 0, 0, 0),
                fill=self.__KNOB_COL,
                parent=self.__drawlist,
            )

            # if self.__label:
            #     dpg.add_text(self.__label)

        self.__handler_registry = dpg.add_item_handler_registry()
        
        dpg.add_item_clicked_handler(
            parent=self.__handler_registry, 
            callback=self.__on_click
        )
        
        dpg.bind_item_handler_registry(self.__drawlist, self.__handler_registry)

        super().build()

    def __on_click(self, sender, app_data, *args) -> None:
        self.__state = not self.__state
        logger.debug(f"Toggle '{self.__label}' changed: {self.__state}")
        
        if self.__callback:
            self.__callback(self.__state)

    def tick(self) -> None:
        """Processes the visual lerp animation"""
        now = time.time()
        delta = now - self.__last
        self.__last = now

        target = 1.0 if self.__state else 0.0
        
        if abs(self.__t - target) > 0.001:
            direction = 1 if self.__t < target else -1
            self.__t += direction * (delta / self.__duration)
            self.__t = max(0.0, min(1.0, self.__t))

            track_color = Math.lerp_color(self.__TRACK_OFF, self.__TRACK_ON, self.__t)
            dpg.configure_item(self.__track, fill=track_color)

            knob_cx = Math.lerp(
                self.__knob_min + self.__knob_r, 
                self.__knob_max + self.__knob_r, 
                self.__t
            )
            dpg.configure_item(self.__knob, center=(knob_cx, self.__height / 2))

    @property
    def value(self) -> bool:
        return self.__state
    
    def get_value(self) -> bool:
        """Returns the current state of the toggle."""
        return self.__state

    def set_value(self, value: bool):
        """Sets the toggle state and lets tick() handle the animation."""
        if self.__state == value:
            return
            
        self.__state = value