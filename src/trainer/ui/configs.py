
import dearpygui.dearpygui as dpg
from typing import Final, ClassVar
from trainer.ui.themes import AppThemes

class AppConfigs():
    
    __padding: ClassVar[float] = 22.5    
    
    def __init__(self, app_width: int, app_height: int, themes: AppThemes) -> None:
        
        self.__themes: Final[AppThemes] = themes
        
        self.__app_width: Final[int] = app_width
        
        self.__app_height: Final[int] = app_height
        
        self.__width = self.__app_width - 50
        
        self.__height = self.__app_height - 190
        
    def create(self) -> None:
        
        
        with dpg.child_window(tag="view-configs", width=self.__width,height=self.__height,indent=self.__padding) as container:
            
            self.__themes.apply_theme(container, self.__themes.main_container)
            
            dpg.add_text("Configs Tab")
            
