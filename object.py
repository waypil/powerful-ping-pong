""" Project PPP v0.1.1 """

import math
import random

from tools import *


class Obj(pg.sprite.Sprite):
    """모든 객체의 틀.
    """
    s = pg.sprite.Group()

    @classmethod
    def collision_check_all(cls):
        colls = pg.sprite.groupcollide(Paddle.s, Wall.s, False, False)
        for paddle, wall in colls.items():
            wall = wall[0]
            if wall.name == TOP:
                paddle.rect.top = wall.rect.bottom
            elif wall.name == BOTTOM:
                paddle.rect.bottom = wall.rect.top

        colls = pg.sprite.groupcollide(Ball.s, Paddle.s, False, False)
        for ball, paddle in colls.items():
            ball.bounce(paddle[0])

        colls = pg.sprite.groupcollide(Ball.s, Wall.s, False, False)
        for ball, wall in colls.items():
            ball.bounce(wall[0])

    @classmethod
    def apply_dxdy_all(cls):
        for name, obj in [*Paddle.group.items(), *Ball.group.items()]:
            obj.apply_dxdy()

    @classmethod
    def get(cls, name=None):
        try:
            return cls.group[name]  # 여기서 cls는 Obj가 아닌, self.__class__
        except KeyError:
            print(f"{cls.__name__}의 {name} 객체가 존재하지 않습니다.")

    def __init__(self, name):
        super().__init__()
        Obj.s.add(self), self.__class__.s.add(self)
        self.__class__.group[name] = self

        self.name = name
        self.image, self.rect = pg.Surface((0, 0)), Rect(0, 0, 0, 0)
        self.dx, self.dy, self.dxd, self.dyd = 0, 0, 0.0, 0.0

        self.move_log = {LEFT: False, RIGHT: False, UP: False, DOWN: False,
                         STOP: False}
        self.coll_log = {LEFT: False, RIGHT: False, TOP: False, BOTTOM: False}

        self.is_alive = True  # self.is_frozen = False

    def clsname(self, compare_name=''):  # class name
        if compare_name:
            if self.__class__.__name__ == compare_name:
                return True
            else:  # 부모 클래스
                return self.__class__.__bases__[0].__name__ == compare_name
        else:
            return self.__class__.__name__

    def apply_dxdy(self):
        self.dxd += self.dx - int(self.dx)
        self.dyd += self.dy - int(self.dy)
        self.dx, self.dy = int(self.dx), int(self.dy)

        self.rect.centerx += self.dx + int(self.dxd)  # 정수 부분만 적용.
        self.rect.centery += self.dy + int(self.dyd)  # 정수 부분만 적용.

        self.dxd -= int(self.dxd)  # 소수 부분만 남김 (다음 dxd와 합산)
        self.dyd -= int(self.dyd)  # 소수 부분만 남김 (다음 dyd와 합산)
        self.dx, self.dy = 0, 0

    def die(self):
        del self.__class__.group[self.name]
        self.kill()


class Background(Obj):
    s = pg.sprite.Group()
    group = {}

    def __init__(self, name):
        super().__init__(name)
        self.image = Img.s['back0']
        self.rect = set_rect(self.image, (0, 0))


class Wall(Obj):
    s = pg.sprite.Group()
    group = {}

    def __init__(self, name, xy: tuple, point):
        super().__init__(name)
        self.image = Img.s['wall']
        self.rect = set_rect(self.image, xy, point=point)


class Ball(Obj):
    s = pg.sprite.Group()
    group = {}

    def __init__(self, name, xy: tuple, point):
        super().__init__(name)
        self.image = Img.s['ball']
        self.rect = set_rect(self.image, xy, point=point)
        self.init_rect = self.rect.copy()

        self.speed = 5  # default
        self.radian = random_radian()
        self.delay = Time.get()

    def update(self):
        super().update()
        if Time.get() - self.delay > 100:
            self.move()

    def move(self):
        self.dx = math.cos(self.radian) * self.speed
        self.dy = -math.sin(self.radian) * self.speed

        if not self.rect.colliderect(Screen.rect):  # 화면 밖으로 나갈 경우
            if left_right(self.rect, Screen.rect):
                Score.plus(RIGHT)
            else:
                Score.plus(LEFT)
            self.reset()  # 초기 위치로 재배치

    def bounce(self, obj):  # 튕기기 함수.
        if not self.coll_log[obj.name]:
            if obj.clsname('Paddle'):
                if obj.move_log[UP]:
                    target_rect = rect_xy_copy(self.rect, dy=-obj.speed * 3)
                elif obj.move_log[DOWN]:
                    target_rect = rect_xy_copy(self.rect, dy=obj.speed * 3)
                else:
                    target_rect = self.rect
                self.radian = calculate_radian(target_rect, obj.rect)

            elif obj.clsname('Wall'):
                self.dy = abs(self.dy) if obj.name == TOP else -abs(self.dy)
                self.radian = math.atan2(-self.dy, self.dx)

            self.speed += 0.3
            self.coll_log[obj.name] = True
            item_replace_all(self.coll_log, False, obj.name)

    def reset(self):
        self.delay = Time.get()
        self.rect = self.init_rect.copy()
        self.speed, self.dx, self.dy, self.radian = 5, 0, 0, random_radian()
        item_replace_all(self.coll_log, False)


class Paddle(Obj):
    s = pg.sprite.Group()
    group = {}

    def __init__(self, name, xy: tuple, point):
        super().__init__(name)
        self.image = Img.s[f'paddle_{name[0]}']
        self.rect = set_rect(self.image, xy, point=point)
        self.speed = 5  # default

    def move(self, command):
        """UP, DOWN, LEFT, RIGHT
        """
        self.move_log[command] = True

        if command == UP:
            self.dy = -self.speed
        if command == DOWN:
            self.dy = self.speed

    def apply_dxdy(self):
        super().apply_dxdy()
        item_replace_all(self.move_log, False)


class Player(Paddle):
    def __init__(self, name, xy: tuple, point):
        super().__init__(name, xy, point)


class Rival(Paddle):
    hard_mode = False

    def __init__(self, name, xy: tuple, point):
        super().__init__(name, xy, point)

    def update(self):
        self.move_auto()
        super().update()

    def move_auto(self):
        if abs(self.rect.centery - Ball.get().rect.centery) <= TILE_LENGTH:
            pass
        elif up_down(self.rect, Ball.get().rect):
            if self.__class__.hard_mode:
                self.move(DOWN)
            else:
                self.move(random.choice([DOWN, STOP]))
        else:
            if self.__class__.hard_mode:
                self.move(UP)
            else:
                self.move(random.choice([UP, STOP]))


class Score:
    font_l = Text('GenShinGothic-Monospace-Bold', 60, WHITE, tl_px(8, 0))
    font_r = Text('GenShinGothic-Monospace-Bold', 60, WHITE, tl_px(23, 0))
    s = {}
    win = None
    win_score = 5

    @classmethod
    def draw(cls):
        cls.font_l.write(cls.s[LEFT]), cls.font_r.write(cls.s[RIGHT])

    @classmethod
    def plus(cls, obj_name, score=1):
        cls.s[obj_name] += score

        if cls.s[LEFT] >= cls.win_score:
            cls.win = LEFT
            SYS.mode('END')
        elif cls.s[RIGHT] >= cls.win_score:
            cls.win = RIGHT
            SYS.mode('END')

    @classmethod
    def reset(cls, reset_score=True, reset_win=True):
        if reset_score:
            cls.s = {LEFT: 0, RIGHT: 0}
        if reset_win:
            cls.win = False



