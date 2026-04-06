from abc import ABC, abstractmethod
from loguru import logger

class BaseHandler(ABC):
    """
    An abstract base class for defining service handlers.

    This class provides a standardized initialization routine that logs the name of 
    the inheriting subclass. All subclasses must implement the `register` method 
    to be instantiated.

    Methods:
        __init__():
            Logs the initialization event using the `loguru.logger`, identifying 
             the specific subclass via `self.__class__.__name__`.
        register():
            An abstract method that must be overridden in subclasses to handle 
            the registration logic for the specific service.
    """
    
    def __init__(self):
        logger.info(f"Initializing handler: {self.__class__.__name__}")
        
    @abstractmethod
    def register(self) -> None:
        """
        Register the handler with the internal system.

        This method should contain the logic required to bind the subclass 
        to its respective listener or service.
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(active: True)"