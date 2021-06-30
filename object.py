""" Project PPP v0.2.0 """

from data.clstools import *


class Obj(pg.sprite.Sprite):
    """모든 객체의 틀.
    """
    s = None

    @classmethod
    def get(cls, name=None):
        objs = cls.s.sprites()  # cls.s는 Obj.s가 아닌, self.__class__.s
        if name is None:
            return objs[0]
        else:
            for obj in objs:
                if obj.name == name:
                    return obj
        raise KeyError(f"{cls.__name__}의 '{name}' 객체가 존재하지 않습니다. "
                       f"len({cls.__name__}.s) : {len(objs)}")

    def __init__(self, name, xy: tuple = (0, 0), point=TOPLEFT):
        super().__init__()
        Obj.s.add(self), self.__class__.s.add(self)
        self.__class__.copied += 1

        if name == self.clsname().lower():
            self.name = self.__class__.copied
        else:
            self.name = name

        self.image = self.__class__.sprite[name, '']
        self.imgkey = self.__class__.sprite.defalut_subkey
        self.rect = set_rect(self.image, xy, point=point)

        self.dx, self.dy, self.dxd, self.dyd = 0, 0, 0.0, 0.0

        self.move_log = {LEFT: False, RIGHT: False, UP: False, DOWN: False,
                         STOP: False}
        self.coll = Collision()

        self.is_alive = True  # self.is_frozen = False

    def clsname(self, compare_name=''):  # class name
        if compare_name:
            if self.__class__.__name__ == compare_name:
                return True
            else:  # 부모 클래스
                return self.__class__.__bases__[0].__name__ == compare_name
        else:
            return self.__class__.__name__

    def set_sprite(self, imgkey=None):
        if imgkey is not None:
            self.imgkey = imgkey
        self.image = self.__class__.sprite[self.name][self.imgkey]

    def after_coll(self, obj):  # 자식 after_coll의 맨 아래에 배치할 것!
        self.coll.all_add(obj)

    def apply_dxdy(self):
        self.dxd += self.dx - int(self.dx)
        self.dyd += self.dy - int(self.dy)
        self.dx, self.dy = int(self.dx), int(self.dy)

        self.rect.centerx += self.dx + int(self.dxd)  # 정수 부분만 적용.
        self.rect.centery += self.dy + int(self.dyd)  # 정수 부분만 적용.

        self.dxd -= int(self.dxd)  # 소수 부분만 남김 (다음 dxd와 합산)
        self.dyd -= int(self.dyd)  # 소수 부분만 남김 (다음 dyd와 합산)
        self.dx, self.dy = 0, 0


class Background(Obj):
    s = None
    sprite = {}
    copied = 0


class Wall(Obj):
    s = None
    sprite = {}
    copied = 0


class Ball(Obj):
    s = None
    sprite = {}
    copied = 0

    def __init__(self, name, xy: tuple, point):
        super().__init__(name, xy, point)
        self.init_rect = set_rect(self.image, SYS.rect.center, point=CENTER)
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

        if not self.rect.colliderect(SYS.rect):  # 화면 밖으로 나갈 경우
            if left_right(self.rect, SYS.rect):
                Score.plus(RIGHT)
            else:
                Score.plus(LEFT)
            self.reset()  # 초기 위치로 재배치

    def bounce(self, obj):  # 튕기기 함수.
        if obj not in self.coll.last:
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

            self.speed += 0.3  # 어딘가에 부딪힐 때마다 조금씩 속도 증가
            self.coll.last = [obj]

    def reset(self):  # 장외 아웃
        if len(Ball.s) >= 2:
            self.kill()
        else:
            self.delay = Time.get()
            self.rect = self.init_rect.copy()
            self.dx, self.dy = 0, 0
            self.speed, self.radian = 5, random_radian()
            self.coll.all_clear()

    def after_coll(self, obj):
        if obj.clsname('Paddle') or obj.clsname('Wall'):
            self.bounce(obj)
        super().after_coll(obj)


