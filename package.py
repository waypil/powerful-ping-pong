""" Project PPP v0.4.0 """

from object import *


class Package(pg.sprite.Sprite):
    """모든 패키지의 틀.
    superclass, subclass 모두 cls.s = pg.sprite.Group() 존재
    """
    def __init__(self, name):
        super().__init__()
        Package.s.add(self), self.__class__.s.add(self)
        self.name = name


class PackSelectPlayer(Package):
    def __init__(self, name, xy: tuple, point):
        super().__init__(name)
        field_xy = xy
        btns_xy = matrix(field_xy, tl_px(1, -2))
        pdl_lxy = matrix(field_xy, tl_px(1, 3))
        pdl_rxy = matrix(pdl_lxy, tl_px(10, 0))

        self.field = Decoration('sample_field', field_xy, point)
        self.button = PackButtonSelectLR(LEFT, btns_xy, TOPLEFT)
        self.paddle_l = PaddleSample(['gray', 'left'], pdl_lxy, TOPLEFT)
        self.paddle_r = PaddleSample(['gray', 'right'], pdl_rxy, TOPRIGHT)

        self.state = None  # None, LEFT, RIGHT

    def update(self):
        super().update()
        self.state = self.button.check()  # 위로 전달

        if self.state == LEFT:
            Player.saves, Rival.saves = self.button.get()
        elif self.state == RIGHT:
            Rival.saves, Player.saves = self.button.get()


class PackButtonSelectLR(Package):
    def __init__(self, name, xy: tuple, point):
        super().__init__(name)
        l_xy = xy
        r_xy = matrix(l_xy, tl_px(6, 0))
        self.l = ButtonSelectLR(LEFT, l_xy, point)
        self.r = ButtonSelectLR(RIGHT, r_xy, point)

        self.__state = None  # None, LEFT, RIGHT

    def check(self):
        if self.l.sprite_is(PUSH) and self.r.sprite_is(PUSH):
            self._unpush(self.__state)  # switching L/R

        if self.l.sprite_is(PUSH) and self.__state in [None, RIGHT]:
            self._unpush(RIGHT)
        elif self.r.sprite_is(PUSH) and self.__state in [None, LEFT]:
            self._unpush(LEFT)

        return self.__state

    def _unpush(self, direction):
        if direction == LEFT:
            self.l.set_sprite(UNPUSH)
            self.__state = RIGHT
        elif direction == RIGHT:
            self.r.set_sprite(UNPUSH)
            self.__state = LEFT
        else:  # if direction is None:
            raise AssertionError

    def get(self, direction=ALL):
        _left = {'name': self.l.name, 'imgkey': self.l.imgkey}
        _right = {'name': self.r.name, 'imgkey': self.r.imgkey}
        
        if direction == ALL:
            return _left, _right
        elif direction == LEFT:
            return _left
        elif direction == RIGHT:
            return _right
        else:  # if direction is None:
            raise AssertionError
