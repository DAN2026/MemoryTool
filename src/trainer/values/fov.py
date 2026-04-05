from trainer.values.base_value import BaseValue


class FovValue(BaseValue):
    base_offset = 0x043E1EA0
    offsets = [0x158, 0xF0, 0xA0, 0x478, 0xAA0, 0x190, 0x158]
    value_type = "float"
