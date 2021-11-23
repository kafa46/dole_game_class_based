import cv2
from copy import deepcopy
from WindowManager import WindowManager

class Mole():
    
    def __init__(
        self, pos_x=50, pos_y=50, 
        mole_img_path='./imgs/mole_jklee_no_bg.png',
        bg_img_path='./imgs/bg_yellow.png',
    ) -> None:

        # Mole image
        self.moleX = 150 # mole size X
        self.moleY = 150 # mole size Y
        self.mole_image_path = mole_img_path
        self.mole_img = None

        # background image
        self.bg_frame_x = 800 # resize scale x
        self.bg_frame_y = 600 # resize scale y
        self.bg_frame_path =  bg_img_path
        self.bg_frame_img = None
        
        self.pos_x = pos_x 
        self.pos_y = pos_y

        self.wind_name = 'Mole'
    
    def load_mole_and_background_imgs(self,):
        try:
            mole_img = cv2.imread(self.mole_image_path, cv2.IMREAD_COLOR)
            bg_frame_img = cv2.imread(self.bg_frame_path, cv2.IMREAD_COLOR)
        except:
            return None
        
        return mole_img, bg_frame_img

    def resize_img(self, img, x, y):
        image_resized = cv2.resize(img, dsize=(x, y), interpolation=cv2.INTER_CUBIC)
        return image_resized

    def img_preprocessiong(self, ):
        mole_img, bg_frame_img = self.load_mole_and_background_imgs()
        # cv2.imshow('mole_img - src', mole_img)
        # cv2.imshow('bg_frame_img - src', bg_frame_img)
        cv2.namedWindow('screen')
        
        
        
        mole_img_resized = self.resize_img(mole_img, self.moleX, self.moleY)
        bg_frame_img_resized = self.resize_img(bg_frame_img, self.bg_frame_x, self.bg_frame_y)
        # cv2.imshow('bg_frame_img_resized', bg_frame_img_resized)
        # cv2.imshow('mole_img_resized', mole_img_resized)
        cv2.imshow('screen', bg_frame_img_resized)
        cv2.imshow('screen', mole_img_resized)
        # Processing background
        frameX = round(200) - round(self.moleY*0.5)
        frameY = round(600/2) - round(self.moleX*0.5)
        
        rows, cols, _ = bg_frame_img_resized.shape
        
        # 두더지 이미지를 배경화면의 원하는 부분에 두기 위한 영역 지정
        #   -> 두더지 파일 필셀 값을 관심영역(ROI)으로 저장
        roi = bg_frame_img_resized[frameY : rows + frameY, frameX : cols + frameX] 
        print(roi.shape)
        cv2.imshow('roi', roi)
        
        # 두더지 이미지를 위한 마스크와 역마스크 생성 준비
        #   -> 두더지 색상을 그레이로 변경
        mole_gray = cv2.cvtColor(mole_img_resized, cv2.COLOR_BGR2GRAY) 
        cv2.imshow('mole_gray', mole_gray)

        # 마스크 생성
        _, mask = cv2.threshold(  
            src=mole_gray,
            thresh=254,
            maxval=255,
            type=cv2.THRESH_BINARY
        )
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        # 역마스크 생성
        mask_inv = cv2.bitwise_not(mask) 

        # 두더지 이미지에서 해당하는 부분만 검정색 만들기
        masked_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        cv2.imshow('masked_bg', masked_bg)

        
        
        # 배경은 흰색으로, 그림을 검정색으로 변경
        
        
        # 참고 블로그
        #   -> https://m.blog.naver.com/samsjang/220503082434 

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