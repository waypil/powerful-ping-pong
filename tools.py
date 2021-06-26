""" Project PPP v0.1.2 """

import math
import random
import time  # processing_time_gauge()에 사용. Framewatch/Time에 사용하지 않음
from typing import Union

from _base import *


def processing_time_gauge(func):  # method/function의 처리 속도 측정 데코레이터
    def __get_result(end_time, per_frame):
        spf = 1 / per_frame  # seconds_per_frame
        safety, notice, caution, warning = spf / 10, spf / 5, spf / 2, spf

        if safety > end_time:
            return SAFETY  # 안전
        elif notice > end_time:
            return NOTICE  # 유의
        elif caution > end_time:
            return CAUTION  # 주의: frame drop에 영향을 줄 수 있음.
        if warning > end_time:
            return WARNING  # 경고: frame drop이 발생할 수 있음. 최적화 요망.
        else:
            return DANGER  # 위험: frame drop 발생 중. 최적화 필수.

    def wrapper(*args, **kwargs):
        try:  # class method or instance method
            self, args = args[0], args[1:]

            if self.__class__.__name__ == 'type':  # class method
                name = self.__name__ + '.'
            else:  # instance method
                name = self.__class__.__name__ + '.'

            start_time = time.time()  # 처리 속도 측정 시작
            returned = func(self, *args, **kwargs)  # 처리 속도 측정 중
            end_time = time.time() - start_time  # 측정 종료

        except IndexError:  # static method or function
            name = ''
            start_time = time.time()  # 처리 속도 측정 시작
            returned = func(*args, **kwargs)  # 함수 실행 & 처리 속도 측정 중
            end_time = time.time() - start_time  # 측정 종료

        if end_time != 0.0 and (result := __get_result(end_time, FPS)):
            print(f"{name}{func.__name__}() : {end_time}  [{result}]")

        if returned is not None:
            return returned

    return wrapper


class Text:
    def __init__(self, fontname, size, color, xy: tuple, background=None,
                 antialias=True):
        self.size = size
        self.color = color
        self.x, self.y = xy
        self.background = background
        self.antialias = antialias
        self.fontname = fontname
        self.font = pg.font.Font(f'resources/fonts/{fontname}.ttf', size)

    def write(self, sentence, xy: tuple = (None, None)):
        text = self.font.render(
            f'{sentence}', self.antialias, self.color, self.background)

        x, y = xy
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        Screen.on.blit(text, [x, y])

    def change_size(self, size):
        self.size = size
        self.font = pg.font.Font(f'resources/{self.fontname}.ttf', size)

    def change_color(self, color):
        self.color = color

    def change_position(self, x, y):
        self.x, self.y = x, y

    def change_background(self, color):
        self.background = color

    def change_antialias(self, boolean):
        self.antialias = boolean


class Framewatch:
    """Default is 100 fps.
    """
    now = 0

    @classmethod
    def tick(cls):
        cls.now += 1

    def __init__(self, mode, min_sec=0, max_sec=0):
        if 0 < min_sec < 0.01 or 0 < max_sec < 0.01:
            raise ValueError(
                "min_sec/max_sec in Framewatch.__init__() must be large number than 0.01.max")

        self.mode = mode
        self.min_limit = int(min_sec * 100)  # use in 'ANTI-MASHING'
        self.max_limit = int(max_sec * 100)  # use in 'TIMER'

        self.running = False
        self.__preset = 0
        self.__checkpoint = None

    def check(self):  # 'TIMER' 모드에서 check를 안 하면 스톱워치가 됨.
        if self.mode == 'TIMER':
            if self.running:
                if self.max_limit == 0 or self.get_elapsed() < self.max_limit:
                    return True
                else:  # 제한 시간 초과
                    self.off()
                    print("\nTime is over!\n")
                    return False
            else:
                return False

        elif self.mode == 'ANTI-MASHING':  # 연타 방지 센서 (RestrictButtonMashing)
            elapsed = self.get_elapsed()
            if elapsed == 0:
                self.start()
                return True  # True: 연타 허용
            elif elapsed >= self.min_limit:
                self.reset()
                return True  # True: 연타 허용
            else:
                return False  # False: 연타 불허
        else:
            raise ValueError(
                "Please input mode='TIMER' or mode='ANTI-MASHING'")

    def get_elapsed(self):
        """현재까지의 스톱워치 재생 시간 취득arrange
        """
        elapsed = self.__preset
        if self.running:
            elapsed = self.__class__.now - self.__checkpoint
        return elapsed

    def start(self):  # 스톱워치 시작 (+resume)
        if not self.running:
            self.running = True
            self.__checkpoint = self.__class__.now

    def pause(self):  # 스톱워치 일시정지 (게임 일시정지 시 사용)
        if self.running:
            self.running = False
            self.__preset += self.__class__.now - self.__checkpoint

    def reset(self, start_frame=0):
        if self.running:
            self.__preset = start_frame
            self.__checkpoint = self.__class__.now - start_frame

    def off(self):
        self.running = False
        self.__preset = 0
        self.__checkpoint = None


