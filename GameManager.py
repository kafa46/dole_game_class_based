from WindowManager import WindowManager
from Player import Player

class GameManager():
    
    def __init__(self, num_doles=9) -> None:
        self.num_doles = num_doles

    def start(self,):
        
        # Create window layout
        win_manager = WindowManager()
        win_manager = WindowManager()
        win_manager.get_screenInfo()
        win_manager.display_monitorInfo()
        win_manager.create_windows()

        # Activate the mole game player
        player = Player()
        player.play_game()


    def pause(self,):
        pass

    def terminate(self,):
        pass


if __name__=='__main__':
    manager = GameManager()
    manager.start()