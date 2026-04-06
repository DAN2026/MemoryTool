from typing import ClassVar
import ctypes
import win32gui
import win32con
import dearpygui.dearpygui as dpg
from trainer.ui.styles.base import BaseStyle

class Themes(BaseStyle):

    __BG_PRIMARY: ClassVar[tuple] = (14, 14, 14, 255)
    __BG_HEADER: ClassVar[tuple] = (20, 20, 20, 255)

        
    __WINDOW_RADIUS: ClassVar[int] = 2
    __WINDOW_OPACITY: ClassVar[int] = 235
    __CHROMA_KEY: ClassVar[int] = 0x0000FF00

    def __init__(self, window_width: float, window_height: float, window_name: str):
        
        self.__setup_window(window_width, window_height, window_name)
        
        super().__init__()

    @property
    def primary(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.__BG_PRIMARY)
        return theme


    def apply(self, component: int | str, theme: int) -> None:
        
        dpg.bind_item_theme(component, theme)
        
    def __setup_window(self, width: int, height: int, name: str) -> None:
        
        hwnd = win32gui.FindWindow(None, name)

        hrgn = ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, width, height, self.__WINDOW_RADIUS * 2, self.__WINDOW_RADIUS * 2)
        
        ctypes.windll.user32.SetWindowRgn(hwnd, hrgn, True)

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
        
        win32gui.SetLayeredWindowAttributes(
            hwnd,
            self.__CHROMA_KEY,
            self.__WINDOW_OPACITY,
            win32con.LWA_COLORKEY | win32con.LWA_ALPHA,
        )

