import dearpygui.dearpygui as dpg
from pathlib import Path
from typing import ClassVar
import ctypes
import win32gui
import win32con


class AppThemes:

    # Colour constants
    BG_PRIMARY: ClassVar[tuple] = (14, 14, 14, 255)
    BG_NAVBAR: ClassVar[tuple] = (20, 20, 20, 255)
    BG_HEADER: ClassVar[tuple] = (20, 20, 20, 255)

    BTN_DEFAULT: ClassVar[tuple] = (20, 20, 20, 255)
    BTN_EXIT: ClassVar[tuple] = (20, 20, 20, 255)
    BTN_EXIT_HOVER: ClassVar[tuple] = (14, 14, 14, 255)
    BTN_EXIT_ACTIVE: ClassVar[tuple] = (14, 14, 14, 255)
    BTN_EXIT_ROUNDING: ClassVar[int] = 6

    BTN_NAVBAR: ClassVar[tuple] = (0, 255, 255, 255)
    BTN_NAVBAR_HOVER: ClassVar[tuple] = (0, 100, 100, 255)
    BTN_NAVBAR_ACTIVE: ClassVar[tuple] = (22, 22, 22, 255)

    BTN_LOGO: ClassVar[tuple] = (0, 0, 0, 0)
    BTN_LOGO_HOVER: ClassVar[tuple] = (0, 0, 0, 0)
    BTN_LOGO_ACTIVE: ClassVar[tuple] = (0, 0, 0, 0)

    # Font constants
    FONTS_DIR: ClassVar[Path] = Path(__file__).parent / "fonts" / "Roboto" / "static"
    FONT_REGULAR: ClassVar[str] = "Roboto-Regular.ttf"
    FONT_BOLD: ClassVar[str] = "Roboto-Bold.ttf"
    FONT_MEDIUM: ClassVar[str] = "Roboto-Medium.ttf"

    FONT_SIZE_SM: ClassVar[int] = 12
    FONT_SIZE_MD: ClassVar[int] = 15
    FONT_SIZE_LG: ClassVar[int] = 20

    # Window constants
    WINDOW_TITLE: ClassVar[str] = "Custom Window"
    WINDOW_RADIUS: ClassVar[int] = 2
    WINDOW_OPACITY: ClassVar[int] = 250
    CHROMA_KEY: ClassVar[int] = 0x0000FF00

    # Icon constants
    ICONS_DIR: ClassVar[Path] = Path(__file__).parent / "icons"
    ICONS: ClassVar[list[str]] = [
        "Arkopedia",
        "bug",
        "exit",
        "eye",
        "folder",
        "house",
        "info",
        "log",
        "settings",
        "star",
        "config",
        "discord",
        "clock",
    ]

    def __init__(self):
        self.__font_sm = None
        self.__font_md = None
        self.__font_lg = None
        self.__font_navbar = None
        self.__textures: dict[str, int] = {}

    def register_fonts(self) -> None:
        with dpg.font_registry():
            self.__font_sm = dpg.add_font(
                str(self.FONTS_DIR / self.FONT_REGULAR), self.FONT_SIZE_SM
            )
            self.__font_md = dpg.add_font(
                str(self.FONTS_DIR / self.FONT_REGULAR), self.FONT_SIZE_MD
            )
            self.__font_lg = dpg.add_font(
                str(self.FONTS_DIR / self.FONT_REGULAR), self.FONT_SIZE_LG
            )
            self.__font_navbar = dpg.add_font(
                str(self.FONTS_DIR / self.FONT_BOLD), 17.5
            )
        dpg.bind_font(self.__font_md)

    def register_icons(self) -> None:
        with dpg.texture_registry():
            for name in self.ICONS:
                path = str(self.ICONS_DIR / f"{name}.png")
                width, height, _, data = dpg.load_image(path)
                self.__textures[name] = dpg.add_static_texture(width, height, data)

    def icon(self, name: str) -> int:
        return self.__textures[name]

    def setup_window(self, width: int, height: int) -> None:
        hwnd = win32gui.FindWindow(None, self.WINDOW_TITLE)

        hrgn = ctypes.windll.gdi32.CreateRoundRectRgn(
            0, 0, width, height, self.WINDOW_RADIUS * 2, self.WINDOW_RADIUS * 2
        )
        ctypes.windll.user32.SetWindowRgn(hwnd, hrgn, True)

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(
            hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED
        )
        win32gui.SetLayeredWindowAttributes(
            hwnd,
            self.CHROMA_KEY,
            self.WINDOW_OPACITY,
            win32con.LWA_COLORKEY | win32con.LWA_ALPHA,
        )

    @property
    def button(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.BTN_DEFAULT)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
        return theme

    @property
    def exit_btn(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvImageButton):

                dpg.add_theme_color(dpg.mvThemeCol_Button, self.BTN_EXIT)

                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.BTN_EXIT_HOVER)

                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.BTN_EXIT_ACTIVE)
                # Rounding
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, self.BTN_EXIT_ROUNDING
                )

                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)

        return theme

    @property
    def navbar_btn(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvButton):

                dpg.add_theme_color(dpg.mvThemeCol_Button, self.BTN_NAVBAR)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.BTN_NAVBAR_HOVER)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.BTN_NAVBAR_ACTIVE)

                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                # dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, self.BTN_EXIT_ROUNDING)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)

        return theme

    @property
    def logo_btn(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvImageButton):

                dpg.add_theme_color(dpg.mvThemeCol_Button, self.BTN_LOGO)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.BTN_LOGO_HOVER)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.BTN_LOGO_ACTIVE)

                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)

        return theme

    @property
    def exit_btn(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvImageButton):

                dpg.add_theme_color(dpg.mvThemeCol_Button, self.BTN_LOGO)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.BTN_LOGO_HOVER)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.BTN_LOGO_ACTIVE)

                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)

        return theme

    @property
    def dc_icon(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvImageButton):

                dpg.add_theme_color(dpg.mvThemeCol_Button, self.BTN_LOGO)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.BTN_LOGO_HOVER)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.BTN_LOGO_ACTIVE)

                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)

        return theme

    @property
    def navbar_txt(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvText):

                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))

                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)

                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)

                dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, 0.0, 0.5)

        return theme

    @property
    def primary(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.BG_PRIMARY)
        return theme

    @property
    def navbar(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.BG_NAVBAR)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
        return theme

    @property
    def footer(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.BG_PRIMARY)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
        return theme

    @property
    def exit_bg(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.BG_NAVBAR)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
        return theme

    @property
    def dc_footer_wrapper(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255, 255))
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
        return theme

    @property
    def main_container(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.BG_NAVBAR)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
        return theme

    @property
    def header(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.BG_HEADER)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
        return theme

    @property
    def font_sm(self) -> int:
        return self.__font_sm

    @property
    def font_md(self) -> int:
        return self.__font_md

    @property
    def font_lg(self) -> int:
        return self.__font_lg

    @property
    def font_navbar(self) -> int:
        return self.__font_navbar

    def apply_theme(self, component: int | str, theme: int) -> None:
        dpg.bind_item_theme(component, theme)

    def apply_font(self, component: int | str, font: int) -> None:
        dpg.bind_item_font(component, font)
