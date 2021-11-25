import cv2
from copy import deepcopy
from WindowManager import WindowManager

class Mole():
    def __init__(
        self, 
        x_start, x_end, 
        y_start, y_end, 
        mole_img, mole_id, 
        show_up_time, 
        bg_img, bg_screen_size
    ) -> None:
        
        self.x_start = int(x_start)
        self.x_end = int(x_end)
        self.y_start = int(y_start)
        self.y_end = int(y_end)
        self.wind_name = 'Mole'
        self.mole_img = mole_img
        self.mole_id = mole_id
        self.show_up_time = show_up_time
        self.bg_img = bg_img
        self.bg_img_size = bg_screen_size
        
        self.mole_img_resized = cv2.resize(
            self.mole_img, 
            (self.x_end - self.x_start, self.y_end - self.y_start), 
            interpolation=cv2.INTER_CUBIC,
        )
        
        self.bg_img_resized = cv2.resize(
            self.bg_img,
            self.bg_img_size,
            interpolation=cv2.INTER_CUBIC,
        )        

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

    def show_up(self,):
        show_up_img = self.bg_img
        print(f'show_up_img size: ({show_up_img.size})')
        show_up_img[self.x_start:self.x_end, self.y_start:self.y_end] = self.mole_img_resized
        return show_up_img
        
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