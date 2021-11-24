import cv2
from copy import deepcopy
from WindowManager import WindowManager

class Mole():
    
    def __init__(self, mole_unit_size_x=500, mole_unit_size_y=500, mole_unit_loc_x=10, mole_unit_loc_y=10) -> None:

        # Mole image
        self.moleX = 150 # mole size X
        self.moleY = 150 # mole size Y

        # background image
        self.bg_frame_x = 800 # resize scale x
        self.bg_frame_y = 600 # resize scale y
        self.mole_image = cv2.imread('./imgs/mole_jklee.jpg', cv2.IMREAD_COLOR)
        self.bg_frame = cv2.imread('./imgs/bg_white.png', cv2.IMREAD_COLOR)
        self.mole_image_resized = cv2.resize(self.mole_image, dsize=(self.moleX, self.moleY), interpolation=cv2.INTER_CUBIC)
        self.mole_unit_size_x = mole_unit_size_x
        self.mole_unit_size_y = mole_unit_size_y
        self.pos_x = 50
        self.pos_y = 50
        self.mole_unit_loc_x = mole_unit_loc_x
        self.mole_unit_loc_y = mole_unit_loc_y

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
        
        mole_resize_unit_size = cv2.resize(
            self.mole_image, 
            (self.mole_unit_size_x, self.mole_unit_size_y), 
            interpolation=cv2.INTER_CUBIC,
        )
        
        bg_resize_unit_size = cv2.resize(
            self.mole_image, 
            (self.mole_unit_size_x, self.mole_unit_size_y), 
            interpolation=cv2.INTER_CUBIC
        )
        
        cv2.imshow('mole - showup', mole_resize_unit_size)
        cv2.waitKey()
        cv2.destroyAllWindows()
    
    def disappear(self,):

        bg_resize_unit_size = cv2.resize(
            self.bg_frame, 
            (self.mole_unit_size_x, self.mole_unit_size_y), 
            interpolation=cv2.INTER_CUBIC
        )
        
        cv2.imshow('mole - disappear', bg_resize_unit_size)
        cv2.waitKey()
        cv2.destroyAllWindows()


if __name__=='__main__': 
    mole = Mole()
    mole.show_up()
    mole.disappear()
    
    print('Bye, end of computation ^^.')