from loguru import logger
from trainer.ui.components.base import BaseComponent
import dearpygui.dearpygui as dpg
from trainer.ui.styles import fonts, themes
from trainer.ui.components.image_btn import ImageBtn
from trainer.ui.animations.animations import ColorTransition
from trainer.ui.common.math import Math

class LogsComponent(BaseComponent):
    
    
    def __init__(self):
        
        self.__transitions: list[ColorTransition] = []
        
        super().__init__()
    
    def build(self):

        dpg.add_spacer(height=2.5)
        
        with dpg.child_window(tag="logs-container", width=425, height=350, border=False, indent=12.5, show=False) as logs:
            
            dpg.add_text("Test 2")
            
        # dpg.configure_item(visuals, show = False)

        themes.apply(logs, themes.container)
        
        super().build()
        
    
        
        
    
