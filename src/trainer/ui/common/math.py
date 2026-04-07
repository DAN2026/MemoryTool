import dearpygui.dearpygui as dpg

class Math():
    
    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def lerp_color(c1, c2, t):
        return (
            int(Math.lerp(c1[0], c2[0], t)),
            int(Math.lerp(c1[1], c2[1], t)),
            int(Math.lerp(c1[2], c2[2], t)),
            int(Math.lerp(c1[3], c2[3], t)),
        )
        
    @staticmethod
    def centre_text_indent(container_width: float, text: str, font=None) -> float:
        size = dpg.get_text_size(text, font=font)
        if size is None:
            return container_width / 2
        return (container_width - size[0]) / 2
    
    @staticmethod
    def centre_indent(container_width: float, item_width: float) -> float:
        return (container_width - item_width) / 2