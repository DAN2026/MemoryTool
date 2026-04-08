from typing import ClassVar, Dict, List, Any
import dearpygui.dearpygui as dpg
from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes, fonts


class StatsPage(BasePage):
    """
    `StatsPage` is responsible for displaying engine internals and diagnostic metrics.
    """

    __slots__ = ("__transitions", "__registry")

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0

    def __init__(self) -> None:
        """
        Initializes the stats page state and diagnostic registries.
        """
        self.__transitions: List[Any] = []
        self.__registry: Dict[str, Any] = {}
        super().__init__()

    def build(self) -> None:
        """
        Constructs the statistical information and metrics layout.
        """
        with dpg.child_window(
            tag="stats-container",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12,
            show=False,
        ) as stats_window:

            dpg.add_spacer(height=10)

            header = dpg.add_text("System Statistics")
            fonts.apply(header, fonts.font_bold_18)

            dpg.add_spacer(height=5)

            dpg.add_text(
                "Engine metrics and memory offsets coming soon...",
                color=(200, 200, 200),
            )

        themes.apply(stats_window, themes.container)
        super().build()

    def tick(self) -> None:
        """
        Processes frame updates for statistical metrics.
        """
        pass