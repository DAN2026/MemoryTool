import dearpygui.dearpygui as dpg
from trainer.ui.handlers.mouse import MouseHandler
from trainer.ui.handlers.base import BaseHandler
from trainer.ui.styles.font import Fonts
from trainer.ui.styles.themes import Themes
from trainer.ui.components.header import HeaderComponent
from trainer.ui.components.navbar import NavbarComponent
from trainer.ui.components.visuals import VisualsComponent
from trainer.ui.components.debug import DebugComponent
from trainer.ui.components.logs import LogsComponent
from trainer.ui.components.settings import SettingsComponent
from trainer.ui.styles.base import BaseStyle
from trainer.ui.components.toggle import Toggle
from trainer.ui.styles import fonts, themes, icons
from loguru import logger
from trainer.memory.game import ShooterGame

class App():
    
    __WINDOW_WIDTH = 450
    __WINDOW_HEIGHT = 600
    __WINDOW_NAME = "Arkopedia"
    
    def __init__(self) -> None:
        
    
        logger.info("App initializing")
        
        self.__HANDLERS: list[type[BaseHandler]] = [MouseHandler]
        self.__active_handlers = []
        self.__STYLES: list[BaseStyle] = []
        self.__ARK = ShooterGame()
        
        
    def __register_handlers(self) -> None:
        
        for instance in self.__HANDLERS:
            
            handler = instance()
            
            handler.register() 
            
            self.__active_handlers.append(handler)
        
        logger.success(f"Registered handlers: {self.__active_handlers}")
    
    
    def __change_page(self, target_tag: str) -> None:
        pages = ["visual-container", "logs-container", "debug-container", "settings-container"]
        
        CONTENT_X = 12.5
        CONTENT_Y = 148.5 

        for page in pages:
            if dpg.does_item_exist(page):
                is_target = (page == target_tag)
                
                dpg.configure_item(page, show=is_target)
                
                if is_target:
                    dpg.set_item_pos(page, [CONTENT_X, CONTENT_Y])
                    themes.apply(page, themes.container)
        
            
    def __on_tick(self) -> None:
        self.navbar.tick()
        self.visual.tick()
    
    def start(self) -> None:
        
        
        dpg.create_context()
        dpg.create_viewport(title=self.__WINDOW_NAME, width=self.__WINDOW_WIDTH, height=self.__WINDOW_HEIGHT, decorated=False)
        dpg.setup_dearpygui()

        fonts.register() 
        
        icons.register()

        with dpg.window(tag="main_window"):
            
            
            self.header = HeaderComponent().build()
            
            self.navbar = NavbarComponent(on_page_change=self.__change_page)
            
            self.navbar.build()
            
            self.visual = VisualsComponent(ark=self.__ARK)
            
            self.visual.build()
            
            DebugComponent().build()
            
            LogsComponent().build()
            
            SettingsComponent().build()
            
            self.__change_page("visual-container")
            # dpg.add_image(icons.apply("eye"))
            
            # This requires the self.__toggle.tick() to be in __on__tick()
            
            # self.__toggle = Toggle(  
            #     parent="main_window",
            #     label="Enable Feature",
            #     default=False,
            #     width=44,
            #     height=24,
            # ).build()
            
        
        dpg.set_primary_window("main_window", True)
        
        dpg.show_viewport()
        
        themes.register() 
        
        themes.apply("main_window", themes.primary)

        self.__register_handlers()
        
        
        logger.success("App Started")
        
        while dpg.is_dearpygui_running():
            
            self.__on_tick()
            
            
            dpg.render_dearpygui_frame()
            
        dpg.destroy_context()