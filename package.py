""" Powerful Ping-Pong v1.4.3 """

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
    def __init__(self, xy: tuple, point):
        super().__init__(None)
        field_xy = xy
        btns_xy = matrix(field_xy, tl_px(+1, -2))
        pdl_lxy = matrix(field_xy, tl_px(+1, +3))
        pdl_rxy = matrix(pdl_lxy, tl_px(+10, 0))

        self.field = Decoration('sample_field', field_xy, point)
        self.button = PackButtonSelectLR(btns_xy, TOPLEFT)
        self.paddle_l = PaddleSample(['gray', 'left'], pdl_lxy, TOPLEFT)
        self.paddle_r = PaddleSample(['gray', 'right'], pdl_rxy, TOPRIGHT)

        self.f = Text(36, WHITE)

        self.state = None  # None, LEFT, RIGHT

    def update(self):
        super().update()
        self.state = self.button.check()  # 위로 전달

        if self.state == LEFT:
            RAM.player, RAM.rival = self.button.get()
        elif self.state == RIGHT:
            RAM.rival, RAM.player = self.button.get()

        if RAM.player:
            self.f[[-4, -4.5]]("SELECT YOUR COLOR.  →")
            self.f[[-7, -1]]("PRESS ENTER TO START GAME.")
            if self.state == LEFT:
                self.f[[5, 3]]("↓ Player")
            else:
                self.f[[11, 3]]("Player ↓")
        else:
            self.f[[-5, -2]]("SELECT YOUR POSITION.  →")


class PackButtonSelectLR(Package):
    def __init__(self, xy: tuple, point):
        super().__init__(None)
        l_xy = xy
        r_xy = matrix(l_xy, tl_px(+6, 0))

        self.l_ = ButtonSelectLR(LEFT, l_xy, point)
        self.r_ = ButtonSelectLR(RIGHT, r_xy, point)

        self.__state = None  # None, LEFT, RIGHT

    def check(self):
        if self.l_.sprite_is(PUSH) and self.r_.sprite_is(PUSH):
            self._unpush(self.__state)  # switching L/R

        if self.l_.sprite_is(PUSH) and self.__state in [None, RIGHT]:
            self._unpush(RIGHT)
        elif self.r_.sprite_is(PUSH) and self.__state in [None, LEFT]:
            self._unpush(LEFT)

        return self.__state
    
    def _unpush(self, direction):
        if direction == LEFT:
            self.l_.set_sprite(UNPUSH)
            self.__state = RIGHT
        elif direction == RIGHT:
            self.r_.set_sprite(UNPUSH)
            self.__state = LEFT
        else:  # if direction is None:
            raise AssertionError

    def get(self, direction=ALL):
        _left = {'name': self.l_.imgfile, 'imgkey': self.l_.imgkey}
        _right = {'name': self.r_.imgfile, 'imgkey': self.r_.imgkey}
        
        if direction == ALL:
            return _left, _right
        elif direction == LEFT:
            return _left
        elif direction == RIGHT:
            return _right
        else:  # if direction is None:
            raise AssertionError


class PackCredits(Package):
    def __init__(self, name, xy: tuple, point):
        super().__init__(name)
        self.default_sentence = name
        self.button = ButtonText(40, BLACK, xy, point, WHITE, fix_text=name)
        self.popup = Decoration('credits', SYS.rect.center, CENTER)
        self.is_on = None

    def update(self):
        super().update()
        if self.is_on is None:
            self.is_on = False
            self.popup.hide()
        elif self.button.is_pushed and not self.is_on:
            self.is_on = True
            Audio.exchange(BGM['title'], BGM['credits'])
            Obj.available_all(False, self.button), self.popup.appear()
            self.button.f("  CLOSE  ")
        elif not self.button.is_pushed and self.is_on:
            self.is_on = False
            Audio.exchange(BGM['credits'], BGM['title'])
            Obj.available_all(True, self.button), self.popup.hide()
            self.button.f.default_text = self.default_sentence


class PackLeaderboard(Package):
    def __init__(self, xy: tuple, point):
        super().__init__(None)
        signboard_xy = xy  # rc(-7, 5)
        easy_xy = matrix(signboard_xy, tl_px(0, +1.5))
        hard_xy = matrix(signboard_xy, tl_px(0, +2.5))

        self.signboard_f = Text(40, WHITE, signboard_xy, point,
                                fix_text="[BEST TIME]")
        self.easy_f = Text(40, WHITE, easy_xy, point)
        self.hard_f = Text(40, WHITE, hard_xy, point)

    def update(self):
        super().update()

        self.signboard_f()

        if ROM.best[STAGE_1] is None:
            self.easy_f[GRAY](f"STAGE 1: ---.--")
        else:
            self.easy_f(self.__get_best_time(STAGE_1))

        if ROM.best[STAGE_2] is None:
            self.hard_f[GRAY](f"STAGE 2: ---.--")
        else:
            self.hard_f(self.__get_best_time(STAGE_2))
            
    @staticmethod
    def __get_best_time(stage):  # EASY / HARD
        best_time = '{:.2f}'.format(ROM.best[stage].time).rjust(6, ' ')
        return f"{' '.join(stage.upper().split('_'))}: {best_time}"
        

