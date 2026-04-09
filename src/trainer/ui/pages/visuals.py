from typing import ClassVar, Dict, List, Tuple, Union, Any, Optional
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.pages.base import BasePage
from trainer.ui.styles import fonts, themes
from trainer.ui.components.toggle import Toggle
from trainer.ui.components.toggle_row import ToggleRowComponent
from trainer.ui.components.slider_row import SliderRowComponent
from trainer.memory.game import ShooterGame
from trainer.ui.animations.color import ColorTransition
from trainer.events.signals import (
    set_ini,
    set_fov,
    set_environment,
    set_beer,
    set_gamma,
    set_mipbias,
    set_testing_ini,
    set_fullbright,
    set_damage_numbers,
    set_stalker_vision,
    set_gamma,
    set_view_distance,
    get_view_distance,
    get_gamma,
    get_fov,
)


class VisualsPage(BasePage):
    """
    VisualsPage implements visual modifications and synchronized row animations.

    This class manages the UI lifecycle for visual settings, emitting signals
    to the memory layer while maintaining UI state and mutual exclusivity.
    """

    __slots__ = (
        "__ARK",
        "__toggles",
        "__transitions",
        "__last_conn_state",
    )

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0
    __ROW_WIDTH: ClassVar[float] = 400.0

    def __init__(self, ark: ShooterGame) -> None:
        """
        Initializes the visuals page with game reference and state tracking.
        """
        self.__ARK: ShooterGame = ark
        self.__toggles: Dict[str, Toggle] = {}
        self.__transitions: List[ColorTransition] = []
        self.__last_conn_state: bool = False

        set_ini.send(self, value=3)
        super().__init__()

    def build(self) -> None:
        """
        Constructs the visuals menu using row components and signals.
        """
        with dpg.child_window(
            tag="visual-container",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12.5,
            show=False,
        ) as visuals:
            dpg.add_spacer(height=10)

            with dpg.group(tag="visual-group-container"):
                # --- INI Presets (Mutual Exclusive) ---
                ToggleRowComponent(
                    "normal_ini", "Normal INI", "folder",
                    callback=lambda s: self.__on_ini_toggle("normal_ini", 3),
                    default_state=True, width=self.__ROW_WIDTH
                ).build(self.__toggles, self.__transitions)

                ToggleRowComponent(
                    "hard_ini", "Hard INI", "folder",
                    callback=lambda s: self.__on_ini_toggle("hard_ini", 1),
                    width=self.__ROW_WIDTH
                ).build(self.__toggles, self.__transitions)


                ToggleRowComponent(
                    "no_water", "No Water", "folder",
                    callback=lambda s: self.__on_ini_toggle("no_water", 6),
                    width=self.__ROW_WIDTH
                ).build(self.__toggles, self.__transitions)

                ToggleRowComponent(
                    "fullbright", "Fullbright", "folder",
                    on_true=lambda: set_fullbright.send(self, state=True),
                    on_false=lambda: set_fullbright.send(self, state=False),
                    width=self.__ROW_WIDTH
                ).build(self.__toggles, self.__transitions)

                ToggleRowComponent(
                    "beer_xz", "Beer / XZ", "folder",
                    on_true=lambda: set_beer.send(self, state=True),
                    on_false=lambda: set_beer.send(self, state=False),
                    width=self.__ROW_WIDTH
                ).build(self.__toggles, self.__transitions)

                ToggleRowComponent(
                    "no_environment", "No Environment", "folder",
                    on_true=lambda: set_environment.send(self, state=True),
                    on_false=lambda: set_environment.send(self, state=False),
                    width=self.__ROW_WIDTH
                ).build(self.__toggles, self.__transitions)
                
                # --- Sliders ---
                SliderRowComponent(
                    "fov", "FOV", 0.0, 2.0, 1.25,
                    lambda s, v: set_fov.send(self, value=v),
                    width=self.__ROW_WIDTH
                ).build(self.__transitions)

                SliderRowComponent(
                    "gamma", "Gamma", 0.0, 5.0, 2.2,
                    lambda s, v: set_gamma.send(self, value=v),
                    width=self.__ROW_WIDTH
                ).build(self.__transitions)

                SliderRowComponent(
                    "view_distance", "View Dist", 0.0, 2.0, 1.0,
                    lambda s, v: set_view_distance.send(self, value=v),
                    width=self.__ROW_WIDTH
                ).build(self.__transitions)

                SliderRowComponent(
                    "test_ini", "Ini Test", 0, 0, 0.0,
                    lambda s, v: set_testing_ini.send(self, value=v),
                    width=self.__ROW_WIDTH
                ).build(self.__transitions)

        themes.apply(visuals, themes.container)
        super().build()

    def __on_ini_toggle(self, clicked_key: str, ini_value: int) -> None:
        """
        Routes toggle clicks and ensures mutual exclusivity for INI presets.
        """
        presets: Tuple[str, ...] = (
            "normal_ini",
            "hard_ini",
            "potato_ini",
            "no_water",
        )

        if self.__toggles[clicked_key].value:
            for key in presets:
                if key != clicked_key:
                    self.__toggles[key].value = False
            set_ini.send(self, value=ini_value)
        else:
            self.__toggles["normal_ini"].value = True
            set_ini.send(self, value=3)

    def __handle_connection_watchdog(self) -> None:
        """
        Monitors ShooterGame connection state and triggers sync on discovery.
        """
        current_conn: bool = self.__ARK.is_connected
        if current_conn != self.__last_conn_state:
            if current_conn:
                logger.info("ShooterGame detected: Active.")
                self.__sync_settings()
            else:
                logger.warning("ShooterGame connection lost: Inactive.")
            self.__last_conn_state = current_conn

    def __sync_settings(self) -> None:
        """
        Reads values from game memory and updates UI components accordingly.
        """
        responses = get_fov.send(self)
        
        game_fov: Optional[float] = responses[0][1] if responses else None

        if game_fov is not None:
            dpg.set_value("fov_slider", game_fov)
            
        responses = get_gamma.send(self)
        
        gamma: Optional[float] = responses[0][1] if responses else None

        if gamma is not None:
            dpg.set_value("gamma_slider", gamma)
            
        responses = get_view_distance.send(self)
        
        view_dist: Optional[float] = responses[0][1] if responses else None

        if view_dist is not None:
            dpg.set_value("view_distance_slider", view_dist)
            

    def tick(self) -> None:
        """
        Synchronizes UI components and handles state-change watchdogs.
        """
        self.__handle_connection_watchdog()

        for toggle in self.__toggles.values():
            toggle.tick()

        for transition in self.__transitions:
            transition.tick()