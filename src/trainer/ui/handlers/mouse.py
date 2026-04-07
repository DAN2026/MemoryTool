import dearpygui.dearpygui as dpg
from trainer.ui.handlers.base import BaseHandler

class MouseHandler(BaseHandler):

    def __init__(self):
        super().__init__()

    def register(self) -> None:
        with dpg.handler_registry(tag="viewport_move_handler"):
            dpg.add_mouse_drag_handler(
                button=dpg.mvMouseButton_Left, 
                callback=MouseHandler._static_drag_viewport
            )
            
    @staticmethod
    def _static_drag_viewport(sender, app_data):
        
        window = dpg.get_active_window()
        
        if window == 112:
            return
        
        if app_data and len(app_data) >= 3:
            dx, dy = app_data[1], app_data[2]
            if dx != 0 or dy != 0:
                pos = dpg.get_viewport_pos()
                dpg.set_viewport_pos([pos[0] + dx, pos[1] + dy])