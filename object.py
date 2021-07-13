""" Powerful Ping-Pong v1.2.0 """

import pickle

from data.clstools import *
from data.framewatch import *


class Obj(pg.sprite.Sprite):
    """모든 객체의 틀.

    [클래스 변수]
    * subclass들 중 상위 class: cls.sprite = Image()
    * subclass들 중 하위 class: cls.s = Group(), cls.copied = 0, cls.saves = {}
    """

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

        self.name, self.imgkey, subkeys = naming(self.__class__, name)

        if name is None:
            self.image = pg.Surface((0, 0))  # must be changed or don't use
        else:
            self.image = self.__class__.sprite[self.name, subkeys]

        self.rect = set_rect(self.image, xy, point=point)

        self.dx, self.dy, self.dxd, self.dyd = 0, 0, 0.0, 0.0

        self.coll = Collision()
        self.move_log = {LEFT: False, RIGHT: False, UP: False, DOWN: False,
                         STOP: False}
        # self.is_alive = True  # self.is_frozen = False

        self.save_settings_download()

    def apply_keys(self):
        pass

    def update(self):  # 자식 update()의 맨 위에 배치할 것!
        self.apply_keys(), super().update()

    def save_settings_download(self):  # 저장된 세팅이 있을 경우
        if 'saves' in self.__class__.__dict__ and self.__class__.saves:
            loaded_name = self.__class__.saves['name']
            loaded_imgkey = self.__class__.saves['imgkey']
            self.set_sprite(loaded_name, loaded_imgkey)

    def hide(self, make_sprite_invisible: bool = True):
        self.kill()
        if make_sprite_invisible:
            Invisible.s.add(self)
        else:  # if make sprite visible
            Obj.s.add(self), self.__class__.s.add(self)

    def hide_temp(self, make_sprite_invisible: bool = True):
        Obj.s.remove(self) if make_sprite_invisible else Obj.s.add(self)

    def clsname(self, compare_name='', get_super=False):  # class name
        if compare_name:
            if self.__class__.__name__ == compare_name:
                return True
            else:  # 부모 클래스
                return self.__class__.__bases__[0].__name__ == compare_name
        else:
            if get_super:  # return superclass name
                if self.__class__.__bases__[0].__name__ == 'Obj':
                    return self.__class__.__name__
                else:
                    return self.__class__.__bases__[0].__name__
            else:
                return self.__class__.__name__

    def set_sprite(self, *keywords):
        if keywords:
            indexes = {}  # [검사 파트]: 자릿수와 subkey를 저장하는 공간

            for keyword in split(keywords):
                for i, subkeys in self.__class__.sprite.subkeys.items():
                    if keyword in subkeys:  # 입력한 키워드가 유효한지 검사
                        indexes[i] = keyword  # {자릿수: 유효키워드} 저장
                    elif not keyword or keyword is None:  # keyword == ''/None
                        self.hide()

            assert indexes, f"잘못된 키워드{keywords}가 입력되었습니다."

            if 0 in indexes:  # self.name에 해당하는 subkey가 있다면
                self.name = indexes[0]

            result = []  # [출력 파트]

            for i, self_subkey in enumerate(split(self.imgkey), start=1):
                if i in indexes:  # 새 subkey를 i자릿수에 붙임
                    result.append(indexes[i])
                else:  # 기존 subkey를 그대로 i자릿수에 붙임
                    result.append(self_subkey)

            self.imgkey = '_'.join(result)

        self.image = self.__class__.sprite[self.name][self.imgkey]

    def sprite_is(self, *subkey):
        return batch(list_(subkey), AND, self.imgkey.split('_'))

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


