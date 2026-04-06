import dearpygui.dearpygui as dpg
from trainer.ui.handlers.mouse import MouseHandler
from trainer.ui.handlers.base import BaseHandler
from trainer.ui.styles.font import Fonts
from trainer.ui.styles.themes import Themes
from trainer.ui.styles.base import BaseStyle
from loguru import logger

class App():
    
    __WINDOW_WIDTH = 450
    __WINDOW_HEIGHT = 600
    __WINDOW_NAME = "ARK QOL"
    
    def __init__(self) -> None:
        self.__HANDLERS: list[type[BaseHandler]] = [MouseHandler]
        self.__active_handlers = []
        self.__STYLES: list[BaseStyle] = []
        
    def __register_handlers(self) -> None:
        
        for instance in self.__HANDLERS:
            
            handler = instance()
            
            handler.register() 
            
            self.__active_handlers.append(handler)
        
        logger.success(f"Registered handlers: {self.__active_handlers}")
            
    def __register_styles(self) -> None:
        self.fonts = Fonts()
        self.themes = Themes(self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT, self.__WINDOW_NAME)
        logger.success(f"Registered styles: {self.fonts, self.themes}")
        
    def __on_tick(self) -> None:
        pass
    
    
    def start(self) -> None:
        
        dpg.create_context()
        dpg.create_viewport(title=self.__WINDOW_NAME, width=self.__WINDOW_WIDTH, height=self.__WINDOW_HEIGHT, decorated=False)

        with dpg.window(label="main", tag="main_window")  as main_window:
            dpg.add_text("\n      ARK QOL")
        
        dpg.set_primary_window("main_window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        
        
        self.__register_handlers()
        self.__register_styles()
        
        self.themes.apply(main_window, self.themes.primary)
        
        logger.success(f"Main UI Loop started")
        
        while dpg.is_dearpygui_running():
            self.__on_tick()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()