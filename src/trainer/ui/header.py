import dearpygui.dearpygui as dpg
from typing import Final, ClassVar
from trainer.ui.themes import AppThemes

class AppHeader():
    
    __padding: ClassVar[float] = 22.5    
    
    def __init__(self, app_width: int, app_height: int, themes: AppThemes) -> None:
        
        self.__themes: Final[AppThemes] = themes
        
        self.__app_width: Final[int] = app_width
        
        self.__app_height: Final[int] = app_height
        
    def create(self) -> None:
        
        with dpg.child_window(
            width=self.__app_width,
            height=25,
        ) as header_container:
            
            self.__themes.apply_theme(header_container, self.__themes.header)
            
            dpg.add_spacer(height=.25)
            
            exit_btn =dpg.add_image_button(self.__themes.icon("exit"), width=15, height=15, indent=self.__app_width - 22, callback=lambda: dpg.stop_dearpygui())
            
            self.__themes.apply_theme(exit_btn, self.__themes.exit_btn)

        self.__header_container = header_container

    @property
    def container(self) -> int:
        return self.__header_container