class Text(Obj):
    def __init__(self, fontname, size, color, align=CENTER, bg=None):
        super().__init__(None, point=align)
        self.fontname = fontname
        self.fontpath = f'resources/fonts/{fontname}.ttf'

        self.default_size = self.size = size
        self.default_color = self.color = color
        self.default_bg = self.bg = bg  # BackGround

        self.align = align  # Rect/Position/Location in _constants.py
        self.xy = (0, 0)  # temp: must be changed
        self.aa = True  # Anti-Aliasing

    def __getitem__(self, argument):
        if type(argument) is int:
            self.size = argument
        elif type(argument) is tuple:
            if len(argument) == 2:  # (x, y)
                self.xy = argument
            elif len(argument) == 3:  # (r, g, b)
                self.color = argument
            else:
                raise AssertionError
        else:
            raise AssertionError
        return self

    def __call__(self, sentence):  # write (draw)
        font = pg.font.Font(self.fontpath, self.size)
        self.image = font.render(f'{sentence}', self.aa, self.color, self.bg)
        self.rect = set_rect(self.image, self.xy, point=self.align)

        if Obj.s.has(self):  # hide 상태가 아닐 경우
            Screen.on.blit(self.image, self.rect)

        self.__reset_to_default()

    def __reset_to_default(self):
        self.size = self.default_size
        self.color, self.bg = self.default_color, self.default_bg


class Field(Obj):
    def __init__(self, name):
        super().__init__(name)
        self.wall_top = Wall(TOP, tl_px(2, 0), TOPLEFT)
        self.wall_bottom = Wall(BOTTOM, tl_px(2, 16), TOPLEFT)


class Decoration(Obj):
    """"""


class Wall(Obj):
    """"""


class Ball(Obj):
    def __init__(self, name, xy: tuple, point, delay_sec):
        super().__init__(name, xy, point)
        self.init_rect = set_rect(self.image, SYS.rect.center, point=CENTER)
        self.speed = 5  # default
        self.radian = random_radian()
        self.timer = Timer(True, delay_sec, immediate_start=True)

    def update(self):
        super().update()
        if self.timer():
            self.move()

    def move(self):
        self.avoid_verticality()
        self.dx = math.cos(self.radian) * self.speed
        self.dy = -math.sin(self.radian) * self.speed

        if not self.rect.colliderect(SYS.rect):  # 화면 밖으로 나갈 경우
            if left_right(self.rect, SYS.rect):
                Score.plus(RIGHT)
            else:
                Score.plus(LEFT)
            self.reset()  # 초기 위치로 재배치

    def avoid_verticality(self):  # 각도가 너무 수직일 경우, 살짝 기울임
        north, south = math.pi * 1 / 2, math.pi * 3 / 2
        revision = 0.01  # 보정치

        if abs(self.radian - north) < revision or \
                abs(self.radian - south) < revision:
            self.radian = random.choice(
                [self.radian + revision, self.radian - revision])

    def bounce(self, obj):  # 튕기기 함수.
        if obj not in self.coll.last:
            if obj.clsname('Paddle'):
                Sound['pang'].play()
                if obj.move_log[UP]:
                    target_rect = rect_xy_copy(self.rect, dy=-obj.speed * 3)
                elif obj.move_log[DOWN]:
                    target_rect = rect_xy_copy(self.rect, dy=obj.speed * 3)
                else:
                    target_rect = self.rect
                self.radian = calculate_radian(target_rect, obj.rect)

            elif obj.clsname('Wall'):
                Sound['pong'].play()
                self.dy = abs(self.dy) if obj.name == TOP else -abs(self.dy)
                self.radian = math.atan2(-self.dy, self.dx)

            self.speed += 0.5  # 어딘가에 부딪힐 때마다 조금씩 속도 증가
            self.coll.last = [obj]

    def reset(self):  # 장외 아웃
        if len(Ball.s) >= 2:
            self.kill()
        else:
            self.timer.reset(immediate_start=True)
            self.rect = self.init_rect.copy()
            self.dx, self.dy = 0, 0
            self.speed, self.radian = 5, random_radian()
            self.coll.all_clear()

    def after_coll(self, obj):
        if obj.clsname('Paddle') or obj.clsname('Wall'):
            self.bounce(obj)
        super().after_coll(obj)


