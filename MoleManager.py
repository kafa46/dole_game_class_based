
from time import sleep
import cv2
import numpy as np

from WindowManager import WindowManager
from utils.Colors import ColorCode
from Mole import Mole

class MoleManager():
    
    def __init__(self, divide_unit=3) -> None:
        self.divide_unit = divide_unit
        self.win_name = 'Mole'
        self.bg_frame =  cv2.imread('./imgs/bg_yellow.png', cv2.IMREAD_COLOR)
    
    def get_mole_unit_locations(self):
        frame_height, frame_width, _ = self.bg_frame.shape
        
        # Calculate unit-distance 
        unit_dist_x = frame_width / self.divide_unit
        unit_dist_y = frame_height / self.divide_unit
 
        # Calculate mole unit locations
        mole_unit_loc = {}
        cnt = 1
        for x in range(self.divide_unit):
            for y in range(self.divide_unit):
                mole_unit_loc[cnt] = {
                    'mole_loc': (x * int(unit_dist_x), y * int(unit_dist_y)),
                    'unit_dist_x': int(unit_dist_x),
                    'unit_dist_y': int(unit_dist_y),
                }
                cnt += 1
                
        return mole_unit_loc        
            
    def generate_grid_on_moleWindow(self, win_manager):
        
        # win_manager = WindowManager()
        # win_manager.get_screenInfo()
        # win_manager.display_monitorInfo()
        # win_manager.create_windows()
        
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

        # while cv2.waitKey(33) < 0:
            
        #     # Draw Horizontal lines
        #     for x in range(1, self.divide_unit):
        #             cv2.line(
        #             self.bg_frame, 
        #             (0, int(unit_dist_y * x)), 
        #             (frame_width, int(unit_dist_y * x)), 
        #             self.grid_color, # green line
        #         )

        #     # Draw vertical lines
        #     for x in range(1, self.divide_unit):
        #         cv2.line(
        #             self.bg_frame, 
        #             (int(unit_dist_x * x), 0), 
        #             (int(unit_dist_x * x), frame_height), 
        #             self.grid_color, # green line
        #         )    
            
        #     cv2.imshow(self.win_name, self.bg_frame)
        
    def create_moles(self,):
        # Compute mole locations
        # Create required moles
        pass
        
            


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
    
    
    