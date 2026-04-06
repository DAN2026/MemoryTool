import dearpygui.dearpygui as dpg
from trainer.ui.navbar import AppNavbar
from trainer.ui.header import AppHeader
from trainer.ui.themes import AppThemes
from trainer.ui.visuals import AppVisuals
from trainer.ui.configs import AppConfigs
from trainer.ui.debug import AppDebug
from trainer.ui.logs import AppLogs
from trainer.ui.footer import AppFooter
import ctypes
import win32gui
import win32con
import win32api
from typing import ClassVar
from pathlib import Path

class App():
    
    
    __WIDTH: ClassVar[int] = 450
    
    __HEIGHT: ClassVar[int] = 550
    
    __VIEW_TAGS: ClassVar[list[str]] = ["view-visuals", "view-logs", "view-debug", "view-configs"]

    
    def __init__(self):
        
        self.__themes = AppThemes()
        self.__navbar = AppNavbar(app_height=self.__HEIGHT, app_width=self.__WIDTH, themes=self.__themes, on_navigate=self.__switch_view)
        self.__footer = AppFooter(app_height=self.__HEIGHT, app_width=self.__WIDTH, themes=self.__themes)
        
        
        self.__visuals = AppVisuals(app_height=self.__HEIGHT, app_width=self.__WIDTH, themes=self.__themes)
        self.__logs = AppLogs(app_height=self.__HEIGHT, app_width=self.__WIDTH, themes=self.__themes)
        self.__debug = AppDebug(app_height=self.__HEIGHT, app_width=self.__WIDTH, themes=self.__themes)
        self.__configs = AppConfigs(app_height=self.__HEIGHT, app_width=self.__WIDTH, themes=self.__themes)
        
        self.__window = None
    
    def __drag(self, sender, app_data) -> None:
        if dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
            if dpg.is_item_hovered(self.__window):
                pos = dpg.get_viewport_pos()
                dpg.set_viewport_pos([pos[0] + app_data[1], pos[1] + app_data[2]])
            
    def __register_drag(self) -> None:
        
        with dpg.handler_registry(): dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left, callback=self.__drag)
    
    
    def __build(self) -> None:
        
        with dpg.window(
            label="Main",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            no_title_bar=True,
            ) as main_window:  
            
            self.__window = main_window
            
            dpg.set_primary_window(main_window, True)
            
            self.__themes.apply_theme(component=main_window,theme=self.__themes.primary)
            
            self.__navbar.create()
            
            self.__visuals.create()
            self.__logs.create()  
            self.__debug.create()
            self.__configs.create()
            
            self.__footer.create()    
            
        self.__switch_view(0)    

    def __switch_view(self, index: int) -> None:
        for i, tag in enumerate(self.__VIEW_TAGS):
            if i == index:
                dpg.show_item(tag)
            else:
                dpg.hide_item(tag)

    def __show_viewport(self) -> None:
        dpg.show_viewport()
        self.__themes.setup_window(self.__WIDTH, self.__HEIGHT)

        
    def __initialize(self) -> None:
        
        dpg.create_context()

        self.__themes.register_fonts()
        self.__themes.register_icons()
        
        dpg.create_viewport(
            title="Custom Window", 
            width=600, 
            height=550, 
            decorated=False, 
            resizable=False,
            clear_color=(0, 0, 0, 0)
        )

        self.__register_drag()
        
        self.__build()
        
        dpg.setup_dearpygui()
        self.__show_viewport()
        
        while dpg.is_dearpygui_running():
            self.__navbar.tick()
            self.__footer.tick()
            self.__visuals.tick()
            dpg.render_dearpygui_frame()
            
        dpg.destroy_context()
    
    def main(self) -> None:
        
        self.__initialize()

    