import time
import math
import dearpygui.dearpygui as dpg
from typing import List, Union


class RotationTransition:
    """
    Handles a 360-degree rotation using a transformation matrix.
    """
    __slots__ = ("__target", "__duration", "__t", "__active", "__last", "__center")

    def __init__(
        self,
        target: Union[str, int],
        center: List[float],
        duration: float = 0.5,
    ) -> None:
        self.__target: Union[str, int] = target
        self.__center: List[float] = center
        self.__duration: float = duration
        self.__t: float = 0.0
        self.__active: bool = False
        self.__last: float = time.time()

    @property
    def target(self) -> Union[str, int]:
        """Returns the target node tag."""
        return self.__target

    def trigger(self) -> None:
        """Starts the rotation sequence."""
        if not self.__active:
            self.__active = True
            self.__t = 0.0
            self.__last = time.time()

    def tick(self) -> None:
        """Processes the rotation matrix frame by frame."""
        if not self.__active:
            return

        now = time.time()
        delta = now - self.__last
        self.__last = now

        if self.__t < 1.0:
            self.__t = min(1.0, self.__t + (delta / self.__duration))

            rad = self.__t * (math.pi * 2)

            t_origin = dpg.create_translation_matrix([-self.__center[0], -self.__center[1]])
            rotate = dpg.create_rotation_matrix(rad, [0, 0, 1])
            t_back = dpg.create_translation_matrix([self.__center[0], self.__center[1]])

            combined = t_back * rotate * t_origin
            dpg.apply_transform(self.__target, combined)

            if self.__t >= 1.0:
                self.__active = False
                identity = dpg.create_rotation_matrix(0, [0, 0, 1])
                dpg.apply_transform(self.__target, identity)