class Paddle(Obj):
    pos = {LEFT: [(tl_px(3), SYS.rect.centery), MIDLEFT],
           RIGHT: [matrix(SYS.rect.midright, tl_px(-3, 0)), MIDRIGHT]}

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
    def __init__(self):
        super().__init__('gray', (0, 0), TOPLEFT)
        xy, point = self.__class__.pos[self.__class__.saves['name']]
        self.rect = set_rect(self.image, xy, point=point)

        self.skill = {}
        self.init_skills(BoostBall, IncreaseBall, ReviveBall, WarpPaddle)

        self.control = {UP: [UP], DOWN: [DOWN],
                        'Skill1': ['z', 'q'], 'Skill2': ['x', 'w'],
                        'Skill3': ['c', 'e'], 'Skill4': ['v', 'r']
                        }

    def apply_keys(self):
        super().apply_keys()
        if batch(self.control[UP], OR, Key.keep):
            self.move(UP)
        if batch(self.control[DOWN], OR, Key.keep):
            self.move(DOWN)
        if batch(self.control['Skill1'], OR, Key.down):
            self.skill[1].button()
        if batch(self.control['Skill2'], OR, Key.down):
            self.skill[2].button()
        if batch(self.control['Skill3'], OR, Key.down):
            self.skill[3].button()
        if batch(self.control['Skill4'], OR, Key.down):
            self.skill[4].button()

    def update(self):
        super().update()

    def init_skills(self, *skill_classes):
        for i, skill_class in enumerate(skill_classes, start=1):
            if self.sprite_is(LEFT):
                self.skill[i] = skill_class(tl_px(2 + i * 2, 16), TOPLEFT)
            else:  # RIGHT
                self.skill[i] = skill_class(tl_px(18 + i * 2, 16), TOPLEFT)


class Rival(Paddle):
    def __init__(self):
        super().__init__('gray', (0, 0), TOPLEFT)
        xy, point = self.__class__.pos[self.__class__.saves['name']]
        self.rect = set_rect(self.image, xy, point=point)

    def update(self):
        self.move_auto()
        super().update()

    def move_auto(self):
        if abs(self.rect.centery - Ball.get().rect.centery) <= TILE_LENGTH:
            pass
        elif up_down(self.rect, Ball.get().rect):
            if SYS.hard_mode:
                self.move(DOWN)
            else:
                self.move(random.choice([DOWN, STOP]))
        else:
            if SYS.hard_mode:
                self.move(UP)
            else:
                self.move(random.choice([UP, STOP]))


class PaddleSample(Paddle):
    def update(self):
        super().update()
        for button_lr in ButtonSelectLR.s.sprites():
            if self.imgkey == button_lr.name:
                self.set_sprite(button_lr.imgkey.split('_')[0])  # color


class Button(Obj):
    def update(self):
        super().update()
        if bool(self.rect.collidepoint(Mouse.pos)):
            if Mouse.event == CLICK_LEFT_DOWN:
                self.sound_effect(), self.set_sprite(PUSH)

    def button(self, state):
        assert state in ['gray', 'red', 'blue', PUSH, UNPUSH]
        self.set_sprite(state)

    def sound_effect(self):
        pass


class ButtonText(Button):
    def __init__(self, sentence, xy: tuple, point):
        super().__init__(None, xy, point)
        self.xy = xy

        self.font = None
        self.size, self.color, self.align, self.bg = 0, WHITE, point, None
        self.__apply_font()

        self.sentence = sentence
        self.is_pushed = False

    def update(self):
        if bool(self.rect.collidepoint(Mouse.pos)):
            if Mouse.event == CLICK_LEFT_DOWN:
                self.is_pushed = False if self.is_pushed else True

        self.font[self.xy](self.sentence)  # write (draw)
        self.image, self.rect = self.font.image, self.font.rect

    def font_reset(self, size='', color='', align='', bg=''):
        if size:
            self.size = size
        if color:
            self.color = color
        if align:
            self.align = align
        if bg:
            self.bg = bg

        self.__apply_font()
        self.image, self.rect = self.font.image, self.font.rect

    def __apply_font(self):
        self.font = Text('GenShinGothic-Monospace-Bold',
                         self.size, self.color, self.align, self.bg)


class ButtonSelectColor(Button):
    def sound_effect(self):
        super().sound_effect()
        Sound['color'].play()


class ButtonSelectLR(Button):
    def __init__(self, name, xy: tuple, point):
        super().__init__(name, xy, point)
        red_pos = matrix(xy, tl_px(0.5, -1))
        blue_pos = matrix(red_pos, tl_px(2, 0))
        self.red = ButtonSelectColor(['color', 'red_unpush'], red_pos, TOPLEFT)
        self.blue = ButtonSelectColor(['color', 'blue_unpush'],
                                      blue_pos, TOPLEFT)
        self.red.hide(), self.blue.hide()

    def update(self):
        super().update()
        if self.sprite_is(PUSH):
            self.red.hide(False), self.blue.hide(False)
        else:  # self.sprite_is(UNPUSH)
            self.red.hide(), self.blue.hide()

        if self.red.sprite_is(PUSH):
            self.set_sprite('red')
            self.red.set_sprite(UNPUSH, ''), self.blue.set_sprite(UNPUSH)
        elif self.blue.sprite_is(PUSH):
            self.set_sprite('blue')
            self.red.set_sprite(UNPUSH), self.blue.set_sprite(UNPUSH, '')

    def sound_effect(self):
        super().sound_effect()
        Sound['button'].play()


