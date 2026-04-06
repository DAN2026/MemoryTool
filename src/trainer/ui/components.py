import time
import dearpygui.dearpygui as dpg


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
        int(lerp(c1[3], c2[3], t)),
    )


class Toggle:

    # Colours
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
        self.__state = default
        self.__t = 1.0 if default else 0.0
        self.__duration = duration
        self.__last = time.time()
        self.__callback = callback
        self.__width = width
        self.__height = height

        padding = 3
        self.__knob_min = padding
        self.__knob_max = width - height + padding  # knob travel distance

        # ── Draw list acts as the canvas ─────────────────────────────────────
        with dpg.group(horizontal=True, parent=parent):

            self.__drawlist = dpg.add_drawlist(width=width, height=height)

            # Track (rounded rect via circle + rect combo)
            self.__track = dpg.draw_rectangle(
                pmin=(0, 0),
                pmax=(width, height),
                color=(0, 0, 0, 0),
                fill=self.__TRACK_OFF,
                rounding=height / 2,
                parent=self.__drawlist,
            )

            # Knob
            knob_r = (height / 2) - padding
            knob_cx = self.__knob_min + knob_r
            knob_cy = height / 2

            self.__knob = dpg.draw_circle(
                center=(knob_cx, knob_cy),
                radius=knob_r,
                color=(0, 0, 0, 0),
                fill=self.__KNOB_COL,
                parent=self.__drawlist,
            )

            if label:
                dpg.add_text(label)

        # Click handler
        with dpg.item_handler_registry() as handler:
            dpg.add_item_clicked_handler(callback=self.__on_click)
        dpg.bind_item_handler_registry(self.__drawlist, handler)

    def __on_click(self) -> None:
        self.__state = not self.__state
        if self.__callback:
            self.__callback(self.__state)

    def tick(self) -> None:
        now         = time.time()
        delta       = now - self.__last
        self.__last = now

        target    = 1.0 if self.__state else 0.0
        direction = 1 if self.__t < target else -1 if self.__t > target else 0

        if direction != 0:
            self.__t += direction * (delta / self.__duration)
            self.__t  = max(0.0, min(1.0, self.__t))

            # Delete and redraw track
            dpg.delete_item(self.__track)
            track_color  = lerp_color(self.__TRACK_OFF, self.__TRACK_ON, self.__t)
            self.__track = dpg.draw_rectangle(
                pmin=(0, 0),
                pmax=(self.__width, self.__height),
                color=(0, 0, 0, 0),
                fill=track_color,
                rounding=self.__height / 2,
                parent=self.__drawlist
            )

            # Delete and redraw knob
            dpg.delete_item(self.__knob)
            knob_r       = (self.__height / 2) - 3
            knob_cx      = lerp(self.__knob_min + knob_r, self.__knob_max + knob_r, self.__t)
            self.__knob  = dpg.draw_circle(
                center=(knob_cx, self.__height / 2),
                radius=knob_r,
                color=(0, 0, 0, 0),
                fill=self.__KNOB_COL,
                parent=self.__drawlist
            )

    @property
    def value(self) -> bool:
        return self.__state
