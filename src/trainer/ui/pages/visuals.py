from typing import ClassVar, Dict, List, Tuple, Callable, Optional, Union, Any
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.pages.base import BasePage
from trainer.ui.styles import fonts, themes
from trainer.ui.components.toggle import Toggle
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.memory.game import ShooterGame
from trainer.ui.animations.color import ColorTransition


class VisualsPage(BasePage):
    """
    VisualsPage implements visual modifications and synchronized row animations.

    This class manages the UI lifecycle for visual settings, including 
    the creation of toggle and slider rows, state synchronization with game 
    memory, and color transition animations for interactive elements.
    """

    __slots__ = (
        "__ARK",
        "__toggles",
        "__transitions",
        "__last_conn_state",
        "__last_env_state",
    )

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0
    __ITEM_LEFT_PADDING: ClassVar[float] = 5.0
    __ITEM_PADDING_BOTTOM: ClassVar[float] = 5.0
    __ROW_HEIGHT: ClassVar[int] = 45
    __BG_THIRD: ClassVar[Tuple[int, int, int, int]] = (16, 16, 16, 255)
    __BG_HOVER: ClassVar[Tuple[int, int, int, int]] = (28, 28, 28, 255)

    ENV_ENABLED_VAL: ClassVar[float] = 290.669
    ENV_DISABLED_VAL: ClassVar[float] = 9.401001429934889e-38

    TOGGLES_CONFIG: ClassVar[List[Tuple[str, str, str]]] = [
        ("normal_ini", "Normal INI", "folder"),
        ("hard_ini", "Hard INI", "folder"),
        ("potato_ini", "Potato INI", "folder"),
        ("no_water", "No Water", "folder"),
        ("fullbright", "Fullbright", "folder"),
        ("beer_xz", "Beer / XZ", "folder"),
        ("damage_numbers", "Damage Numbers", "folder"),
        ("stalker_vision", "Stalker Vision", "folder"),
        ("no_environment", "No Environment", "folder"),
    ]

    def __init__(self, ark: ShooterGame) -> None:
        """
        Initializes the visuals page with game reference and state tracking.

        Args:
            ark (ShooterGame): The game memory controller instance.
        """
        self.__ARK: ShooterGame = ark
        self.__toggles: Dict[str, Toggle] = {}
        self.__transitions: List[ColorTransition] = []
        self.__last_conn_state: bool = False
        self.__last_env_state: bool = False

        logger.success(f"Initial env value is: {self.__ARK.environment.get()}")
        self.__apply_normal_ini()
        super().__init__()

    @property
    def SLIDERS_CONFIG(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns the configuration mapping for all slider-based rows.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary where keys are slider IDs 
                and values contain `label`, `min`, `max`, `default`, 
                and the `callback` function.
        """
        return {
            "fov": {
                "label": "FOV",
                "min": 0.0,
                "max": 2.0,
                "default": 1.25,
                "callback": self.__apply_fov,
            },
            "gamma": {
                "label": "Gamma",
                "min": 0.0,
                "max": 5.0,
                "default": 2.2,
                "callback": self.__apply_gamma,
            },
            "view_distance": {
                "label": "View Dist",
                "min": 0.1,
                "max": 10.0,
                "default": 1.0,
                "callback": self.__apply_view_distance,
            },
            "test_ini": {
                "label": "Ini Test",
                "min": 0.1,
                "max": 1000.0,
                "default": 0.0,
                "callback": self.__apply_test_ini,
            },
        }

    def build(self) -> None:
        """
        Constructs the visuals menu components using metadata and mappings.
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
                for key, label, icon in self.TOGGLES_CONFIG:
                    self.__build_toggle_row(key, label, icon)

                for key, cfg in self.SLIDERS_CONFIG.items():
                    self.__build_slider_row(
                        key,
                        cfg["label"],
                        cfg["min"],
                        cfg["max"],
                        cfg["default"],
                        cfg["callback"],
                    )

        themes.apply(visuals, themes.container)
        super().build()

    def __build_toggle_row(self, key: str, label: str, icon: str) -> None:
        """
        Helper to construct standardized toggle rows.
        """
        row_tag: str = f"row_{key}"
        icon_tag: str = f"icon_{key}"
        text_tag: str = f"label_{key}"

        with dpg.child_window(
            tag=row_tag,
            width=self.__WIDTH - 25,
            height=self.__ROW_HEIGHT,
            border=False,
            no_scrollbar=True,
            indent=self.__ITEM_LEFT_PADDING,
        ):
            with dpg.group(horizontal=True):
                IconButtonComponent(
                    tag=icon_tag,
                    icon_name=icon,
                    width=40,
                    height=40,
                    icon_size=22,
                    x_indent=9,
                    y_indent=9,
                    theme=themes.visuals_item,
                ).build()

                TextComponent(
                    tag=text_tag,
                    text=label,
                    width=600,
                    height=40,
                    y_indent=10,
                    font=fonts.font_bold_18,
                    theme=themes.visuals_item,
                ).build()

                self.__toggles[key] = Toggle(
                    parent=dpg.last_container(),
                    label=f"##toggle_{key}",
                    default_state=(key == "normal_ini"),
                    width=44,
                    height=24,
                    pos=[270, 5.5],
                    callback=lambda state, k=key: self.__on_toggle_clicked(k, state),
                )
                self.__toggles[key].build()

        self.__transitions.append(
            ColorTransition(
                target=row_tag,
                initial=self.__BG_THIRD,
                final=self.__BG_HOVER,
                related_items=[icon_tag, text_tag],
            )
        )
        dpg.add_spacer(height=self.__ITEM_PADDING_BOTTOM)

    def __build_slider_row(
        self,
        key: str,
        label: str,
        v_min: float,
        v_max: float,
        default: float,
        callback: Callable[[Union[int, str], float], None],
    ) -> None:
        """
        Helper to construct standardized slider rows via mapping.
        """
        row_tag: str = f"row_{key}"
        icon_tag: str = f"icon_{key}_row"
        text_tag: str = f"label_{key}_row"
        slider_tag: str = f"{key}_slider"

        with dpg.child_window(
            tag=row_tag,
            width=self.__WIDTH - 25,
            height=self.__ROW_HEIGHT,
            border=False,
            no_scrollbar=True,
            indent=self.__ITEM_LEFT_PADDING,
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
                    text=label,
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
                        default_value=default,
                        min_value=v_min,
                        max_value=v_max,
                        callback=lambda s, d: callback(s, d),
                    )
                    themes.apply(slider, themes.slider_float_theme)

        self.__transitions.append(
            ColorTransition(
                target=row_tag,
                initial=self.__BG_THIRD,
                final=self.__BG_HOVER,
                related_items=[icon_tag, text_tag, slider_tag],
            )
        )
        dpg.add_spacer(height=self.__ITEM_PADDING_BOTTOM)

    def __on_toggle_clicked(self, clicked_key: str, state: bool) -> None:
        """
        Routes toggle clicks and ensures mutual exclusivity for INI presets.
        """
        ini_presets: Dict[str, Callable[[], None]] = {
            "normal_ini": self.__apply_normal_ini,
            "hard_ini": self.__apply_hard_ini,
            "potato_ini": self.__apply_potato_ini,
            "no_water": self.__apply_no_water,
        }
        if clicked_key in ini_presets:
            self.__handle_conflicting_toggles(clicked_key, ini_presets)
        else:
            self.__handle_utility_toggles(clicked_key, state)

    def __handle_conflicting_toggles(
        self, clicked_key: str, presets: Dict[str, Callable[[], None]]
    ) -> None:
        """
        Ensures only one INI preset is active at a time.
        """
        if self.__toggles[clicked_key].value:
            for key in presets:
                if key != clicked_key:
                    self.__toggles[key].value = False
            presets[clicked_key]()
        else:
            self.__toggles["normal_ini"].value = True
            self.__apply_normal_ini()

    def __handle_utility_toggles(self, key: str, state: bool) -> None:
        """
        Handles standalone visual features that do not conflict with presets.
        """
        if key == "damage_numbers":
            self.__apply_damage_numbers(state)
        elif key == "stalker_vision":
            self.__apply_stalker_vision(state)

    def __apply_normal_ini(self) -> None:
        """
        Reverts game to standard visual settings.
        """
        self.__ARK.ini.set(3)

    def __apply_hard_ini(self) -> None:
        """
        Applies competitive visual settings to the game memory.
        """
        self.__ARK.ini.set(1)

    def __apply_potato_ini(self) -> None:
        """
        Applies extreme performance settings.
        """
        logger.info("Potato INI activated.")

    def __apply_no_water(self) -> None:
        """
        Disables water rendering for visibility in game memory.
        """
        self.__ARK.ini.set(6)

    def __apply_damage_numbers(self, state: bool) -> None:
        """
        Enables or disables damage numbers in game memory.
        """
        self.__ARK.damage_numbers.set(state)

    def __apply_stalker_vision(self, state: bool) -> None:
        """
        Enables or disables stalker vision in game memory.
        """
        self.__ARK.stalker_vision.set(state)

    def __apply_fov(self, sender: Union[int, str], app_data: float) -> None:
        """
        Writes the new Field of View value to game memory.
        """
        self.__ARK.fov.set(app_data)

    def __apply_test_ini(self, sender: Union[int, str], app_data: float) -> None:
        """
        Writes the Test INI value to game memory.
        """
        self.__ARK.testing_ini.set(app_data)

    def __apply_gamma(self, sender: Union[int, str], app_data: float) -> None:
        """
        Updates game Gamma via log.
        """

    def __apply_view_distance(self, sender: Union[int, str], app_data: float) -> None:
        """
        Updates game View Distance via log.
        """

    def __sync_settings(self) -> None:
        """
        Reads values from game memory and updates UI components accordingly.
        """
        game_fov: Optional[float] = self.__ARK.fov.get()
        if game_fov is not None:
            dpg.set_value("fov_slider", game_fov)

        ini_keys: Tuple[str, ...] = ("normal_ini", "hard_ini", "potato_ini", "no_water")
        for key in ini_keys:
            if key in self.__toggles:
                self.__toggles[key].value = (key == "normal_ini")

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

    def __handle_environment_watchdog(self) -> None:
        """
        Monitors environment toggle and writes to memory only on state change.
        """
        if "no_environment" not in self.__toggles:
            return

        env_state: bool = self.__toggles["no_environment"].value

        if env_state != self.__last_env_state:
            value: float = self.ENV_ENABLED_VAL if env_state else self.ENV_DISABLED_VAL
            self.__ARK.environment.set(value)
            self.__last_env_state = env_state

    def tick(self) -> None:
        """
        Synchronizes UI components and handles state-change watchdogs.
        """
        self.__handle_connection_watchdog()
        self.__handle_environment_watchdog()

        for toggle in self.__toggles.values():
            toggle.tick()

        for transition in self.__transitions:
            transition.tick()