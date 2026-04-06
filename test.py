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


class ColorTransition:

    def __init__(
        self,
        target: str | int,
        color_slot: int,
        initial: tuple,
        final: tuple,
        duration: float = 0.2
    ):
        self.__target   = target
        self.__initial  = initial
        self.__final    = final
        self.__duration = duration
        self.__t        = 0.0
        self.__last     = time.time()

        with dpg.theme() as self.__theme:
            with dpg.theme_component(dpg.mvAll):
                self.__color_item = dpg.add_theme_color(color_slot, initial)

        dpg.bind_item_theme(self.__target, self.__theme)

    def tick(self):
        now        = time.time()
        delta      = now - self.__last
        self.__last = now

        hovered   = dpg.is_item_hovered(self.__target)
        direction = 1 if hovered else -1

        # Only advance t if there is still progress to make
        if (direction == 1 and self.__t < 1.0) or (direction == -1 and self.__t > 0.0):
            self.__t += direction * (delta / self.__duration)
            self.__t  = max(0.0, min(1.0, self.__t))
            dpg.set_value(
                self.__color_item,
                lerp_color(self.__initial, self.__final, self.__t)
            )
            
dpg.create_context()
dpg.create_viewport(title="Transition Demo", width=400, height=200)
dpg.setup_dearpygui()

with dpg.window(label="Demo", width=400, height=200, no_title_bar=True):
    dpg.add_spacer(height=40)
    with dpg.child_window(tag="card", width=200, height=80, indent=100, no_scrollbar=True):
        dpg.add_spacer(height=15)
        dpg.add_text("Hover over me", indent=35)

transition = ColorTransition(
    target     = "card",
    color_slot = dpg.mvThemeCol_ChildBg,
    initial    = (45,  45,  48,  255),
    final      = (60,  80,  160, 255),
    duration   = 0.2
)

dpg.show_viewport()

while dpg.is_dearpygui_running():
    transition.tick()
    dpg.render_dearpygui_frame()

dpg.destroy_context()