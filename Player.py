import cv2
import mediapipe as mp

from time import sleep
from WindowManager import WindowManager 
from MoleManager import MoleManager
from utils.measure_arm_information import measure_arm_distance, measure_shoulder_elbow_wrist_loc
from utils.Colors import ColorCode
from utils.PoseLandmarks import LandMarks
from utils.angle_calculaters import calculate_angle
from utils.get_player_grid_unit_id import get_grid_unit_id
from utils.get_mole_unit_locations import get_mole_locations

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
        self.distance = None # will be stored with tuple (left, right distance info)
        self.angle = None # will be stored with tuple (left, right angle info)
        self.grid_color = ColorCode.GRID_COLOR
        self.prev_shoulder_loc = None
        self.prev_index_loc = None
        self.success_crit_for_hit_mole = 100
        
        # 좌, 우 팔 선택에 따라 반전
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
        """[summary]

        Args:
            frame (numpy array): img, in case we use fram from webcam
            results ([type]): [description]
            idx ([type]): [description]

        Returns:
            tuple: (loc_x, loc_y), relative location of frame
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

    def draw_excercise_grid(self, frame, distance, monitor_info, train_arm_pos='right'):

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
            shoulder_loc = self.calculate_frame_relative_coordinate(frame, results, self.shoulder_position)
            self.prev_shoulder_loc = shoulder_loc
        except:
            shoulder_loc = self.prev_shoulder_loc

        # Calculate coordinate of current index location
        try:
            index_loc = self.calculate_frame_relative_coordinate(frame, results, self.index_position)
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
        
        win_manager = WindowManager()
        win_manager.get_screenInfo()
        win_manager.display_monitorInfo()
        win_manager.create_windows()
        self.player_win_name = win_manager.window_names['Player']
        bg_screen_size = (
            win_manager.windows_info['Mole']['height'],
            win_manager.windows_info['Mole']['width'],
        ) 

        mole_manager = MoleManager(bg_screen_size)
        
        # Processing Mole window
        frame_mole_window = mole_manager.generate_grid_on_moleWindow(win_manager)
        mole_unit_loc_list = get_mole_locations(frame_mole_window, self.divide_unit)  # location on original bg_frame (image)
        # mole_manager.create_moles(mole_unit_loc_list)
        
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print(f"\n웹캠 작동 상태: {cap.isOpened()}")
            print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
        
        while cv2.waitKey(33) < 0:
            
            _ , frame = cap.read()

            if not self.success:
                frame = cv2.flip(frame, 1)
                cv2.imshow(self.player_win_name, frame)
                _ , self.success, self.distance, self.angle, shoulder_loc = measure_arm_distance(frame, self.player_win_name)
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
                # Processing Mole window
                frame_mole_window = mole_manager.generate_grid_on_moleWindow(win_manager)
                cv2.imshow(win_manager.window_names['Mole'], frame_mole_window)

                # Processing Player window
                current_monitor_info = win_manager.windows_info['Player']
                frame_player = self.draw_excercise_grid(frame, self.distance, current_monitor_info)
                frame_player = self.draw_shoulder_and_hand_loc(frame)
                if frame_player is None:
                    continue
                
                
                # Compute arm angle -> do actions with mole image
                shoulder_loc, elbow_loc, wrist_loc, index_loc = measure_shoulder_elbow_wrist_loc(
                    frame, 
                    success_crit=self.success_crit_for_hit_mole
                )
                if shoulder_loc and elbow_loc and wrist_loc:
                    angle = calculate_angle(
                        index_loc[self.arm_position],
                        # wrist_loc[self.arm_position],
                        elbow_loc[self.arm_position],
                        shoulder_loc[self.arm_position],
                    )
                    # print('angle {0}: {1:5.1f}'.format(self.arm_position, angle))
                else:
                    continue
                
                # 일정시간 정해진 영역에 머물러 있으면 두더지 때리기 성공으로 처리
                #   -> 각도 측정이 도저히 안됨... ㅠ
                results = pose.process(frame) 
                index_pos = self.calculate_frame_relative_coordinate(frame, results, self.index_position)
                if index_pos == None:
                    continue
                pane_id = get_grid_unit_id(frame, self.divide_unit, index_pos)
                
                if pane_id != None:
                    print(f'mole_pane_id: {pane_id}\n')
                    
                else:
                    continue

                
                # 전체 이미지 처리 후 반전
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