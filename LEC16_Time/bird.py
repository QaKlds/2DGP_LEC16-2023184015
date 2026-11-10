from pico2d import *

from boy import PIXEL_PER_METER

# 비둘기 실제 크기 기준: 몸길이(부리~꼬리) 약 32cm
PIGEON_LENGTH_M = 0.32

# bird_animation.png : 5열 x 3행, 한 프레임 약 183 x 168 픽셀
FRAME_W, FRAME_H = 183, 168
# 프레임 안에서 새 몸통(꼬리~부리)이 차지하는 폭(픽셀)
BODY_W_IN_FRAME = 145

# 화면에 그려진 소년의 신발 길이(약 20px)와 비슷하게 맞춤
PIGEON_BODY_PX = 20

# 몸통 폭이 PIGEON_BODY_PX가 되도록 프레임 전체의 화면 크기 계산
DRAW_W = PIGEON_BODY_PX * FRAME_W / BODY_W_IN_FRAME  # 약 25px
DRAW_H = DRAW_W * FRAME_H / FRAME_W                  # 약 23px


class Bird:
    def __init__(self, x=800, y=540):
        self.x, self.y = x, y
        self.image = load_image('bird_animation.png')
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass  # 움직이지 않음

    def draw(self):
        # 첫 번째 프레임(좌상단)만 고정해서 출력
        self.image.clip_draw(0, self.image.h - FRAME_H, FRAME_W, FRAME_H,
                             self.x, self.y, DRAW_W, DRAW_H)
        self.font.draw(self.x - 60, self.y + 25,
                       f'Pigeon = {PIGEON_BODY_PX}px',
                       (255, 255, 255))
