import cv2
from random import randint
import mediapipe as mp

from time import sleep
from WindowManager import WindowManager 
from MoleManager import MoleManager
from utils.Criteria import Criteria
from utils.Timer import Timer
from utils.measure_arm_information import measure_arm_distance, measure_shoulder_elbow_wrist_loc
from utils.Colors import ColorCode
from utils.PoseLandmarks import LandMarks
from utils.angle_calculaters import calculate_angle
from utils.get_player_grid_unit_id import get_grid_unit_id
from utils.get_mole_unit_locations import get_grid_locations, get_grid_unit_distace
from utils.mole_show_up import mole_show_up

mpPose = mp.solutions.pose
pose = mp.solutions.pose.Pose()

class Player():
    def __init__(self, divide_units=3, arm_position='right') -> None:
        self.divide_unit = divide_units
        self.max_angle = 160
        self.min_angle = 30
        self.num_count_left = 0
        self.num_count_right = 0
        self.shrinked_left = True
        self.shrinked_right = True
        self.success = False
        self.distance = None # will be stored with tuple (left, right distance info)
        self.angle = None # will be stored with tuple (left, right angle info)
        self.grid_color = ColorCode.GRID_COLOR
        self.prev_shoulder_loc = None
        self.prev_index_loc = None
        self.mole_hit_success = False
        self.current_pane_id = None
        self.target_pane_id = None
        self.IS_FIRST = True
        
        # 좌/우 팔 선택에 따라 해당 좌표 정보를 할당
        self.arm_position = arm_position
        if self.arm_position == 'right':
            self.shoulder_position = LandMarks.RIGHT_SHOULDER
            self.wrisk_position = LandMarks.RIGHT_WRIST
            self.index_position = LandMarks.RIGHT_INDEX
        elif self.arm_position == 'left':
            self.shoulder_position = LandMarks.LEFT_SHOULDER
            self.wrisk_position = LandMarks.LEFT_WRIST
            self.index_position = LandMarks.LEFT_INDEX
        else:
            print(f'You selected arm position: {self.arm_position}')
            print("arm_position must be either 'right' or 'left'")
        
        super().__init__()  
        
    
    def calculate_frame_relative_coordinate(self, frame, results, idx):
        """cv.image.shape에서 리턴하는 상대적 좌표를 입력으로 주어진
        frame 이미지에 적용하여 이미지상에 적용할 수 있는 좌표를 리턴합니다.

        Args:
            frame (numpy array): img (cv2 object), in case we use fram from webcam
            results (mediapipe pose object): object after processing 'mediapipe의 pose.process(frame)'
            idx (int): the target landmark index in result object

        Returns:
            loc_x, loc_y (tuple): relative location of frame
        """     
        
        try:
            x = results.pose_landmarks.landmark[idx].x
            y = results.pose_landmarks.landmark[idx].y
            # z = results.pose_landmarks.landmark[idx].z # we don't use z value, only use (x, y)
        except:
            return None
        
        frame_height, frame_width, _ = frame.shape
        loc_x = int(frame_width * x)
        loc_y = int(frame_height * y)
        
        return loc_x, loc_y


    def draw_excercise_grid(self, frame):

        # Get frame dimension from image (frame)
        frame_height, frame_width, _ = frame.shape # we don't use channel info

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

        # cv2.imshow(self.player_win_name, frame)

        return frame


    def draw_shoulder_and_hand_loc(self, frame):
        try:
            results = pose.process(frame) 
        except:
            return

        # Calculate soulder location
        try:
            shoulder_loc = self.calculate_frame_relative_coordinate(
                frame, 
                results, 
                self.shoulder_position
            )
            self.prev_shoulder_loc = shoulder_loc
        except:
            shoulder_loc = self.prev_shoulder_loc

        # Calculate coordinate of current index location
        try:
            index_loc = self.calculate_frame_relative_coordinate(
                frame, 
                results, 
                self.index_position
            )
        except:
            index_loc = self.prev_index_loc
        
        # Draw a ractangle marker on target shoulder position
        try:
            rectangle_end_loc = (shoulder_loc[0] + 30, shoulder_loc[1] - 3)
        except:
            return None
        
        # Draw rectangle on shoulder location
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

        return frame
    

    def play_game(self,) -> None:
        MOVE_TO_NEW_LOCATION = True
        win_manager = WindowManager()
        win_manager.get_screenInfo()
        win_manager.display_monitorInfo()
        win_manager.create_windows()
        self.player_win_name = win_manager.window_names['Player']
        bg_screen_size = (
            win_manager.windows_info['Mole']['height'],
            win_manager.windows_info['Mole']['width'],
        ) 

        mole_manager = MoleManager(bg_screen_size, divide_unit=self.divide_unit)
        pane_timer = Timer()
        
        # Processing Mole window
        frame_mole_window = mole_manager.create_background_image(win_manager)
        
        mole_unit_loc_list = get_grid_locations(
            frame_mole_window, 
            self.divide_unit        
        )
        
        unit_distances = get_grid_unit_distace(
            frame_mole_window, 
            self.divide_unit
        )
        
        cap = cv2.VideoCapture(0)

        if cap.isOpened():
            print(f"\n웹캠 작동 상태: {cap.isOpened()}")
            print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
        
        while cv2.waitKey(33) < 0:
            _ , frame = cap.read()

            if not self.success:
                frame = cv2.flip(frame, 1)
                cv2.imshow(self.player_win_name, frame)
                _ , self.success, self.distance, self.angle, shoulder_loc = measure_arm_distance(
                    frame, self.
                    player_win_name
                )
                
                if not self.success or not self.distance or not shoulder_loc:
                    continue
                
                elif self.success and self.distance and self.angle and shoulder_loc:
                    self.success = True
                    try:
                        results = pose.process(frame) 
                        self.prev_shoulder_loc = self.calculate_frame_relative_coordinate(
                            frame, results, self.shoulder_position
                        )
                    except:
                        continue
                else:
                    continue
            
            else:
                # Processing Player window
                current_monitor_info = win_manager.windows_info['Player']
                frame_player = self.draw_excercise_grid(frame)
                frame_player = self.draw_shoulder_and_hand_loc(frame)
                if frame_player is None:
                    continue
                
                # Compute arm angle -> do actions with mole image
                shoulder_loc, elbow_loc, wrist_loc, index_loc = measure_shoulder_elbow_wrist_loc(
                    frame, 
                    success_crit=Criteria.SUCCESS_ARM_ANGLE_TO_HIT_MOLE
                )

                if shoulder_loc and elbow_loc and wrist_loc:
                    angle = calculate_angle(
                        index_loc[self.arm_position],
                        # wrist_loc[self.arm_position],
                        elbow_loc[self.arm_position],
                        shoulder_loc[self.arm_position],
                    )
                
                else:
                    continue
                
                # 일정시간 정해진 영역에 머물러 있으면 두더지 때리기 성공으로 처리
                #   -> 각도 측정이 도저히 안됨... ㅠ
                #   대안 1: 임준환 멀티 카메라 심험결과 적용
                #   대안 2: mediapipe 3D coordinate를 활용한 추가 실험
                results = pose.process(frame) 
                index_pos = self.calculate_frame_relative_coordinate(frame, results, self.index_position,)
                
                if index_pos == None:
                    continue
                
                self.current_pane_id = get_grid_unit_id(frame, self.divide_unit, index_pos)

                if self.IS_FIRST:
                    self.target_pane_id = self.current_pane_id
                    self.IS_FIRST = False
                
                if self.current_pane_id != None:
                    # 두더지가 현재 pane에서 머물러 있는 시간을 체크하고,
                    # 일정 시간 (Criteria.SUCCESS_ARM_ANGLE_TO_HIT_MOLE) 이상 지난 경우
                    # pane ID를 랜덤하게 추출하여 두더지 위치 변경
                    if self.current_pane_id == self.target_pane_id:
                        pane_stay_time = pane_timer.update(self.target_pane_id)
                    else:
                        pane_stay_time = 0.0

                    self.mole_hit_success = pane_stay_time >= Criteria.MIN_STAY_TIME_IN_PANE
                    
                    if self.mole_hit_success:
                        MOVE_TO_NEW_LOCATION = True
                    else:
                        MOVE_TO_NEW_LOCATION = False
                    
                    print('Current Pane: {0} Target Pane: {1} \
                        pane_stay_time: {2:3.1f} \ hit_success: {3}'.format(
                            self.current_pane_id, 
                            self.target_pane_id,
                            pane_stay_time, self.
                            mole_hit_success,
                        ), 
                    )
                    
                    if MOVE_TO_NEW_LOCATION: 
                        while True:
                            next_pane_id = randint(0, self.divide_unit**2 - 1)    
                            if self.target_pane_id != next_pane_id:
                                self.current_pane_id = self.target_pane_id
                                self.target_pane_id = next_pane_id
                                # MOVE_TO_NEW_LOCATION = False
                                break
                        
                    mole_img = mole_show_up(
                        img_top=mole_manager.mole_img,
                        img_bg=mole_manager.bg_frame,
                        hpos=int(mole_unit_loc_list[self.target_pane_id][0][0]), 
                        vpos=int(mole_unit_loc_list[self.target_pane_id][1][0]),
                        img_top_x=unit_distances[0], 
                        img_top_y=unit_distances[1],
                        img_bg_x=bg_screen_size[0],  
                        img_bg_y=bg_screen_size[1],
                    )
                    mole_img = mole_manager.draw_grids_on_mole_window(mole_img)
                    mole_img = cv2.flip(mole_img, 1)
                    cv2.imshow(win_manager.window_names['Mole'], mole_img)
                
                else:
                    continue

                
                # 전체 이미지 처리 후 Player 화면 반전
                frame_player = cv2.flip(frame_player, 1)
                cv2.imshow(win_manager.window_names['Player'], frame_player)
                

if __name__=='__main__':
    # win_manager = WindowManager()
    # win_manager.get_screenInfo()
    # win_manager.display_monitorInfo()
    # #win_manager.select_monitor()
    # win_manager.create_windows()
    player = Player()
    player.play_game()