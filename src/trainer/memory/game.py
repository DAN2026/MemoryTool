from trainer.values.fov import FovValue
from trainer.memory.memory_connection import MemoryConnection

class ShooterGame:
    
    def __init__(self):
        
        conn = MemoryConnection("ShooterGame.exe")

        self.fov = FovValue(conn)
