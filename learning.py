import dearpygui.dearpygui as dpg

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 550

def drag_viewport(sender, app_data):
    
    if dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
        pos = dpg.get_viewport_pos()
        dpg.set_viewport_pos([pos[0] + app_data[1], pos[1] + app_data[2]])

def example_hello_world() -> None:
    dpg.create_context()
    
    dpg.create_viewport(
        title="Custom Window", 
        width=WINDOW_WIDTH, 
        height=WINDOW_HEIGHT, 
        decorated=False, 
        resizable=False
    )

    with dpg.handler_registry():
        dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left, callback=drag_viewport)

    dpg.setup_dearpygui()

    with dpg.theme() as test_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 120, 255, 255))

    with dpg.window(label="Main", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, no_title_bar=True):
        
        with dpg.child_window(width=-1, height=100):
            
            with dpg.group(horizontal=True, width=100, height=50, indent=0):
                testBtn = dpg.add_button(label="Click Me", width=-1)
                dpg.add_button(label="Click Me", width=-1)
                dpg.add_button(label="Click Me", width=-1)
                dpg.add_button(label="Click Me", width=-1)
                
                dpg.bind_item_theme(testBtn, test_theme)
            
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    example_hello_world()