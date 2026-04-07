from loguru import logger
from trainer.ui.components.base import BaseComponent
import dearpygui.dearpygui as dpg
from trainer.ui.styles import fonts, themes
from trainer.ui.components.image_btn import ImageBtn
from trainer.ui.animations.animations import ColorTransition
from trainer.ui.common.math import Math
from trainer.ui.components.toggle import Toggle
from trainer.memory.game import ShooterGame

class VisualsComponent(BaseComponent):
    
    
    def __init__(self, ark: ShooterGame ):
        
        self.__transitions: list[ColorTransition] = []
        
        self.__ARK = ark
        
        self.set_normal_ini()
        
        super().__init__()
        
    def __on_toggle_clicked(self, clicked_key: str):
        
        ini_map = {
            "normal_ini": self.set_normal_ini,
            "hard_ini": self.set_hard_ini,
            "potato_ini": self.set_potato_ini,
            "no_water": self.set_no_water 
        }
        
        if clicked_key in ini_map:
            self.__handle_ini_logic(clicked_key, ini_map)
        else:
            self.__handle_non_ini(clicked_key)

    def __handle_ini_logic(self, clicked_key: str, ini_map: dict):
        
        is_active = self.toggles[clicked_key].get_value()

        if is_active:
            for key in ini_map:
                if key != clicked_key:
                    self.toggles[key].set_value(False)
            ini_map[clicked_key]()
        else:
            self.toggles["normal_ini"].set_value(True)
            self.set_normal_ini()

    def __handle_non_ini(self, key: str):
        
        state = self.toggles[key].get_value()
        
        utility_map = {
            "fullbright": lambda s: logger.info(f"Fullbright: {s}"),
            "beer_xz":    lambda s: logger.info(f"Beer / XZ: {s}"),
            "no_trees":   lambda s: logger.info(f"No Trees: {s}"),
        }

        if key in utility_map:
            utility_map[key](state)
                    
    def build(self):

        options = ["Normal INI", "Hard INI", "Potato INI", "No Water", "Fullbright", "Beer / XZ", "No Trees", "Fov"]

        toggles_data = [
            ("normal_ini", "Normal INI"),
            ("hard_ini", "Hard INI"),
            ("potato_ini", "Potato INI"),
            ("no_water", "No Water"),
            ("fullbright", "Fullbright"),
            ("beer_xz", "Beer / XZ"),
            ("no_trees", "No Trees"),
        ]
        
        self.toggles = {}

        with dpg.child_window(tag="visual-container", width=425, height=350, border=False, indent=12.5, show=False) as visuals:
            
            dpg.add_spacer(height=10)
            
            with dpg.group(tag="visual-group-container", horizontal=True, horizontal_spacing=25, indent=35):
                
                with dpg.group(tag="visual-group-1"):
                
                    for option in options:
                        
                        text_item = dpg.add_text(option)
                        
                        fonts.apply(text_item, fonts.font_bold_18)
                    
                        dpg.add_spacer(height=10)
                    
                    
                with dpg.group(tag="visual-group-2"):
                
                    for key, label in toggles_data:
                        
                        self.toggles[key] = Toggle(
                            parent="visual-group-2",
                            label=label,
                            default=False,
                            width=44,
                            height=24,
                            callback=lambda _, k=key: self.__on_toggle_clicked(k)
                        )
                        
                        self.toggles[key].build()
                        
                        self.toggles["normal_ini"].set_value(True)
                        
                        dpg.add_spacer(height=10)
                        
                    dpg.add_spacer(height=1)    
                    
                    dpg.add_slider_float(
                        label="##fov_slider", 
                        default_value=self.__ARK.fov.get(), 
                        min_value=0.0, 
                        max_value=2.0,
                        callback=lambda s, a: self.set_fov(s, a)
                    )
                    
        themes.apply(visuals, themes.container)
        
        super().build()
        
    def tick(self) -> None:
        
        for toggle in self.toggles.values():
            toggle.tick()
            
            
    def set_normal_ini(self):
        
        self.__ARK.ini.set(3)
        

    def set_hard_ini(self):
        
        self.__ARK.ini.set(1)
        

    def set_potato_ini(self):
        logger.info("Applying Potato INI settings...")    
        
    def set_fullbright(self):
        
        self.__ARK.ini.set(1)
        

    def set_no_water(self):
        
        self.__ARK.ini.set(6)
        
    def set_fov(self, sender, app_data):
        
        self.__ARK.fov.set(app_data)
