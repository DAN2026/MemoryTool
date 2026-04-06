import dearpygui.dearpygui as dpg
from typing import Final, ClassVar, Callable
from trainer.ui.themes import AppThemes
from trainer.ui.animation import ColorTransition, UnderlineTransition

def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
        int(lerp(c1[3], c2[3], t)),
    )

class AppNavbar():
    
    
    __padding: ClassVar[float] = 22.5   
    
    __PADDING_BTM: ClassVar[float] = 7.5   
    
    __PADDING_TOP: ClassVar[float] = 15
      
    __NAVBAR_BTN_TAGS: ClassVar[list[str]] = ["nav-btn-1", "nav-btn-2", "nav-btn-3", "nav-btn-4"]
    
    __ICONS: ClassVar[list[str]] = ["eye", "log", "bug", "config"]
    
    __LINKS: ClassVar[list[str]] = ["Visuals", "Logs", "Debug", "Configs"]
    
    __EVENT_HANDLER_LIST: ClassVar[list[str]] = ["nav-btn-1-handler", "nav-btn-2-handler", "nav-btn-3-handler", "nav-btn-4-handler"]
    
    __ICON_TAGS: ClassVar[list[str]] = ["nav-icon-1", "nav-icon-2", "nav-icon-3", "nav-icon-4"]
    
    
    __PADDING_LIST_TEXT: ClassVar[list[float]] = [5, 10, 7.5, 5]
    
    __PADDING_LIST_ICON: ClassVar[list[float]] = [15, 12.5, 15, 15]
    
    def __init__(self, app_width: int, app_height: int, themes: AppThemes, on_navigate = None) -> None:
        
        self.__themes: Final[AppThemes] = themes
        
        self.__app_width: Final[int] = app_width
        
        self.__app_height: Final[int] = app_height
        
        self.__navbar_width: Final[int] = self.__app_width - 50
        
        self.__navbar_height: Final[int] = 75
        
        self.__SUBSCRIBED_FUNCTIONS: Final[Callable[[], None]] = [self.__visuals_btn, self.__logs_btn, self.__debug_btn, self.__configs_btn]
        
        self.__transitions: list[ColorTransition] = []
        
        self.__underlines: list[UnderlineTransition] = []
        
        self.__on_navigate = on_navigate

        
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

            with dpg.group(horizontal=True, indent=10):
                
                
                dpg.add_spacer(width=10)
                
                for i in range(len(self.__LINKS)):
                    
                    with dpg.group(tag=self.__NAVBAR_BTN_TAGS[i]):
                        
                        dpg.add_spacer(height=8.5)
                        
                        dpg.add_image(self.__themes.icon(self.__ICONS[i]), tag=self.__ICON_TAGS[i], indent=self.__PADDING_LIST_ICON[i])

                        dpg.add_spacer(height=1.0)
                        
                        icon_txt = dpg.add_text(self.__LINKS[i], indent=self.__PADDING_LIST_TEXT[i])
                        
                        self.__themes.apply_theme(icon_txt, self.__themes.navbar_txt)
                        self.__themes.apply_font(icon_txt, self.__themes.font_navbar)
                        
                        dpg.add_spacer(width=85)
                        
                dpg.add_spacer(width=10)

            self.__add_navbar_events()
            
            self.__add_transitions()
                    
        dpg.add_spacer(height=self.__PADDING_BTM)
        
    
    def __add_transitions(self) -> None:
        for i, tag in enumerate(self.__NAVBAR_BTN_TAGS):

            self.__transitions.append(
                ColorTransition(
                    target     = tag,
                    color_slot = dpg.mvThemeCol_ChildBg,
                    initial    = self.__themes.BTN_NAVBAR,
                    final      = self.__themes.BTN_NAVBAR_HOVER,
                    duration   = 0.2
                )
            )
            self.__underlines.append(
                UnderlineTransition(
                    target   = tag,
                    width    = 60,
                    color    = (0, 180, 255, 255),
                    duration = 0.2
                )
            )
            
    def tick(self) -> None:
        
        for transition in self.__transitions:
            transition.tick()
            
        for underline in self.__underlines:  
            underline.tick()

        for i, tag in enumerate(self.__NAVBAR_BTN_TAGS):
            t = 1.0 if dpg.is_item_hovered(tag) else 0.0  
            tint = lerp_color(self.__themes.BTN_NAVBAR, self.__themes.BTN_NAVBAR_HOVER, t)
            dpg.configure_item(self.__ICON_TAGS[i], tint_color=tint)   
    
    
    
    def __add_navbar_events(self):
        
        for i in range(len(self.__EVENT_HANDLER_LIST)):
            with dpg.item_handler_registry(tag=self.__EVENT_HANDLER_LIST[i]):
                dpg.add_item_clicked_handler(callback=self.__SUBSCRIBED_FUNCTIONS[i])
                dpg.add_item_hover_handler(callback=self.__on_hover, user_data=i)
                
            dpg.bind_item_handler_registry(
                self.__NAVBAR_BTN_TAGS[i], 
                self.__EVENT_HANDLER_LIST[i]
            )
            
            
    def __on_hover(self, sender, app_data, user_data) -> None:
        index = user_data
                
    def __visuals_btn(self) -> None:
        if self.__on_navigate: self.__on_navigate(0)

    def __logs_btn(self) -> None:
        if self.__on_navigate: self.__on_navigate(1)

    def __debug_btn(self) -> None:
        if self.__on_navigate: self.__on_navigate(2)

    def __configs_btn(self) -> None:
        if self.__on_navigate: self.__on_navigate(3)
        
        