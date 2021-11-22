
import cv2
import numpy as np

from WindowManager import WindowManager
from utils.Colors import ColorCode

class MoleManager():
    def __init__(self, divide_units=3) -> None:
        self.divide_units = divide_units
        self.win_name = 'Dole'


    def generate_grid_on_moleWindow(self, ):
        # get window size
        height = win_manager.windows_info[self.win_name]['height']
        width = win_manager.windows_info[self.win_name]['width']
        print(height, width)
        
        
        # create empty image to fill out the window
        # 빈 이미지를 준비하는게 좋을 듯.... ㅠㅠ
        frame = np.zeros((height, width, 3), np.uint8)

        cv2.imshow(self.win_name, frame)
        print()


        # generate grid using created image
        pass

if __name__=='__main__':
    win_manager = WindowManager()
    win_manager.get_screenInfo()
    win_manager.display_monitorInfo()
    win_manager.create_windows()
    mole_manager = MoleManager()
    mole_manager.generate_grid_on_moleWindow()