class Paddle(Obj):
    sprite = {}

    def __init__(self, name, xy: tuple, point):
        super().__init__(name, xy, point)
        self.speed = 5  # default

    def move(self, command):
        """UP, DOWN, LEFT, RIGHT
        """
        self.move_log[command] = True

        if command == UP:
            self.dy = -self.speed
        if command == DOWN:
            self.dy = self.speed

    def after_coll(self, obj):
        if obj.clsname('Wall'):
            if obj.name == TOP:
                self.rect.top = obj.rect.bottom
            elif obj.name == BOTTOM:
                self.rect.bottom = obj.rect.top
        super().after_coll(obj)

    def apply_dxdy(self):
        super().apply_dxdy()
        replace_items(self.move_log, False)


class Player(Paddle):
    s = None
    copied = 0


class Rival(Paddle):
    s = None
    copied = 0
    hard_mode = False

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


class Skill(Obj):
    s = None
    sprite = {}
    copied = 0

    def __init__(self, name, xy: tuple, point):
        super().__init__(name, xy, point)
        self.state = {PUSH: False, AVAILABLE: True}

    def update(self):
        super().update()
        if self.name == 'x' and 'unpush' in self.imgkey:
            self.on() if left_right(SYS.rect, Ball.get().rect) else self.off()

        if batch(True, ALL, self.state):
            if self.name == 'z':
                self.boost_ball(Player.s, Ball.s)
            elif self.name == 'x':
                self.triple_ball(Ball.get())
            elif self.name == 'c':
                self.revive_ball(Player.get(), Ball.get())

    def boost_ball(self, players: pg.sprite.Group, balls: pg.sprite.Group):
        if colls := pg.sprite.groupcollide(players, balls, False, False):
            for player, ball in colls.items():
                ball[0].speed *= 5  # ball이 [*ball] 꼴로 출력되기 때문
            self.off()

    def triple_ball(self, ball):
        if Time.get() - ball.delay > 100:
            ball2 = Ball('ball', ball.rect.center, CENTER)
            ball3 = Ball('ball', ball.rect.center, CENTER)
            ball2.delay = ball3.delay = Time.get(-100)
            ball2.speed = ball3.speed = ball.speed
            ball2.radian = ball.radian + math.pi / 6  # 시계 반대 방향
            ball3.radian = ball.radian - math.pi / 6  # 시계 방향
            self.off()

    def revive_ball(self, player, ball):
        if left_right(player.rect.topright, ball.rect.topleft):
            ball.radian = math.pi
            self.off()

    def push(self):
        if self.state == {PUSH: False, AVAILABLE: True}:
            replace_items(self.state, True)
            self.set_sprite('on_push')

    def on(self):
        self.state[AVAILABLE] = True
        if 'unpush' in self.imgkey:
            self.set_sprite('on_unpush')
        else:
            self.set_sprite('on_push')

    def off(self):
        self.state[AVAILABLE] = False
        if 'unpush' in self.imgkey:
            self.set_sprite('off_unpush')
        else:
            self.set_sprite('off_push')


class Score:
    font_l = Text('GenShinGothic-Monospace-Bold', 52, WHITE, tl_px(8, 0))
    font_r = Text('GenShinGothic-Monospace-Bold', 52, WHITE, tl_px(23, 0))
    win = None
    win_score = 5

    @classmethod
    def draw(cls):
        cls.font_l.write(cls.s[LEFT]), cls.font_r.write(cls.s[RIGHT])

    @classmethod
    def plus(cls, obj_name, score=1):
        cls.s[obj_name] += score
        cls.win_check()

        for skill in Skill.s.sprites():  # 이미 눌린 스킬 버튼 무효화
            if skill.state[PUSH]:
                skill.state[AVAILABLE] = False
                skill.set_sprite('off_push')

    @classmethod
    def win_check(cls):
        if cls.s[LEFT] >= cls.win_score:
            cls.win = LEFT
        elif cls.s[RIGHT] >= cls.win_score:
            cls.win = RIGHT

        if cls.win:
            Ball.get().remove(Obj.s)  # Obj.s.remove(Ball.get())와 동일
            SYS.mode_change('END')

    @classmethod
    def reset(cls, reset_score=True, reset_win=True):
        if reset_score:
            cls.s = {LEFT: 0, RIGHT: 0}
        if reset_win:
            cls.win = False
