import threading
import webbrowser
from typing import ClassVar, Callable, Optional, List, Union
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.memory.game import ShooterGame
from trainer.ui.components.base import BaseComponent
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.vertical_seperator import VerticalSeparatorComponent
from trainer.ui.components.reconnect import ReconnectButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.styles import themes, fonts
from trainer.ui.animations.color import ColorTransition


class FooterComponent(BaseComponent):
    """
    Component responsible for rendering and handling interactions for the footer UI.

    Manages status labels, navigation icons, and dynamic background color transitions
    for interactive elements including a white-to-grey Discord icon background.
    """

    __HEIGHT: ClassVar[float] = 55.0
    __ICON_SIZE: ClassVar[float] = 55.0
    __Y_POS: ClassVar[float] = 535.5
    __X_POS: ClassVar[float] = 12.5
    __RECONNECT_DELAY: ClassVar[float] = 0.55
    __ERROR_DURATION: ClassVar[float] = 3.0
    __DISCORD_URL: ClassVar[str] = "https://discord.gg/XXQNVqzm2G"

    __slots__ = (
        "__ark",
        "__icons",
        "__reconnect_btn",
        "__logout_btn",
        "__status_label",
        "__error_label",
        "__seperator",
        "__status",
        "__transitions",
    )

    def __init__(self, ark: ShooterGame) -> None:
        """
        Initializes the footer component with game state and animation tracking.

        Args:
            ark: The ShooterGame memory instance.
        """
        super().__init__()
        self.__ark: ShooterGame = ark
        self.__icons: List[IconButtonComponent] = []
        self.__reconnect_btn: Optional[ReconnectButtonComponent] = None
        self.__logout_btn: Optional[IconButtonComponent] = None
        self.__status_label: Optional[TextComponent] = None
        self.__error_label: Optional[TextComponent] = None
        self.__seperator: Optional[VerticalSeparatorComponent] = None
        self.__status: str = "Connected"
        self.__transitions: List[ColorTransition] = []

    def build(self) -> None:
        """
        Constructs the footer layout and initializes interactive animations.
        """
        self.__add_icon(
            tag="footer-arkopedia-icon",
            icon_name="arkopedia",
            theme=themes.container,
            pos=[self.__X_POS, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            on_click=self.__on_arkopedia_click,
        )

        self.__error_label = TextComponent(
            tag="footer_error_text",
            text="Ark Survival Evolved is not open",
            pos=[self.__X_POS + 75, self.__Y_POS + 10],
            width=200,
            height=20,
            y_indent=0,
            show=False,
            font=fonts.font_18,
            theme=themes.footer_error,
        )
        self.__error_label.build()

        self.__status_label = TextComponent(
            tag="footer_status_text",
            text=f"Status: {self.__status}",
            pos=[self.__X_POS + 75, self.__Y_POS + 30],
            width=200,
            height=20,
            y_indent=0,
            font=fonts.font_bold_18,
            theme=themes.footer_text,
        )
        self.__status_label.build()

        self.__logout_btn = IconButtonComponent(
            tag="footer-logout-icon",
            icon_name="logout",
            theme=themes.container,
            pos=[self.__X_POS + 285, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            icon_size=26.0,
            show=True,
            on_click=self.__on_logout_click,
            x_indent=16,
            y_indent=13.5,
        )
        self.__logout_btn.build()

        self.__reconnect_btn = ReconnectButtonComponent(
            tag="footer_reconnect_btn",
            pos=[self.__X_POS + 285, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            theme=themes.container,
            show=False,
            on_click=self.__execute_reconnect_logic,
        )
        self.__reconnect_btn.build()

        self.__seperator = VerticalSeparatorComponent(
            tag="footer_seperator",
            pos=[self.__X_POS + 355, self.__Y_POS],
            height=self.__HEIGHT,
            thickness=2.0,
            color=[255, 255, 255, 150],
        )
        self.__seperator.build()

        self.__add_icon(
            tag="footer-discord-icon",
            icon_name="discord",
            theme=themes.discord_icon,
            pos=[382.5, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            on_click=self.__on_discord_click,
        )

        self.__transitions.append(
            ColorTransition(
                "footer-arkopedia-icon", (20, 20, 20, 255), (0, 28, 28, 255)
            )
        )
        self.__transitions.append(
            ColorTransition(
                "footer-logout-icon", (20, 20, 20, 255), (28, 28, 28, 255)
            )
        )
        self.__transitions.append(
            ColorTransition(
                "footer_reconnect_btn", (20, 20, 20, 255), (28, 28, 28, 255)
            )
        )
        self.__transitions.append(
            ColorTransition(
                "footer-discord-icon", (255, 255, 255, 255), (180, 180, 180, 255)
            )
        )

        self.set_status(self.__ark.is_connected)
        super().build()

    def set_status(self, connected: bool) -> None:
        """
        Updates UI visibility and labels based on the game connection state.

        Args:
            connected: The current connection status.
        """
        self.__status = "Connected" if connected else "Disconnected"

        if self.__status_label:
            self.__status_label.set_text(f"Status: {self.__status}")

        if self.__logout_btn:
            self.__logout_btn.toggle(show=connected)

        if self.__reconnect_btn:
            self.__reconnect_btn.toggle(show=not connected)

    def tick(self) -> None:
        """
        Processes animations and polls for game connection changes.

        Utilizes check_connection() to verify if memory addresses are still
        reachable by the process handle.
        """
        for transition in self.__transitions:
            transition.tick()

        for icon in self.__icons:
            icon.tick()

        if self.__logout_btn:
            self.__logout_btn.tick()

        if self.__reconnect_btn:
            self.__reconnect_btn.tick()

        if self.__status == "Connected":
            # Using the new check_connection logic to detect handle/memory invalidation
            if not self.__ark._conn.check_connection():
                logger.warning("ShooterGame.exe memory is no longer reachable. Disconnecting...")
                self.__ark.disconnect()
                self.set_status(False)

    def __execute_reconnect_logic(self, tag: str) -> None:
        """
        Handles the reconnection attempt and temporary error display.

        Args:
            tag: The tag of the sender component.
        """
        logger.debug(f"Attempting game reconnection via `{tag}`...")
        success: bool = self.__ark.reconnect()

        if not success and self.__error_label:
            self.__error_label.toggle(show=True)
            threading.Timer(
                self.__ERROR_DURATION,
                lambda: self.__error_label.toggle(show=False),
            ).start()

        threading.Timer(
            self.__RECONNECT_DELAY, lambda: self.set_status(success)
        ).start()

    def __on_logout_click(self, tag: str) -> None:
        """
        Stops the application runtime.

        Args:
            tag: The tag of the sender component.
        """
        logger.info(f"Logout triggered via `{tag}`. Closing application...")
        dpg.stop_dearpygui()

    def __on_discord_click(self, tag: str) -> None:
        """
        Redirects the user to the Discord URL.

        Args:
            tag: The tag of the sender component.
        """
        logger.info(f"Opening Discord link via `{tag}`...")
        webbrowser.open(self.__DISCORD_URL)

    def __add_icon(
        self,
        tag: str,
        icon_name: str,
        theme: Union[int, str],
        pos: List[float],
        width: float,
        height: float,
        on_click: Optional[Callable[[str], None]] = None,
    ) -> None:
        """
        Helper method to build and store icon button components.
        """
        icon_btn: IconButtonComponent = IconButtonComponent(
            tag=tag,
            icon_name=icon_name,
            theme=theme,
            pos=pos,
            width=width,
            height=height,
            on_click=on_click,
        )
        icon_btn.build()
        self.__icons.append(icon_btn)

    def __on_arkopedia_click(self, tag: str) -> None:
        """
        Branding redirect callback.

        Args:
            tag: The tag of the sender component.
        """
        webbrowser.open(self.__DISCORD_URL)