from trainer.core.memory_connection import MemoryConnection
from trainer.values.fov import FovValue


class ShooterGame:
    
    def __init__(self):
        
        conn = MemoryConnection("ShooterGame.exe")

        self.fov = FovValue(conn)