class Skill(Obj):
    @classmethod
    def reset_buttons(cls):  # 현재 사용하지 않음
        for subclass in get_subclasses(cls, get_supers=True):
            for skill in subclass.s:
                skill.state = ON
                skill.set_sprite(ON)

    def __init__(self, xy: tuple, point):
        super().__init__(self.clsname().lower(), xy, point)
        # self.antimash = Framewatch('ANTI-MASHING', min_sec=10)
        self.state = ON  # ON, RUNNING, OFF

    def update(self):
        super().update()
        if self.state == RUNNING:
            self.invoke()

    def button(self, force_state=''):
        assert force_state in ['', ON, RUNNING, OFF]

        if force_state:
            self.state = force_state
        elif self.state == ON:
            Sound['skill'].play()
            self.state = RUNNING

        self.set_sprite(self.state)

    def invoke(self):  # 스킬 발동 (자식 class의 맨 마지막 줄에 배치할 것!)
        self.button(OFF)

    def sound_effect(self):
        pass


class BoostBall(Skill):
    def __init__(self, xy: tuple, point):
        super().__init__(xy, point)
        self.players, self.balls = Player.s, Ball.s

    def invoke(self):
        Audio.play(Sound['charge'])

        colls = pg.sprite.groupcollide(self.players, self.balls, False, False)
        if colls:
            for player, ball in colls.items():
                Audio.exchange(Sound['charge'], Sound['shoot'])
                ball[0].speed *= 5  # ball이 [*ball] 꼴로 출력되기 때문
            super().invoke()


class IncreaseBall(Skill):  # obj 증식
    def __init__(self, xy: tuple, point):
        super().__init__(xy, point)
        self.player, self.ball = None, None

    def update(self):
        self.player, self.ball = Player.get(), Ball.get()
        super().update()

    def invoke(self):
        if self.player.sprite_is(LEFT):
            invocable_area = left_right(self.ball.rect.center, SYS.rect.center)
        else:  # RIGHT
            invocable_area = left_right(SYS.rect.center, self.ball.rect.center)

        if invocable_area and self.ball.timer():
            ball2 = Ball('ball', self.ball.rect.center, CENTER, [0, 1])
            ball3 = Ball('ball', self.ball.rect.center, CENTER, [0, 1])
            ball2.speed = ball3.speed = self.ball.speed
            ball2.radian = self.ball.radian + math.pi / 6  # 시계 반대 방향
            ball3.radian = self.ball.radian - math.pi / 6  # 시계 방향
            super().invoke()
        else:  # if self.state == RUNNING:
            self.button(ON)


class ReviveBall(Skill):  # 공 부활
    def __init__(self, xy: tuple, point):
        super().__init__(xy, point)
        self.player, self.balls = None, Ball.s

    def update(self):
        self.player = Player.get()
        super().update()

    def invoke(self):  # 스킬 발동
        for ball in self.balls:
            if self.player.sprite_is(LEFT):
                if left_right(ball.rect.right, self.player.rect.left):
                    Sound['revive'].play()
                    ball.radian = 0  # 오른쪽 수직 방향
                    super().invoke()
            else:  # RIGHT
                if left_right(self.player.rect.right, ball.rect.left):
                    Sound['revive'].play()
                    ball.radian = math.pi  # 왼쪽 수직 방향
                    super().invoke()


class WarpPaddle(Skill):  # 공이 있는 높이로 Paddle 워프
    def __init__(self, xy: tuple, point):
        super().__init__(xy, point)
        self.player, self.balls = None, Ball.s

    def update(self):
        self.player = Player.get()
        super().update()

    def invoke(self):  # 스킬 발동
        distances, balls = [], []

        for ball in self.balls:
            distances.append(abs(self.player.rect.centerx - ball.rect.centerx))
            balls.append(ball)

        nearest_ball = balls[distances.index(min(distances))]
        self.player.rect.centery = nearest_ball.rect.centery
        super().invoke()


