import dearpygui.dearpygui as dpg
from typing import Final, ClassVar, Callable
from trainer.ui.themes import AppThemes

class AppNavbar():
    
    
    __padding: ClassVar[float] = 22.5   
    
    __PADDING_BTM: ClassVar[float] = 7.5   
    
    __PADDING_TOP: ClassVar[float] = 15
      
    __NAVBAR_BTN_TAGS: ClassVar[list[str]] = ["nav-btn-1", "nav-btn-2", "nav-btn-3", "nav-btn-4"]
    
    __ICONS: ClassVar[list[str]] = ["eye", "log", "bug", "config"]
    
    __LINKS: ClassVar[list[str]] = ["Visuals", "Logs", "Debug", "Configs"]
    
    __EVENT_HANDLER_LIST: ClassVar[list[str]] = ["nav-btn-1-handler", "nav-btn-2-handler", "nav-btn-3-handler", "nav-btn-4-handler"]
    
    
    
    __PADDING_LIST: ClassVar[list[float]] = [12, 4, 9, 12.5]
    
    def __init__(self, app_width: int, app_height: int, themes: AppThemes) -> None:
        
        self.__themes: Final[AppThemes] = themes
        
        self.__app_width: Final[int] = app_width
        
        self.__app_height: Final[int] = app_height
        
        self.__navbar_width: Final[int] = self.__app_width - 50
        
        self.__navbar_height: Final[int] = 75
        
        self.__SUBSCRIBED_FUNCTIONS: Final[Callable[[], None]] = [self.__visuals_btn, self.__logs_btn, self.__debug_btn, self.__configs_btn]
        
    def create(self) -> None:
        
        dpg.add_spacer(height=self.__PADDING_TOP)
        
        with dpg.child_window(
        width=self.__navbar_width,
        height=self.__navbar_height,
        indent=self.__padding,
        horizontal_scrollbar=False,
        no_scrollbar=True
        ) as navbar_container:
            
            self.__themes.apply_theme(navbar_container, self.__themes.navbar)

            with dpg.group(horizontal=True):
                
                

                dpg.add_spacer(width=37.5)

                for i in range(len(self.__LINKS)):
                    
                    with dpg.group(tag=self.__NAVBAR_BTN_TAGS[i]):
                        
                        dpg.add_spacer(height=12.5)
                        dpg.add_image(self.__themes.icon(self.__ICONS[i]), indent=self.__PADDING_LIST[i])
                        dpg.add_spacer(height=1.0)
                        icon_txt = dpg.add_text(self.__LINKS[i])
                        
                        self.__themes.apply_theme(icon_txt, self.__themes.navbar_txt)
                        self.__themes.apply_font(icon_txt, self.__themes.font_navbar)
                    dpg.add_spacer(width=25)


            self.__add_navbar_events()
                    
        dpg.add_spacer(height=self.__PADDING_BTM)
    
    
    def __add_navbar_events(self):
        
        for i in range(len(self.__EVENT_HANDLER_LIST)):
            with dpg.item_handler_registry(tag=self.__EVENT_HANDLER_LIST[i]):
                dpg.add_item_clicked_handler(callback=self.__SUBSCRIBED_FUNCTIONS[i])
                
            dpg.bind_item_handler_registry(
                self.__NAVBAR_BTN_TAGS[i], 
                self.__EVENT_HANDLER_LIST[i]
            )
            
                
    def __visuals_btn(self) -> None:
        print("Visuals button clicked")

    def __logs_btn(self) -> None:
        print("Logs button clicked")

    def __debug_btn(self) -> None:
        print("Debug button clicked")

    def __configs_btn(self) -> None:
        print("Configs button clicked")