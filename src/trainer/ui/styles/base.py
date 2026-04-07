from abc import ABC, abstractmethod
from loguru import logger

class BaseStyle(ABC):
    
    def __init__(self):
        logger.info(f"Initializing styles: {self.__class__.__name__}")
    
    @abstractmethod
    def register(self) -> None: pass
    
    @abstractmethod
    def apply(self) -> None: pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(active: True)"