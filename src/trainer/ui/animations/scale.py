import time
import dearpygui.dearpygui as dpg

from trainer.ui.animations.lerp import lerp


class ScaleTransition:

    def __init__(
        self,
        target: str | int,
        base_w: int,
        base_h: int,
        scale: float = 1.2,
        duration: float = 0.15,
    ):
        self.__target = target
        self.__base_w = base_w
        self.__base_h = base_h
        self.__final_w = int(base_w * scale)
        self.__final_h = int(base_h * scale)
        self.__duration = duration
        self.__t = 0.0
        self.__last = time.time()

    def tick(self):
        now = time.time()
        delta = now - self.__last
        self.__last = now

        hovered = dpg.is_item_hovered(self.__target)
        direction = 1 if hovered else -1

        if direction == 1 and self.__t >= 1.0:
            return
        if direction == -1 and self.__t <= 0.0:
            return

        self.__t += direction * (delta / self.__duration)
        self.__t = max(0.0, min(1.0, self.__t))

        w = int(lerp(self.__base_w, self.__final_w, self.__t))
        h = int(lerp(self.__base_h, self.__final_h, self.__t))

        dpg.configure_item(self.__target, width=w, height=h)
