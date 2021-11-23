import cv2

def combine_bitwise(hpos, vpos, src_img_path, dst_img_path):
    base_img = cv2.imread(src_img_path, cv2.IMREAD_COLOR) # 배경
    top_img = cv2.imread(dst_img_path, cv2.IMREAD_COLOR) # 두더지

    # 전처리: 이미지 크기 조정
    base_img = cv2.resize(base_img, (800, 600), interpolation=cv2.INTER_CUBIC)
    top_img = cv2.resize(base_img, (800, 600), interpolation=cv2.INTER_CUBIC)
    
    # 두더지 사진을 원하는 위치(hpos, vpos) 윗부분에
    # 위치시키기 위한 영역 지정
    rows, cols, _ = base_img.shape
    roi = base_img[vpos:rows+vpos, hpos:hpos+cols]

    # 두더지를 위안 마스크와 역마스크 생성하기
    img2gray = cv2.cvtColor(top_img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # ROI에서 두더지에 해당하는 부분만 검정색으로 만들기
    # 
    # 이 부분에서 계속 에러가 발생합니다. ㅠㅠ
    # 
    base_img_background = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # 두더지 이미지에서 두더지만 추출하기
    top_img_foreground = cv2.bitwise_and(top_img, top_img, mask=mask)

    # 배경없는 두더지를 ROI 영역에 합치기
    dst = cv2.add(base_img_background, top_img_foreground)

    # 원래 배경에 합쳐진 이미지를 반영하기
    base_img[vpos:vpos+rows, hpos:hpos+cols] = dst

    cv2.imshow('result', base_img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__=='__main__':
    bg_dir = './imgs/bg_yellow.png'
    top_dir = './imgs/mole_jklee_no_bg.png'
    combine_bitwise(10, 10, bg_dir, top_dir)
