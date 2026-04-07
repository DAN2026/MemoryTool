from abc import ABC
from loguru import logger


class BaseComponent(ABC):
    
    def __init__(self):
        logger.info(f"Initializing component: {self.__class__.__name__}")
    
    def build(self) -> None:
        
        logger.success(f"Built component: {self.__class__.__name__}")

