from loguru import logger
from trainer.ui.components.base import BaseComponent
from trainer.ui.styles import themes, icons
import dearpygui.dearpygui as dpg

class ImageBtn(BaseComponent):
    
    def __init__(self, name: str, width: float, height: float, icon_size: float = 24, icon_key: str = "exit", indent: float = 0):
        super().__init__()
        self.__name = name
        self.__width = width
        self.__height = height
        self.__icon_key = icon_key
        self.__icon_size = icon_size
        self.__indent = indent

    def build(self):
        
        h_indent = (self.__width - self.__icon_size) / 2
        v_padding = (self.__height - self.__icon_size) / 2

        with dpg.child_window(
            tag=self.__name, 
            width=self.__width, 
            height=self.__height,
            border=False,
            no_scrollbar=True,
        ) as container:
            
            themes.apply(container, themes.img_btn)
            
            dpg.add_spacer(height=v_padding)
            
            with dpg.group(horizontal=True, indent=h_indent):
                dpg.add_image(
                    icons.apply(self.__icon_key), 
                    width=self.__icon_size, 
                    height=self.__icon_size,
                    indent=self.__indent
                )
        
        return super().build()