import time
import dearpygui.dearpygui as dpg

from trainer.ui.animations.lerp import lerp


class UnderlineTransition:

    def __init__(
        self, target: str | int, width: float, color: tuple, duration: float = 0.2
    ):
        self.__target = target
        self.__width = width
        self.__color = color
        self.__duration = duration
        self.__t = 0.0
        self.__last = time.time()

        self.__drawlist = dpg.add_drawlist(width=width, height=4, parent=target)
        self.__line = dpg.draw_line(
            p1=(0, 0),
            p2=(0, 0),
            color=color,
            thickness=2,
            parent=self.__drawlist,
        )

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

        centre = self.__width / 2
        half = lerp(0, self.__width / 2, self.__t)

        dpg.configure_item(
            self.__line,
            p1=(centre - half, 0),
            p2=(centre + half, 0),
        )
