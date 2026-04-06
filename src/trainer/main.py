# from trainer.memory.game import ShooterGame


# def main():
    
#     game = ShooterGame()

#     game.fov.set(1.25)


# if __name__ == "__main__":
#     main()

import dearpygui.dearpygui as dpg

from trainer.ui.app import App

def main() -> None:
    __app = App()
    
    __app.start()

if __name__ == "__main__":
    main()