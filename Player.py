import cv2
import mediapipe as mp

from time import sleep
from WindowManager import WindowManager
from utils.measure_arm_distance import measure_arm_distance
from utils.Colors import ColorCode
from utils.PoseLandmarks import LandMarks

mpPose = mp.solutions.pose
pose = mp.solutions.pose.Pose()

class Player():
    def __init__(self, num_moles=3, divide_units=3, arm_position='right') -> None:
        self.num_moles = num_moles
        self.divide_unit = divide_units
        self.max_angle = 160
        self.min_angle = 30
        self.num_count_left = 0
        self.num_count_right = 0
        self.shrinked_left = True
        self.shrinked_right = True
        self.success = False
        self.player_win_name = 'Player'
        self.distance = None # will be stored with tuple (left, right distance info)
        self.angle = None # will be stored with tuple (left, right angle info)
        self.grid_color = ColorCode.GRID_COLOR
        
        # 좌, 우 팔 선택에 따라 반전
        self.arm_position = arm_position
        if self.arm_position == 'right':
            self.shoulder_position = LandMarks.LEFT_SHOULDER
            self.wrisk_position = LandMarks.LEFT_WRIST
            self.index_position = LandMarks.LEFT_INDEX
        elif self.arm_position == 'left':
            self.shoulder_position = LandMarks.RIGHT_SHOULDER
            self.wrisk_position = LandMarks.RIGHT_WRIST
            self.index_position = LandMarks.RIGHT_INDEX
        else:
            print(f'You selected arm position: {self.arm_position}')
            print("arm_position must be either 'right' or 'left'")
        
    
    def calculate_frame_relative_coordinate(self, frame, results, idx):
        """[summary]

        Args:
            frame (numpy array): img, in case we use fram from webcam
            results ([type]): [description]
            idx ([type]): [description]

        Returns:
            tuple: (loc_x, loc_y), relative location of frame
        """        
        x = results.pose_landmarks.landmark[idx].x
        y = results.pose_landmarks.landmark[idx].y
        # z = results.pose_landmarks.landmark[idx].z # we don't use z value, only use (x, y)
        
        frame_height, frame_width, _ = frame.shape
        loc_x = int(frame_width * x)
        loc_y = int(frame_height * y)
        
        return loc_x, loc_y

    def draw_excercise_grid(self, frame, distance, monitor_info, train_arm_pos='right'):

        try:
            results = pose.process(frame) 
        except:
            return

        # Get frame dimension from image (frame)
        frame_height, frame_width, _ = frame.shape # we don't use channel info
        
        # Calculate soulder location
        shoulder_loc = self.calculate_frame_relative_coordinate(frame, results, self.shoulder_position)

        # Calculate coordinate of current index location
        index_loc = self.calculate_frame_relative_coordinate(frame, results, self.index_position)

        ### 우선 절대 격자를 먼저 그리는 방법을 테스트 ###
        unit_dist_x = frame_width / self.divide_unit
        unit_dist_y = frame_height / self.divide_unit
        
        # Draw Horizontal lines
        for x in range(1, self.divide_unit):
            cv2.line(
                frame, 
                (0, int(unit_dist_y * x)), 
                (frame_width, int(unit_dist_y * x)), 
                self.grid_color, # green line
            )

        # Draw vertical lines
        for x in range(1, self.divide_unit):
            cv2.line(
                frame, 
                (int(unit_dist_x * x), 0), 
                (int(unit_dist_x * x), frame_height), 
                self.grid_color, # green line
            )        

        # Draw a ractangle marker on target shoulder position
        rectangle_end_loc = (shoulder_loc[0] + 30, shoulder_loc[1] - 3)
        cv2.rectangle(
            frame, 
            shoulder_loc, 
            rectangle_end_loc, 
            thickness=-1, 
            color=ColorCode.SHOULDER_MARKER
        )
        
        # Draw cicle on wrist location
        cv2.circle(
            frame, 
            (index_loc), 
            radius=10, 
            color=(0, 0, 255), 
            thickness=-1
        )

        cv2.imshow(self.player_win_name, frame)

        ### Future Work Area ###
        # # Calculate unit distance from target shoulder
        # relative_dist = max(distance['left'], distance['right'])
        # unit_dist = relative_dist * 


    def play_game(self,) -> None:
        
        win_manager = WindowManager()
        win_manager.get_screenInfo()
        win_manager.display_monitorInfo()
        win_manager.create_windows()
        self.player_win_name = win_manager.window_names[1]

        
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print(f"\n웹캠 작동 상태: {cap.isOpened()}")
            print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
        
        while cv2.waitKey(33) < 0:
            
            _ , frame = cap.read()
            
            # 이미지 좌우 반전을 먼저 수행
            frame = cv2.flip(frame, 1)
            
            if not self.success:
                cv2.imshow(self.player_win_name, frame)
            
                # print('\nMeasuring arm distance...')
                _ , self.success, self.distance, self.angle = measure_arm_distance(frame, self.player_win_name)
                # print(f'success: {success} \t Arm distance: {distance} \t Arm angle: {angle}')

                if not self.success or not self.distance:
                    continue

                elif self.success and self.distance and self.angle:
                    self.success = True
                
                else:
                    pass
            
            # 초기 팔 거리를 구하면  화면에 distance 값을 활용하여 격자 그리기
            else:
                current_monitor_info = win_manager.windows_info['Player']
                self.draw_excercise_grid(frame, self.distance, current_monitor_info)
                # sleep(1)
                

if __name__=='__main__':
    # win_manager = WindowManager()
    # win_manager.get_screenInfo()
    # win_manager.display_monitorInfo()
    # #win_manager.select_monitor()
    # win_manager.create_windows()
    player = Player()
    player.play_game()