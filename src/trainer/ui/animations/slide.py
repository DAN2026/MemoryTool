import time
import dearpygui.dearpygui as dpg

from trainer.ui.animations.lerp import lerp


class SlideTransition:

    def __init__(
        self,
        target: str | int,
        active_x: float,
        offscreen_x: float,
        y: float,
        duration: float = 0.25,
    ):
        self.__target = target
        self.__active_x = active_x
        self.__offscreen_x = offscreen_x
        self.__y = y
        self.__duration = duration
        self.__t = 0.0
        self.__active = False
        self.__last = time.time()

    def set_state(self, active: bool):
        self.__active = active
        dpg.configure_item(self.__target, show=True)

    def tick(self):
        now = time.time()
        delta = now - self.__last
        self.__last = now

        direction = 1 if self.__active else -1

        if direction == 1 and self.__t >= 1.0:
            return
        if direction == -1 and self.__t <= 0.0:
            return

        self.__t += direction * (delta / self.__duration)
        self.__t = max(0.0, min(1.0, self.__t))

        current_x = lerp(self.__offscreen_x, self.__active_x, self.__t)
        dpg.set_item_pos(self.__target, [current_x, self.__y])

        if self.__t <= 0.0 and not self.__active:
            dpg.configure_item(self.__target, show=False)
