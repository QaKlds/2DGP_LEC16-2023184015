import random

from pico2d import *

import game_framework
from boy import PIXEL_PER_METER

# bird_animation.png : 918 x 506, 5열 x 3행 (마지막 행은 4개) = 총 14프레임
FRAME_COLS, FRAME_ROWS, FRAME_COUNT = 5, 3, 14
FRAME_W, FRAME_H = 183, 168
CELL_W, CELL_H = 918 / FRAME_COLS, 506 / FRAME_ROWS  # 칸 간격 (183.6 x 168.7)
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

FLAP_LENGTH_M = 2.0  # 날개 1회 펄럭일 때 날아가는 거리
FLY_FRAMES_PER_FLAP = FRAME_COUNT  # 날갯짓 1회 = 14프레임
# 1초당 프레임 증가량 = 9.72 / 2 * 14 ≈ 68
FLY_FRAMES_PER_SECOND = FLY_SPEED_MPS / FLAP_LENGTH_M * FLY_FRAMES_PER_FLAP


# 새가 날아다니는 하늘 높이 범위 (y 좌표)
SKY_Y_MIN, SKY_Y_MAX = 300, 570
# 위아래로 천천히 오르내리는 속도 범위 : 최대 1m/s
VERT_SPEED_MAX_PPS = 1.0 * PIXEL_PER_METER  # 약 33 px/s


class Bird:
    image = None  # 10마리가 이미지를 공유하도록 한 번만 로드

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        half_w = DRAW_W / 2
        self.x = random.uniform(half_w, get_canvas_width() - half_w)
        self.y = random.uniform(SKY_Y_MIN, SKY_Y_MAX)
        self.dir = random.choice([-1, 1])  # 1: 오른쪽, -1: 왼쪽
        self.dy = random.uniform(-VERT_SPEED_MAX_PPS, VERT_SPEED_MAX_PPS)
        self.frame = random.uniform(0, FRAME_COUNT)  # 날갯짓 타이밍이 서로 다르게

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FLY_FRAMES_PER_SECOND * dt) % FRAME_COUNT
        self.x += self.dir * FLY_SPEED_PPS * dt
        self.y += self.dy * dt

        # 화면 좌우 끝에 닿으면 방향 전환
        half_w = DRAW_W / 2
        if self.x > get_canvas_width() - half_w:
            self.x = get_canvas_width() - half_w
            self.dir = -1
        elif self.x < half_w:
            self.x = half_w
            self.dir = 1

        # 하늘 범위의 위아래 끝에 닿으면 반대로
        if self.y > SKY_Y_MAX:
            self.y = SKY_Y_MAX
            self.dy = -abs(self.dy)
        elif self.y < SKY_Y_MIN:
            self.y = SKY_Y_MIN
            self.dy = abs(self.dy)

    def draw(self):
        # 시트는 좌상단부터 행 순서로 진행, 왼쪽으로 갈 때는 좌우 반전
        i = int(self.frame)
        col, row = i % FRAME_COLS, i // FRAME_COLS
        left = int(col * CELL_W)
        bottom = int(self.image.h - (row + 1) * CELL_H)
        if self.dir == 1:
            self.image.clip_draw(left, bottom, FRAME_W, FRAME_H,
                                 self.x, self.y, DRAW_W, DRAW_H)
        else:
            self.image.clip_composite_draw(left, bottom, FRAME_W, FRAME_H,
                                           0, 'h', self.x, self.y, DRAW_W, DRAW_H)
