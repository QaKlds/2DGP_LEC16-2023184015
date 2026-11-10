from pico2d import *

import game_framework
from boy import PIXEL_PER_METER

# bird_animation.png : 5열 x 3행, 한 프레임 약 183 x 168 픽셀
FRAME_W, FRAME_H = 183, 168
# 프레임 안에서 새 몸통(꼬리~부리)이 차지하는 폭(픽셀)
BODY_W_IN_FRAME = 145

# 화면에 그려진 소년의 신발 길이(약 20px)와 비슷하게 맞춤
PIGEON_BODY_PX = 20

# 몸통 폭이 PIGEON_BODY_PX가 되도록 프레임 전체의 화면 크기 계산
DRAW_W = PIGEON_BODY_PX * FRAME_W / BODY_W_IN_FRAME  # 약 25px
DRAW_H = DRAW_W * FRAME_H / FRAME_W                  # 약 23px

# Bird Fly Speed : 근처를 느긋하게 나는 비둘기 속도 약 35km/h
FLY_SPEED_KMPH = 35.0  # Km / Hour
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)  # 약 324 px/s


class Bird:
    def __init__(self, x=800, y=540):
        self.x, self.y = x, y
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.image = load_image('bird_animation.png')

    def update(self):
        self.x += self.dir * FLY_SPEED_PPS * game_framework.frame_time

        # 화면 끝에 닿으면 방향 전환
        half_w = DRAW_W / 2
        if self.x > get_canvas_width() - half_w:
            self.x = get_canvas_width() - half_w
            self.dir = -1
        elif self.x < half_w:
            self.x = half_w
            self.dir = 1

    def draw(self):
        # 첫 번째 프레임(좌상단)만 고정해서 출력, 왼쪽으로 갈 때는 좌우 반전
        left, bottom = 0, self.image.h - FRAME_H
        if self.dir == 1:
            self.image.clip_draw(left, bottom, FRAME_W, FRAME_H,
                                 self.x, self.y, DRAW_W, DRAW_H)
        else:
            self.image.clip_composite_draw(left, bottom, FRAME_W, FRAME_H,
                                           0, 'h', self.x, self.y, DRAW_W, DRAW_H)
