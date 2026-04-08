from typing import Callable, List, Tuple, Any
import dearpygui.dearpygui as dpg
from trainer.ui.components.base import BaseComponent
from trainer.ui.styles import fonts, themes, icons
from trainer.ui.animations.animations import UnderlineTransition
from trainer.ui.common.math import Math


class NavbarComponent(BaseComponent):
    """
    Navigation bar component for switching between different application containers.
    """

    __slots__ = ("__underlines", "__on_page_change")

    def __init__(self, on_page_change: Callable[[str], None]) -> None:
        """
        Initializes the navbar with page change logic.
        """
        self.__underlines: List[UnderlineTransition] = []
        self.__on_page_change: Callable[[str], None] = on_page_change
        super().__init__()

    def show_visuals(self, *args: Any, **kwargs: Any) -> None:
        """
        Navigates to the visuals container.
        """
        self.__on_page_change("visual-container")

    def show_logs(self, *args: Any, **kwargs: Any) -> None:
        """
        Navigates to the logs container.
        """
        self.__on_page_change("logs-container")

    def show_stats(self, *args: Any, **kwargs: Any) -> None:
        """
        Navigates to the stats container.
        """
        self.__on_page_change("stats-container")

    def show_settings(self, *args: Any, **kwargs: Any) -> None:
        """
        Navigates to the settings container.
        """
        self.__on_page_change("settings-container")

    def build(self) -> None:
        """
        Constructs the Navbar UI and initializes underline transitions.

        nav_items breakdown:
        1. Icon Name (str): Key used to fetch the image from the icons registry.
        2. Label (str): Display text shown under the icon.
        3. Image Indent (float): Base horizontal offset for the icon.
        4. Text Indent (float): Base horizontal offset for the text label.
        5. Callback (Callable): Method triggered when the navigation group is clicked.
        """
        nav_items: List[Tuple[str, str, float, float, Callable]] = [
            ("eye", "Visuals", 60.0, 42.5, self.show_visuals),
            ("logs", "Logs", 65.0, 60.0, self.show_logs),
            ("stats", "Stats", 52.5, 42.5, self.show_stats),
            ("settings", "Settings", 60.0, 32.5, self.show_settings),
        ]

        with dpg.child_window(
            tag="app-navbar",
            width=425,
            height=75,
            border=False,
            indent=12.5,
        ) as navbar:
            themes.apply(navbar, themes.container)

            with dpg.group(horizontal=True, indent=15):
                for label_lower, label, img_indent, text_indent, target_callback in nav_items:
                    group_tag: str = f"nav-group-{label_lower}"

                    with dpg.group(tag=group_tag):
                        dpg.add_spacer(height=10.5)

                        img_ind_val: float = Math.centre_text_indent(
                            img_indent, label, fonts.font_bold_18
                        )
                        dpg.add_image(
                            icons.apply(label_lower),
                            width=24,
                            height=24,
                            indent=img_ind_val
                        )

                        text_ind_val: float = Math.centre_text_indent(
                            text_indent, label, fonts.font_bold_18
                        )
                        text_item: int = dpg.add_text(label, indent=text_ind_val)
                        fonts.apply(text_item, fonts.font_bold_18)

                    with dpg.item_handler_registry() as registry:
                        dpg.add_item_clicked_handler(callback=target_callback)

                    dpg.bind_item_handler_registry(group_tag, registry)

                    self.__underlines.append(
                        UnderlineTransition(
                            target=group_tag,
                            width=90,
                            color=(1, 180, 240, 255),
                            duration=0.2,
                        )
                    )

        super().build()

    def tick(self) -> None:
        """
        Updates underline animations for each frame.
        """
        for underline in self.__underlines:
            underline.tick()