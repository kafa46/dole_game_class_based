
from time import sleep
import cv2
import numpy as np

from WindowManager import WindowManager
from utils.Colors import ColorCode
from Mole import Mole

class MoleManager():
    def __init__(self, bg_screen_size, divide_unit=3) -> None:
        self.divide_unit = divide_unit
        self.win_name = 'Mole'
        self.bg_frame =  cv2.imread('./imgs/bg_yellow.png', cv2.IMREAD_COLOR)
        self.mole_list = None
        self.mole_img = cv2.imread('./imgs/mole_jklee.jpg', cv2.IMREAD_COLOR)
        self.show_up_time = 1
        self.bg_screen_size = bg_screen_size
            
    def generate_grid_on_moleWindow(self, win_manager):
        
        # get window size
        win_height = win_manager.windows_info[self.win_name]['height']
        win_width = win_manager.windows_info[self.win_name]['width']
        
        frame_height, frame_width, _ = self.bg_frame.shape
        # print(f'height: {frame_height}, width: {frame_width}')
        
        # Calculate unit-distance 
        unit_dist_x = frame_width / self.divide_unit
        unit_dist_y = frame_height / self.divide_unit

        # Draw Horizontal lines
        for x in range(1, self.divide_unit):
                cv2.line(
                self.bg_frame, 
                (0, int(unit_dist_y * x)), 
                (frame_width, int(unit_dist_y * x)), 
                ColorCode.RED, 
            )

        # Draw vertical lines
        for x in range(1, self.divide_unit):
            cv2.line(
                self.bg_frame, 
                (int(unit_dist_x * x), 0), 
                (int(unit_dist_x * x), frame_height), 
                ColorCode.RED, 
            )    
        
        return self.bg_frame

        
    def create_moles(self, mole_locations):
        ''' 
        Compute mole locations, Create required moles
        Args:
            mole_num [int]: the number of moles in this game
            mole_locations [list]: [((x_start, x_end), (y_start, y_end)), ... ]
        '''
        mole_list = []
        for idx,  (x_range, y_range)  in enumerate(mole_locations):
            mole = Mole(
                x_start=x_range[0],
                x_end=x_range[1],
                y_start=y_range[0],
                y_end=y_range[1],
                mole_img=self.mole_img,
                mole_id=idx,
                show_up_time=self.show_up_time,
                bg_img=self.bg_frame,
                bg_screen_size=self.bg_screen_size
            )
            mole_list.append(mole)
        self.mole_list = mole_list
        
            


if __name__=='__main__':
    # img = cv2.imread('./managers/imgs/mole.png', cv2.IMREAD_COLOR)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print()
    
    mole_manager = MoleManager()
    mole_manager.generate_grid_on_moleWindow()
    # frame = mole_manager.generate_grid_on_moleWindow()
    
    print('Bye, end of computation ^^')
    
    
    