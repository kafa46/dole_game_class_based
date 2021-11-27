import cv2

import numpy as np

def mole_show_up(
    img_top, img_bg, 
    hpos=10, vpos=10, 
    img_top_x=150, img_top_y=150, 
    moleSwitch=True
):
    
    if moleSwitch:
        rows, cols, channels = img_top.shape
        
        # hpos, vpos 파라미터를 이용해 관심영역 ROI (Region of Interest) 설정
        roi = img_bg[vpos:vpos+rows, hpos:hpos+cols]

        # 상단 이미지를 흑백(gray)으로 전환
        img_top_gray = cv2.cvtColor(img_top, cv2.COLOR_BGR2GRAY)

        _, mask = cv2.threshold(img_top_gray, 254, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)









    else:
        pass

        
    return frame_img


if __name__=='__main__':
    mole_img = cv2.imread('./imgs/mole_jklee.jpg')
    
    cap = cv2.VideoCapture(0)
    while cv2.waitKey(33) < 0:
        _ , frame = cap.read()
        frame = mole_show_up(frame, mole_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        

    pass