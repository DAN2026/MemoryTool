import dearpygui.dearpygui as dpg
from typing import Final, ClassVar
from trainer.ui.themes import AppThemes
from trainer.ui.components import Toggle


class AppVisuals:

    __padding: ClassVar[float] = 22.5

    def __init__(self, app_width: int, app_height: int, themes: AppThemes) -> None:

        self.__themes: Final[AppThemes] = themes

        self.__app_width: Final[int] = app_width

        self.__app_height: Final[int] = app_height

        self.__visuals_width = self.__app_width - 50

        self.__visuals_height = self.__app_height - 190

    def create(self) -> None:

        with dpg.child_window(
            tag="view-visuals",
            width=self.__visuals_width,
            height=self.__visuals_height,
            indent=self.__padding,
        ) as container:

            self.__themes.apply_theme(container, self.__themes.main_container)

            dpg.add_text("Visuals Tab")

            self.__toggle = Toggle(  
                parent=container,
                label="Enable Feature",
                default=False,
                callback=lambda state: print(f"Toggle is now: {state}"),
                width=44,
                height=24,
            )

    def tick(self) -> None:
        self.__toggle.tick()