class Time:  # Framewatch를 객체화한 클래스.
    __font = Text('GenShinGothic-Monospace-Bold', 64, WHITE, (20, 0))
    __clock = Framewatch('TIMER')
    most = 0
    current = 0  # current frame

    @classmethod
    def update(cls):
        cls.__clock.tick()
        cls.current = cls.__clock.get_elapsed()
        cls.most = max(cls.most, cls.current)

    @classmethod
    def draw(cls, convert_frame_to_second=False, ndigits=0):
        if convert_frame_to_second:
            seconds = cls.convert(ndigits)
        else:
            seconds = cls.current  # deciseconds

        cls.__font.write(seconds)

    @classmethod
    def convert(cls, ndigits=0):
        if ndigits == 0:
            seconds = cls.current // 100  # 0초
        elif ndigits == 1:
            seconds = cls.current // 10 / 10  # 0.0초
        elif ndigits == 2:
            seconds = cls.current / 100  # 0.00초
        else:
            raise ValueError("Time.convert(ndigits=) must be integer 1/2/3")
        return seconds

    @classmethod
    def get(cls, adjust_frame=0):
        assert isinstance(adjust_frame,
                          int), "type of 'adjust_frame' param must be int."
        return cls.current + adjust_frame

    @classmethod
    def start(cls):
        cls.__clock.start()

    @classmethod
    def reset(cls, start_seconds):
        cls.current = start_seconds * 100
        cls.__clock.reset(cls.current)

    @classmethod
    def pause(cls):  # 스톱워치 일시정지 (게임 일시정지 시 사용)
        cls.__clock.pause()

    @classmethod
    def off(cls):
        cls.__clock.off()
        cls.current = 0

    @classmethod
    def go(cls, warp_seconds):
        cls.current = max(0, cls.current + warp_seconds * 100)
        cls.__clock.reset(cls.current)


def random_radian() -> float:
    while True:
        radian = random.uniform(0.0, math.pi * 2)
        if math.pi * 5 / 12 < radian < math.pi * 7 / 12 or \
                math.pi * 17 / 12 < radian < math.pi * 19 / 12:
            continue
        else:
            return radian


def item_replace_all(log, insert_item, *exception_keys):
    assert isinstance(log, dict), "type of 'log' param must be dict."
    for key in log:
        if key not in exception_keys:
            log[key] = insert_item
    return log


def tuple_cal(tuple_a: Union[list, tuple], tuple_b: Union[list, tuple],
              subtraction=False) -> tuple:
    tuple_a, tuple_b, result = list(tuple_a), list(tuple_b), []

    if len(tuple_a) > len(tuple_b):
        while len(tuple_a) == len(tuple_b):
            tuple_b.append(0)
    elif len(tuple_a) < len(tuple_b):
        while len(tuple_a) == len(tuple_b):
            tuple_a.append(0)

    if subtraction:
        for a, b in zip(tuple_a, tuple_b):
            result.append(a - b)
    else:
        for a, b in zip(tuple_a, tuple_b):
            result.append(a + b)

    return tuple(result)


def clean_subclasses(classes):
    for sub_class in classes.__subclasses__():
        sub_class.s = pg.sprite.Group()
        sub_class.group = {}


