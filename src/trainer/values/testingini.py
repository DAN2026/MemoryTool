from trainer.values.base_value import BaseValue


class TestingtINI(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x0437FE60

    @property
    def offsets(self) -> list[int]:
        return [0x90]

    @property
    def value_type(self) -> str:
        return "float"
