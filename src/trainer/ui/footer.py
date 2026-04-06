
import dearpygui.dearpygui as dpg
from typing import Final, ClassVar
from trainer.ui.themes import AppThemes
from trainer.ui.animation import ScaleTransition

class AppFooter():
    
    __padding: ClassVar[float] = 22.5  
    
    __padding_btm: ClassVar[float] = 7.5  
    
    def __init__(self, app_width: int, app_height: int, themes: AppThemes) -> None:
        
        self.__themes: Final[AppThemes] = themes
        
        self.__app_width: Final[int] = app_width
        
        self.__app_height: Final[int] = app_height
        
        self.__visuals_width = self.__app_width - 50
        
        self.__visuals_height = self.__app_height - 500
        
        self.__scales: list[ScaleTransition] = []

        
    def create(self) -> None:
        dpg.add_spacer(height=self.__padding_btm)
        
        with dpg.group(horizontal=True):
            
            with dpg.child_window(width=self.__visuals_width - 135, height=self.__visuals_height, indent=self.__padding, no_scrollbar=True, no_scroll_with_mouse=True) as container:
                
                self.__themes.apply_theme(container, self.__themes.footer)
                
                with dpg.group(tag="footer", horizontal=True):
                    
                    logo_btn = dpg.add_image_button(self.__themes.icon("Arkopedia"), width=50, height=50, tag="footer-logo-btn",)
                    
                    self.__themes.apply_theme(logo_btn, self.__themes.logo_btn)
                    
            with dpg.child_window(width=50, height=self.__visuals_height, no_scrollbar=True, no_scroll_with_mouse=True) as container_dc:
                
                self.__themes.apply_theme(container_dc, self.__themes.exit_bg)
                
                dpg.add_spacer(height=5)
                
                with dpg.group(tag="footer-exit", horizontal=True):
                    
                    exit_btn = dpg.add_image_button(self.__themes.icon("exit"), width=30, height=30, indent=10, tag="footer-exit-btn", callback=lambda: dpg.stop_dearpygui())
                    
                    self.__themes.apply_theme(exit_btn, self.__themes.exit_btn)
                    
            with dpg.drawlist(width=10, height=50):

                dpg.draw_line((5, 0), (5, 50), color=(255, 255, 255, 100), thickness=1)

            with dpg.child_window(width=50, height=self.__visuals_height, no_scroll_with_mouse=True, no_scrollbar=True) as container_dc:
                
                self.__themes.apply_theme(container_dc, self.__themes.dc_footer_wrapper)
                
                with dpg.group(tag="footer-discord"):
                    
                    discord_btn = dpg.add_image_button(self.__themes.icon("discord"), width=50, height=50, tag="footer-discord-btn")
                    
                    self.__themes.apply_theme(discord_btn, self.__themes.dc_icon)
                    
        self.__add_transitions()
    
    def __add_transitions(self) -> None:
        self.__scales = [
            ScaleTransition(target="footer-logo-btn",    base_w=50, base_h=50, scale=1.055),
            ScaleTransition(target="footer-exit-btn",    base_w=30, base_h=30, scale=1.055),
            ScaleTransition(target="footer-discord-btn", base_w=50, base_h=50, scale=1.055),
        ]

    def tick(self) -> None:
        for scale in self.__scales:
            scale.tick()   

