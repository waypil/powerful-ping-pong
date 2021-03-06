""" Tools consist of single function """

import csv
import math  # Mathtools
import random  # Randomtools
from itertools import combinations  # 조합: collision_check_all()

import numpy as np  # matrix() and grayscale() in clstools.py

from data._bios import *
from data._debugtools import *


# def switch_assign(var, value1, value2):  # 스위치식(번갈아) 할당
#     variable = value1 if var != value1 else value2
#     return variable


def get_subclasses(superclass, get_supers=True, get_subs=True):
    subclass_list = []
    for sub_class in superclass.__subclasses__():
        if sub_class.__subclasses__():
            if get_supers:
                subclass_list.append(sub_class)
            if get_subs:
                subclass_list += get_subclasses(sub_class)
        else:
            subclass_list.append(sub_class)
    return subclass_list


def check_method_exists(instance, method: str):
    # 입력된 method 이름이 객체에 있으면 True, 아닐 경우 False를 반환.
    return method in vars(instance.__class__)


def load_csv(path, return_shape=True):
    csv_file = open(path, 'r', encoding='utf-8-sig')
    csv_iter = csv.reader(csv_file)
    csv_array = [row for row in map(list, zip(*csv_iter))]
    # 행열[y][x] → 열행[x][y] 변환 저장

    if return_shape:  # array_shape
        shape = (len(csv_array), len(csv_array[0]))
        return csv_array, shape
    else:
        return csv_array


#


""" Recttools: Tools for pg.Rect, pixels, hitbox """


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


def rc(x, y):  # Relative Coordinates ±n/16
    result_x = SYS.rect.w * (16 + x) / 32
    result_y = SYS.rect.h * (16 + y) / 32
    return result_x, result_y


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


#


""" Datatools: Tools for all types in python """


def list_(*args):  # 모든 item/value들을 1차원 list로 강제 변환
    """debug용 샘플: {'A': {'B': [2, {'C': 3}, 4, (5, 6, 7)], 'D': [8, 9]}}
    """
    result = []

    for arg in args:
        if type(arg) in [tuple, list, set, frozenset]:
            result = [*result, *list_(*arg)]
        elif type(arg) is dict:
            result = [*result, *list_(*arg.values())]
        else:
            result.append(arg)

    return result


def tuple_(*args):
    return tuple(list_(*args))


def set_(*args):
    return set(list_(*args))


def frozenset_(*args):
    return frozenset(list_(*args))


def batch(set_a, logical_operator: str, set_b):
    """
    * OR: set_a의 item이/item들 중 하나라도 set_b에 있을 경우 True.
    * AND: set_a의 item이/item들 모두가 set_b에 있을 경우 True.
    * ALL: set_b가 set_a의 item(들)으로만 이루어져 있을 경우 True.
    """
    assert logical_operator in [OR, AND, ALL], 'Use OR/AND/ALL only.'

    set_a, set_b = set(list_(set_a)), set(list_(set_b))

    if logical_operator == OR:
        return bool(set_a & set_b)  # 교집합
    elif logical_operator == AND:
        return bool(set_a == (set_a & set_b))  # 부분집합
    else:  # ALL
        return bool(set_a == set_b)  # 일치


def batch_bool(boolean: bool, logical_operator: str,
               samples: Union[list, tuple, dict]):
    """
    * OR: set_a의 item들 중 하나라도 set_b에 있을 경우 True.
    * AND: set_a의 item들 모두가 set_b에 있을 경우 True.
    """
    assert logical_operator in [OR, AND], 'Use OR/AND only.'

    comparison = []

    if type(samples) is dict:
        samples = samples.values()

    for sample in samples:
        comparison.append(boolean == bool(sample))

    if logical_operator == OR:
        return True in comparison
    else:  # AND
        return False not in comparison


def add(_dict: dict, *args):  # dict에 안전하게 새 key:[] 생성 및 item 추가
    if len(args) >= 3:
        key, args, value = args[0], args[1:-1], args[-1]
        if key not in _dict:  # 덮어쓰기 버그 방지
            _dict[key] = {}
        _dict[key] = add(_dict[key], *args, value)
        return _dict
    else:
        key, value = args
        try:
            if key not in _dict:
                _dict[key] = value
            elif type(_dict[key]) is not list:  # int.append(value) 버그 방지
                _dict[key] = [_dict[key], value]
            else:
                _dict[key].append(value)
            return _dict
        except TypeError:
            raise TypeError("_dict의 층 수와 args의 층 수가 일치하지 않습니다")


def append(_list: Union[list, pg.sprite.Group], _item, tidy: bool = False):
    """tidy=True: _item을 추가한 뒤, _list에 있는 모든 중복값들을 삭제.
    tidy=False: _list에 _item이 있으면 _item을 추가하지 않음. (기본값)
    """
    if type(_list) is list:
        if _item not in _list:
            _list.append(_item)
        if tidy:
            list(set(_list))
    else:  # pg.sprite.Group (여기서는 tidy를 적용하지 않음)
        while _list.has(_item):
            _list.remove(_item)
        _list.add(_item)
    return _list


def remove(_list: Union[list, pg.sprite.Group], _item, tidy: bool = False):
    """tidy=True: _list 안에 있는 모든 _item들을 삭제.
    tidy=False: _list 맨 앞에 있는 하나의 item을 삭제.
                _list.remove()와 동일하나, 찾는 item이 없어도 에러 발생 안 함.
    """
    if type(_list) is list:
        if tidy:
            while _item in _list:
                _list.remove(_item)
        else:
            if _item in _list:
                _list.remove(_item)
    else:  # pg.sprite.Group (여기서는 tidy를 적용하지 않음)
        while _list.has(_item):
            _list.remove(_item)
    return _list


