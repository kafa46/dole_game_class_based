import cv2
import numpy as np

from PIL import ImageFont, ImageDraw, Image
from utils.Colors import ColorCode

class InformationManager():
    '''
    Display information about mole game
    '''
    def __init__(self, goal_to_complete):
        self.hit_num_to_complete = goal_to_complete
        self.current_hit_num = 0
        self.pane_move_num = 0
        self.left_margin = 5
        self.right_margin = 5
        self.text_line_space = 10
        self.bg_img = cv2.imread('./imgs/bg_white.png', cv2.IMREAD_COLOR)
        
    def increase_hit_number(self,):
        self.current_hit_num += 1

    def increase_pane_movement(self,):
        self.pane_move_num += 1
    
    def check_mission_complete(self,):
        if self.current_hit_num >= self.hit_num_to_complete:
            return True
        else:
            return False
        
    def reset_game(self,):
        self.current_hit_num = 0
        self.pane_move_num = 0
    
    def display_game_info(self, window_size_height, window_size_width):
        
        frame = cv2.resize(self.bg_img, (window_size_width, window_size_height), cv2.INTER_CUBIC)
        
        # 화면을 2:1 비율로 분할
        win_width_unit = int(window_size_width/4)
        win_height_unit = int(window_size_height/3)
        
                
        # 운동량 바깥 사각형 -> 오른쪽 2칸 unit 중앙에 현재/목표수 gage 출력
        outer_rectangle_start_point = (self.left_margin, win_height_unit)
        outer_rectangle_end_point = (self.left_margin + win_width_unit*2, win_height_unit*2)
        cv2.rectangle(
            frame,
            pt1=outer_rectangle_start_point,  # 시작점 좌표(x, y)
            pt2=outer_rectangle_end_point, # 종료점 좌표(x, y)
            color=ColorCode.RED, 
            thickness=1, # 선 두께, default=1
        )
        
        # 운동량 안쪽 사각형 -> 오른쪽 2칸 unit 중앙에 현재/목표수 gage 출력
        current_count_length = int(
            (self.left_margin + win_width_unit*2) / (self.hit_num_to_complete + 1e-5) * self.current_hit_num
        )
        cv2.rectangle(
            frame,
            pt1=outer_rectangle_start_point,  # 시작점 좌표(x, y)
            pt2=(current_count_length, win_height_unit*2), # 종료점 좌표(x, y)
            color=ColorCode.RED, 
            # color=cv2.COLORMAP_TURBO,
            thickness=-1, # 선 두께, default=1, -1일 경우 가득 채우기
        )
        
        # 왼쪽 1칸에 목표 hit, 현재 hit, pane 이동수 출력
        cv2.rectangle(
            frame,
            pt1=(self.left_margin + win_width_unit*2 + 10, 10),  # 시작점 좌표(x, y)
            pt2=(window_size_width-10, window_size_height-10), # 종료점 좌표(x, y)
            color=ColorCode.GREEN, 
            thickness=-1, # 선 두께, default=1
        )
        
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text(
            xy=(
                self.left_margin + win_width_unit*2 + self.text_line_space*5 -2, 
                self.text_line_space * 5 - 2
            ), 
            text=str(int(self.current_hit_num / (self.hit_num_to_complete * 100 + 1e-5))) + r'%', 
            font=ImageFont.truetype('fonts/nanum/NanumBarunGothic/NanumBarunGothicBold.ttf', 10), 
            fill=(0,0,255)
        )
        frame = np.array(img_pil)
        
        return frame
        

if __name__=='__main__':
    pass