def random_denom(denominator):  # 1/denominator의 확률로 True를 뽑기.
    return random.randrange(denominator) == 1


def random_pick(*args: Union[list, tuple]):
    __list = []
    for choice, quantity in args:
        for i in range(quantity):
            __list.append(choice)
    return random.choice(__list)


# def alive(*class_s):  # self.is_alive가 True인 item들로만 그룹 재구성.
#     for obj in sum(class_s, []):
#         if obj.is_alive:
#             yield obj
#
#
# def dump(*class_s):  # self.is_alive가 False인 item들로만 그룹 재구성.
#     for obj in sum(class_s, []):
#         if obj.is_alive:
#             yield obj


def left_right(rect_a, rect_b):
    a_position = rect_a.centerx if type(rect_a) is pg.Rect else rect_a
    b_position = rect_b.centerx if type(rect_b) is pg.Rect else rect_b
    return a_position < b_position


def up_down(rect_a, rect_b):
    a_position = rect_a.centery if type(rect_a) is pg.Rect else rect_a
    b_position = rect_b.centery if type(rect_b) is pg.Rect else rect_b
    return a_position < b_position


def tl_px(*numbers):  # tile to pixel
    if type(numbers[0]) is list or type(numbers[0]) is tuple:
        result = []
        for number in numbers[0]:
            result.append(tl_px(number))
        result = tuple(result)
        if len(result) == 1:
            result = result[0]
        return result
    elif type(numbers[0]) is int or type(numbers[0]) is float:
        result = tuple([number * TILE_LENGTH for number in numbers])
        if len(result) == 1:
            result = result[0]
        return result
    else:
        raise TypeError("*numbers type must be list/tuple/int/float.")


