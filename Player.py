import cv2
import numpy as np
import mediapipe as mp

from WindowManager import WindowManager
from utils.measure_arm_distance import measure_arm_distance

class Player():
    def __init__(self) -> None:
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
        self.excercise_arm_position = 'right' # 운동하는 팔은 기본적으로 오른팔로 세팅, 
                                              # 나중에 선택적으로 변경할 수 있도록 코드 수정해야 함
    
    def draw_excercise_grid(self, frame, distance, monitor_info, train_arm_pos='right'):
        
        mpDraw= mp.solutions.drawing_utils  #미디어 파이프 초록색 선 그리기
        mpPose = mp.solutions.pose
        pose = mp.solutions.pose.Pose()

        cv2.imshow('output', frame)
        results = pose.process(frame) 
        landmark = results.pose_landmarks.landmark
        
        # Extract target shoulder location
        if train_arm_pos == 'right':
            shoulder_loc = [
                landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
                landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y
            ]            
        
        else:
            shoulder_loc = [
                landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
                landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y
            ]
        
        # Calculate coordinate of current shoulder location
        window_height = monitor_info['height']
        window_width = monitor_info['width']
        
        shoulder_x = int(window_height * shoulder_loc[0])
        shoulder_y = int(window_width * shoulder_loc[1])
        shoulder_loc = (shoulder_x, shoulder_y)
        
        # 우선 절대 격자를 먼저 그리는 방법을 테스트
        target_loc = (shoulder_x + 30, shoulder_y)
        cv2.line(frame, shoulder_loc, target_loc, (0, 0, 255))

        cv2.imshow(self.player_win_name, frame)

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
            
                print('\nMeasuring arm distance...')
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
                pass
                




if __name__=='__main__':
    # win_manager = WindowManager()
    # win_manager.get_screenInfo()
    # win_manager.display_monitorInfo()
    # #win_manager.select_monitor()
    # win_manager.create_windows()
    player = Player()
    player.play_game()