def divide(remains: Union[list, tuple], *item_names: str):
    if type(remains) is tuple:
        remains = list(remains)

    match_lists = {}
    for name in item_names:
        if name in remains:
            match_lists[name] = remains.pop(remains.index(name))

    if match_lists:
        return *match_lists.values(), remains
    else:
        return [], remains


def replace_items(log: dict, insert_item, *exception_keys):
    for key in log:
        if key not in exception_keys:
            log[key] = insert_item
    return log


#


""" Mathtools: Tools for math, physics, matrix """


def matrix(*args):  # *args == data_a, sign_1, data_b, sign_2 ......
    data_a, sign, data_b = None, None, None

    def __matrix_inner(_data_a, _sign, _data_b):
        matrix_a, matrix_b = np.array(_data_a), np.array(_data_b)
        if _sign == '+':
            return matrix_a + matrix_b
        elif _sign == '-':
            return matrix_a - matrix_b
        elif _sign in ['*', '×']:
            return matrix_a * matrix_b
        elif _sign in ['/', '÷']:
            return matrix_a / matrix_b
        elif _sign == '//':  # 몫
            return matrix_a // matrix_b
        elif _sign == '%':  # 나머지
            return matrix_a % matrix_b
        else:
            raise AssertionError("use '+', '-', '*', '×', '/', '÷', '//', '%'")

    for arg in args:
        if data_a is not None and sign is not None and data_b is not None:
            data_a = __matrix_inner(data_a, sign, data_b)
            sign, data_b = None, None

        if type(arg) is str:
            sign = arg
        elif data_a is None:
            data_a = arg
        elif data_b is None:
            if sign is None:
                sign = '+'
            data_b = arg
        else:
            raise AssertionError

    return __matrix_inner(data_a, sign, data_b).tolist()  # np.array → list


def calculate_radian(rect_a, rect_b):
    a_position = rect_a.center if type(rect_a) is pg.Rect else rect_a
    b_position = rect_b.center if type(rect_b) is pg.Rect else rect_b
    base_length, height_length = matrix(a_position, '-', b_position)
    radian = math.atan2(-height_length, base_length)  # 라디안 값 각도(angle)
    return radian


def calculate_distance(rect_a: Union[pg.Rect, tuple],
                       rect_b: Union[pg.Rect, tuple]):
    ax, ay = rect_a if type(rect_a) is tuple else rect_a.center
    bx, by = rect_b if type(rect_b) is tuple else rect_b.center
    distance = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
    return distance  # 두 좌표 사이의 거리


def circular_relocation(radian, radius, center_of_circle):
    x = center_of_circle[0] + radius * math.cos(radian)
    y = center_of_circle[1] + radius * math.sin(radian)
    return x, y


#


""" Randomtools: Tools for random """


def random_radian() -> float:
    while True:
        radian = random.uniform(0.0, math.pi * 2)
        if math.pi * 5 / 12 < radian < math.pi * 7 / 12 or \
                math.pi * 17 / 12 < radian < math.pi * 19 / 12:
            continue
        else:
            return radian


def random_per(denominator):  # 1/denominator의 확률로 True를 뽑기.
    return random.randrange(denominator) == 1


def random_pick(*args: Union[list, tuple]):
    __list = []
    for choice, quantity in args:
        for i in range(quantity):
            __list.append(choice)
    return random.choice(__list)


#


""" Exclusivetools: functions for other classes """


def subobjs(obj_class):  # Only use in main.py
    result = []
    for subclass in get_subclasses(obj_class, get_supers=False):  # Obj
        result.append(subclass.s.sprites())
    return list_(result)


def collision_check(objs: pg.sprite.Group):  # Only in main.py
    for a, b in combinations(objs.sprites(), 2):  # 두 obj씩 짝 짓기
        if not batch(COLL_CHECK_EXCEPTION, OR, [a.clsname(), b.clsname()]):
            # obj의 class가 '충돌 체크 제외 대상'에 해당되지 않을 경우
            if pg.sprite.collide_rect(a, b):  # 충돌 시
                a.after_coll(b), b.after_coll(a)
            else:  # 충돌이 아닐 시
                remove(a.coll.now, b), remove(b.coll.now, a)


def apply_dxdy(objs: pg.sprite.Group):  # Only in main.py
    for obj in objs.sprites():
        obj.apply_dxdy()


def naming(cls, name=None):  # Only in Obj.__init__()
    if name is None:
        new_name, subkeys = f'{cls.__name__.lower()}', ''
        imgkey = cls.sprite.defalut_imgkey
    elif type(name) in [list, tuple]:
        new_name, subkeys = name[0], name[1:]
        imgkey = '_'.join(subkeys)
    else:  # if type(name) is str:
        new_name, subkeys = name, ''
        imgkey = cls.sprite.defalut_imgkey
    return new_name, imgkey, subkeys


def split(*strings):  # Only in Obj.set_sprite()
    result = []
    for _str in list_(strings):
        result.append(None) if _str is None else result.append(_str.split('_'))
    return list_(result)


def folder_check(path):  # Only in Image.create_sprite_dict()
    try:  # 경로(폴더)가 없을 경우, 빈 폴더를 생성
        os.makedirs(path)
    except FileExistsError:  # 이미 폴더가 있다면 그냥 무시
        pass
