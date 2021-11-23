import cv2
from copy import deepcopy
from WindowManager import WindowManager
class Mole():
    
    def __init__(self, pos_x=50, pos_y=50) -> None:
        self.moleX = 150 # mole size X
        self.moleY = 150 # mole size Y
        self.pos_x = pos_x 
        self.pos_y = pos_y
        self.wind_name = 'Mole'
        self.bg_frame =  cv2.imread('./imgs/bg_yellow.png', cv2.IMREAD_COLOR)
        self.mole_image = cv2.imread('./imgs/mole_jklee.jpg', cv2.IMREAD_COLOR)
        self.mole_image_resized = cv2.resize(self.mole_image, dsize=(self.moleX, self.moleY), interpolation=cv2.INTER_CUBIC)
        
    def img_preprocessiong(self, ):
        cv2.imshow('back ground1-src', self.bg_frame)
        cv2.imshow('mole_img-src', self.mole_image_resized)
        
        # Processing background
        frame = cv2.resize(self.bg_frame, (800, 600), cv2.INTER_CUBIC)
        frameX = round(200) - round(self.moleY*0.5)
        frameY = round(600/2) - round(self.moleX*0.5)
        cv2.imshow('back ground-resized', frame)
        
        rows, cols, _ = frame.shape
        
        # 두더지 파일 필셀 값을 관심영역(ROI)으로 저장함
        roi = frame[frameY : rows+frameY, frameX : cols+frameX] 
        print(roi.shape)
        cv2.imshow('roi', roi)
        
        # 로고 파일의 색상을 그레이로 변경
        mole_gray = cv2.cvtColor(self.mole_image, cv2.COLOR_BGR2GRAY) 
        cv2.imshow('mole_gray', mole_gray)
        
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        # 배경은 흰색으로, 그림을 검정색으로 변경
        _, mask = cv2.threshold(
            src=mole_gray,
            thresh=254,
            maxval=255,
            type=cv2.THRESH_BINARY
        )
        mask_inv = cv2.bitwise_not(mask)

        # 배경에서만 연산 = src1 배경 복사
        src1_bg = cv2.bitwise_and(roi, roi, mask=mask) 
        # src1_bg2 = cv2.bitwise_and(src1=roi, src2=roi, mask=mask)
        
        # 로고에서만 연산
        mole_image = cv2.resize(mole_gray, dsize=(self.moleX, self.moleY), interpolation=cv2.INTER_CUBIC)
        src2_fg = cv2.bitwise_and(mole_image, mole_image, mask = mask_inv) 
        
        # src1_bg와 src2_fg를 합성
        dst = cv2.bitwise_or(src1_bg, src2_fg) 
        
        frame[frameY:rows+frameY,frameX:cols+frameX] = dst #src1에 dst값 합성
        
        cv2.imshow('output', frame)
        
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        return frame
        
        return frame
        
    def show_up(self,):
        
        win_manager = WindowManager()
        win_manager.get_screenInfo()
        win_manager.display_monitorInfo()
        win_manager.create_windows()
        
        rows, cols, _ =self.mole_image.shape
        
        frame = cv2.resize(self.mole_image, (self.moleX, self.moleY), interpolation=cv2.INTER_CUBIC)
        frameX = 200 - round(rows * 0.5)
        frameY = round(600/2)-round(cols * 0.5)
        
        
        # 두더지 파일 필셀값을 관심영역(ROI)으로 저장함
        roi = frame[frameY:rows+frameY, frameX:cols+frameX] 
        cv2.imshow('Mole', self.mole_image)
       
        cv2.waitKey()
        cv2.destroyAllWindows()
    
    def disappear(self,):
        pass
    
    def adjust_size(self,):
        pass


if __name__=='__main__': 
    mole = Mole()
    mole.img_preprocessiong()
    # mole.show_up()