# class SpeedUpPaddle(Skill):
#     def __init__(self, xy: tuple, point):
#         super().__init__(xy, point)
#         self.player = None
#         self.is_available = True
#
#     def update(self):
#         self.player = Player.get()
#         super().update()
#
#     def invoke(self):  # 스킬 발동
#         if self.is_available:
#             self.player.speed *= 2
#             self.is_available = False
#         else:
#             pass
#             super().invoke()
#
#
# class SpeedDownPaddle(Skill):
#     def __init__(self, xy: tuple, point):
#         super().__init__(xy, point)
#         self.rival = None
#         self.is_available = True
#
#     def update(self):
#         self.rival = Rival.get()
#         super().update()
#
#     def invoke(self):  # 스킬 발동
#         if self.is_used:
#             pass
#             super().invoke()
#         else:
#             self.player.speed //= 2


class Invisible(pg.sprite.Sprite):
    """"""
    @classmethod
    def all(cls, hide=True, *exceptions):
        for obj in cls.__subgroup():
            if obj not in exceptions:
                obj.hide_temp(hide)

    @staticmethod
    def __subgroup(return_objs_list=True):
        result = pg.sprite.Group()
        for subclass in get_subclasses(Obj, get_supers=False):
            result = group(result, subclass.s)

        if return_objs_list:
            return result.sprites()
        else:
            return result


class Score:
    font = None
    win = None
    win_score = 5
    best_time = {EASY: 0, HARD: 0}

    @classmethod
    def draw(cls):
        cls.font[rc8(-3.5, -7.2)](cls.s[LEFT])
        cls.font[rc8(3.5, -7.2)](cls.s[RIGHT])

    @classmethod
    def plus(cls, obj_name, score=1):
        if Player.get().sprite_is(obj_name):
            Sound['score_up'].play()
        else:
            Sound['score_down'].play()

        cls.s[obj_name] += score
        cls.win_check(), cls.cancel_paddle_skills()

    @classmethod
    def cancel_paddle_skills(cls):
        player = Player.get()
        for i in player.skill:
            if len(Ball.s) <= 1 and player.skill[i].state == RUNNING:
                player.skill[i].button(OFF)

    @classmethod
    def win_check(cls):
        if cls.s[LEFT] >= cls.win_score:
            if Player.get().sprite_is(LEFT):
                cls.win = {'Player', LEFT}
            else:
                cls.win = {'Rival', LEFT}
        elif cls.s[RIGHT] >= cls.win_score:
            if Player.get().sprite_is(RIGHT):
                cls.win = {'Player', RIGHT}
            else:
                cls.win = {'Rival', RIGHT}

        if cls.win:
            Ball.get().remove(Obj.s)  # Obj.s.remove(Ball.get())와 동일
            SYS.mode_change('END')

    @classmethod
    def reset(cls, reset_score=True, reset_win=True):
        cls.font = Text('GenShinGothic-Monospace-Bold', 52, WHITE)

        if reset_score:
            cls.s = {LEFT: 0, RIGHT: 0}
        if reset_win:
            cls.win = False

    @classmethod
    def save(cls):
        if cls.win and 'Player' in cls.win:
            sec = SYS.playtime
            if SYS.hard_mode:
                if cls.best_time[HARD] == 0:
                    cls.best_time[HARD] = sec
                else:  # 과거 베스트 타임이 이미 존재한다면
                    cls.best_time[HARD] = min(cls.best_time[HARD], sec)
            else:
                if cls.best_time[EASY] == 0:
                    cls.best_time[EASY] = sec
                else:  # 과거 베스트 타임이 이미 존재한다면
                    cls.best_time[EASY] = min(cls.best_time[EASY], sec)

            with open('data.pickle', 'wb') as savefile:  # 파일로 저장
                pickle.dump(cls.best_time, savefile)

            SYS.playtime = None

    @classmethod
    def load(cls):
        try:
            with open("data.pickle", "rb") as savefile:  # 세이브 파일 불러오기
                cls.best_time = pickle.load(savefile)
        except Exception:   # 세이브 파일이 없을 경우
            cls.best_time = {EASY: 0, HARD: 0}