def px_tl(*numbers):  # pixel to tile
    if type(numbers[0]) is list or type(numbers[0]) is tuple:
        result = []
        for number in numbers[0]:
            result.append(px_tl(number))
        result = tuple(result)
        if len(result) == 1:
            result = result[0]
        return result
    elif type(numbers[0]) is int or type(numbers[0]) is float:
        result = tuple([number // TILE_LENGTH for number in numbers])
        if len(result) == 1:
            result = result[0]
        return result
    else:
        raise TypeError("*numbers type must be list/tuple/int/float.")


def calculate_radian(rect_a, rect_b):
    a_position = rect_a.center if type(rect_a) is pg.Rect else rect_a
    b_position = rect_b.center if type(rect_b) is pg.Rect else rect_b
    base_length, height_length = tuple_cal(a_position, b_position, True)
    radian = math.atan2(-height_length, base_length)  # 라디안 값 각도(angle)
    return radian


def calculate_distance(rect_a, rect_b):  # 두 좌표 사이의 거리 구하기.
    if type(rect_a) is pg.Rect:
        ax, ay = rect_a.centerx, rect_a.centery
    elif type(rect_a) is tuple:
        ax, ay = rect_a

    if type(rect_b) is pg.Rect:
        bx, by = rect_b.centerx, rect_b.centery
    elif type(rect_b) is tuple:
        bx, by = rect_b

    distance = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
    return distance


def circular_relocation(radian, radius, center_of_circle):
    x = center_of_circle[0] + radius * math.cos(radian)
    y = center_of_circle[1] + radius * math.sin(radian)
    return x, y


def check_method_exists(instance, method):
    # 입력된 method 이름이 객체에 있으면 True, 아닐 경우 False를 반환.
    assert isinstance(method, str), "type of 'method' param must be str."
    return method in vars(instance.__class__)


# def get_mouse_pos(adjustive_value):  # 창 mouse 좌표를 stage 좌표로 변환.
#     x, y = pg.mouse.get_pos()
#     new_x = x + adjustive_value
#     mouse_pos = (new_x, y)
#     return mouse_pos


def append(_list, _item, tidy=False):
    """
    tidy=True: _item을 추가한 뒤, _list에 있는 모든 중복값들을 삭제.
    tidy=False: _list에 _item이 있으면 _item을 추가하지 않음. (기본값)
    """
    assert isinstance(_list, list), "type of '_list' param must be list."
    assert isinstance(tidy, bool), "type of 'tidy' param must be bool."

    if _item not in _list:
        _list.append(_item)
    if tidy:
        list(set(_list))
    return _list


def remove(_list, _item, tidy=False):
    """
    tidy=True: _list 안에 있는 모든 _item들을 삭제.
    tidy=False: _list 맨 앞에 있는 하나의 item을 삭제.
                _list.remove()와 동일하나, 찾는 item이 없어도 에러 발생 안 함.
    """
    assert isinstance(_list, list), "type of '_list' param must be list."
    assert isinstance(tidy, bool), "type of 'tidy' param must be bool."

    if tidy:
        while _item in _list:
            _list.remove(_item)
    else:
        if _item in _list:
            _list.remove(_item)
    return _list


def batch(_type, sample, logical_operator, *args):
    comparison = []

    if _type == IN:
        assert isinstance(sample, list), "type of '_list' param must be list."
        # OR: args 중 하나라도 sample(list)에 있을 경우 True.
        # AND: args 전부 sample(list)에 있을 경우 True.
        # ALL: sample(list) 전체가 args로만 채워져 있을 경우 True.

        if logical_operator == ALL:
            for _item in sample:
                comparison.append(_item in args)
            return False not in comparison
        else:
            for arg in args:
                comparison.append(arg in sample)

    else:  # if _type is bool:
        for arg in args:
            comparison.append(sample == arg)

    if logical_operator == OR:
        return True in comparison
    elif logical_operator == AND:
        return False not in comparison
    elif logical_operator == XOR:
        return True in comparison and False in comparison


# def batch_coll(my_rect, mouse_pos, *objs):
#     """하나라도 충돌이 감지되면 True를, 아닐 경우 False를 return.
#     """
#     rect = my_rect.copy()
#     rect.center = mouse_pos
#
#     for obj in sum(objs, []):
#         if rect.colliderect(obj.rect):
#             return True
#     return False


def rect_xy_copy(rect, dx=None, dy=None):
    result_rects = []
    rect_x, rect_y = rect.copy(), rect.copy()

    if dx is not None:
        rect_x.centerx += int(dx)
        result_rects.append(rect_x)
    if dy is not None:
        rect_y.centery += int(dy)
        result_rects.append(rect_y)

    if len(result_rects) == 1:
        return result_rects[0]
    else:
        return tuple(result_rects)


def set_rect(rect, xy: tuple, dx=None, dy=None, point=TOPLEFT, tile=False):
    if type(rect) is pg.Surface:
        rect = rect.get_rect()
    elif type(rect) is pg.Rect:
        rect = rect.copy()
    elif type(rect) is tuple:
        rect = Rect(rect)
    else:
        raise TypeError("*rect type must be pg.Surface/pg.Rect/tuple.")

    new_xy = tl_px(xy) if tile else xy

    if point == CENTER:
        rect.center = new_xy
    elif point == TOPLEFT:
        rect.topleft = new_xy
    elif point == TOPRIGHT:
        rect.topright = new_xy
    elif point == BOTTOMLEFT:
        rect.bottomleft = new_xy
    elif point == BOTTOMRIGHT:
        rect.bottomright = new_xy
    elif point == MIDLEFT:
        rect.midleft = new_xy
    elif point == MIDRIGHT:
        rect.midright = new_xy
    elif point == MIDTOP:
        rect.midtop = new_xy
    elif point == MIDBOTTOM:
        rect.midbottom = new_xy

    if dx is not None:
        rect.left += tl_px(dx) if tile else dx
    if dy is not None:
        rect.top += tl_px(dy) if tile else dy

    return rect


def set_hitbox(obj_rect, width=None, height=None):
    if width is None:
        width = obj_rect.w
    if height is None:
        height = obj_rect.h

    hitbox = Rect(0, 0, width, height)
    return hitbox


def get_hitbox(obj_rect, hitbox, point=CENTER):
    if point == TOPLEFT:
        hitbox.topleft = obj_rect.topleft
    elif point == CENTER:
        hitbox.center = obj_rect.center
    return hitbox
