""" Project PPP v1.0.2 """

from keyinput import *


""" [Import Order]
* main > keyinput > package > object > /data/
* /data/: clstools > functools > _bios > _constants
"""


class Game:
    @staticmethod
    def assign_class_variable_image():  # 모든 이미지 로드하기
        for subclass in get_subclasses(Obj, get_subs=False):
            setattr(subclass, 'sprite', Image(subclass.__name__))

    @staticmethod
    def assign_class_variable_copied():
        for subclass in get_subclasses(Obj, get_supers=False):  # 하위 cls들만
            setattr(subclass, 'copied', 0)

    @staticmethod
    def assign_class_variable_saves():
        for subclass in get_subclasses(Obj, get_supers=False):  # 하위 cls들만
            setattr(subclass, 'saves', {})

    def set_sprite_groups(self, init=True):
        """
        Game.__init__() 안에 self.attr_name = pg.sprite.Group() 변수들을 만들고
        그 변수들을 각 class.s에 전달, 서로 공유하도록 만듦.

        init=True: cls명에 따른 인스턴스 변수 양산, 그곳에 빈 Group() 할당.
                   첫 실행, 혹은 SYS.mode가 변경될 때(예: stage가 바뀔 때) 사용
        init=False: Group()가 담긴 기존 inst 변수를 object.py의 cls에 각각 전송
                    게임 이어하기, 저장 후 로드, 대전 이력 확인 등에 사용 예정
        """
        for subclass in [Obj, Package, Invisible, *get_subclasses(Package),
                         *get_subclasses(Obj, get_supers=False)]:
            attr_name = f'{subclass.__name__.lower()}s'  # 'Obj' → 'objs'
            if init:  # Game.objs = pg.sprite.Group()
                setattr(self, attr_name, pg.sprite.Group())
            subclass.s = getattr(self, attr_name)  # Game.objs → Obj.s

    @staticmethod
    def apply_system_keys():
        if 'esc' in Key.up:  # 게임 종료
            if SYS.mode('GAME'):
                Rival.hard_mode = False
                SYS.mode_change('TITLE')
            else:  # 'TITLE', 'END'
                pg.quit(), sys.exit()

        if 'enter' in Key.up:  # 전체화면/창모드 전환
            if SYS.mode('TITLE', 'END') and Player.saves:
                SYS.mode_change('GAME')  # ENTER 누르면 게임 시작

        if 'F11' in Key.up:  # 전체화면/창모드 전환
            Screen.update_resolution()

    def __init__(self, name):
        self.name = name
        self.font = None

    def init(self):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        self.set_sprite_groups(), Time.init(), self.create()

    def create(self):
        """객체(클래스 인스턴스)를 만드는 전용 공간. init() 안에 배치.
        """
        self.font = Text('GenShinGothic-Monospace-Bold', 40, WHITE, CENTER,
                         BLACK)

    def update(self):
        """게임 창, Obj 객체의 이동/상태 업데이트.
        """
        Keyinput.update(), self.objs.update(), Package.s.update()

    def draw(self):
        """update 결과에 따라, 배경/스프라이트를 화면에 표시.
        """
        Screen.on.fill(BLACK), self.objs.draw(Screen.on)

    @classmethod
    def time(cls):
        Time.update()  # 프레임 시간 +0.01초

        if Time.get() != 0.0:
            Time.draw(True, 1)  # 프레임 시간(소수점 1자릿수까지)을 화면에 표시

    def run(self):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        self.init()
        while SYS.mode(self.name):
            Game.apply_system_keys(), self.loop(), fps.tick(FPS)
        self.off()

    def loop(self):
        """processing_time_gauge 데코레이션 사용을 대비해 따로 분리
        """
        self.update(), self.draw(), self.time()
        pg.display.update()  # 모든 draw 명령을 화면에 반영

        SYS.mode_update()

    def off(self):
        """게임 종료 (강제 중지로 인한 버그/오류 방지)
        """
        self.set_sprite_groups()


class Title(Game):
    def __init__(self, name):
        super().__init__(name)
        self.select_player = None
        self.credits = None

    def init(self):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        super().init(), Time.off(), Game.assign_class_variable_saves()

        pg.mixer.Channel(1).stop(), pg.mixer.Channel(2).stop()
        pg.mixer.Channel(0).play(BGM.s['title'])

    def create(self):
        super().create()

        self.select_player = \
            PackSelectPlayer('select_player', tl_px(18, 9), TOPLEFT)

        self.credits = PackCredits(' CREDITS ', rc8(-8, 8), BOTTOMLEFT)

    def draw(self):
        super().draw()
        self.font[120][CYAN][rc8(0, -5.5)](GAME_TITLE_NAME)

        self.font[50][rc8(-3.5, 2.5)]("[BEST TIME]")

        if Score.best_time[EASY] == 0:
            self.font[rc8(-3.5, 4)][GRAY](f"EASY: ---.--")
        else:
            p = f"EASY: {'{:.2f}'.format(Score.best_time[EASY]).rjust(6, ' ')}"
            self.font[rc8(-3.5, 4)](p)

        if Score.best_time[HARD] == 0:
            self.font[rc8(-3.5, 5)][GRAY](f"HARD: ---.--")
        else:
            p = f"HARD: {'{:.2f}'.format(Score.best_time[HARD]).rjust(6, ' ')}"
            self.font[rc8(-3.5, 5)](p)

        if Player.saves:
            self.font[rc8(-2, -2.2)]("SELECT YOUR COLOR.  →")
            self.font[rc8(-3.5, -0.5)]("PRESS ENTER TO START GAME.")
            if self.select_player.state == LEFT:
                self.font[rc8(2.5, 1.5)]("↓ Player")
            else:
                self.font[rc8(5.5, 1.5)]("Player ↓")
        else:
            self.font[rc8(-2.5, -1)]("SELECT YOUR POSITION.  →")

    def off(self):
        super().off()
        pg.mixer.Channel(0).stop()
        pg.mixer.Channel(1).stop()
        pg.mixer.Channel(2).stop()


class Stage(Game):
    def create(self):
        super().create()
        Field('black')
        Ball('ball', SYS.rect.center, point=CENTER)
        Player(), Rival()

    def init(self):
        Time.off(), super().init(), Score.reset(), Time.start()

        if Rival.hard_mode:
            if not pg.mixer.Channel(2).get_busy():
                pg.mixer.Channel(1).stop()
                pg.mixer.Channel(2).play(BGM.s['game2'])
        else:
            if not pg.mixer.Channel(1).get_busy():
                pg.mixer.Channel(2).stop()
                pg.mixer.Channel(1).play(BGM.s['game1'])

    def update(self):
        super().update(), collision_check(self.objs), apply_dxdy(self.objs)

    def draw(self):
        super().draw(), Score.draw()

    def off(self):
        super().off(), Time.pause(), Score.save()


class End(Game):
    def create(self):
        super().create()
        Field('black')

    def init(self):
        super().init(), Score.reset(False, False)

    def draw(self):
        super().draw(), Score.draw()

        if LEFT in Score.win:
            self.font[120][CYAN][rc8(-3.5, -3.5)]("WIN")
            self.font[120][CYAN][rc8(3.5, -3.5)]("LOSE")
        elif RIGHT in Score.win:
            self.font[120][CYAN][rc8(-3.5, -3.5)]("LOSE")
            self.font[120][CYAN][rc8(3.5, -3.5)]("WIN")

        if 'Player' in Score.win:
            self.font[rc8(0, 4)]("PRESS ENTER TO CHALLENGE THE HARD MODE.")
            Rival.hard_mode = True
        elif 'Rival' in Score.win:
            self.font[rc8(0, 4)]("PRESS ENTER TO TRY AGAIN.")
            Rival.hard_mode = False


if __name__ == '__main__':
    Screen.update_resolution()  # 화면 초기 설정
    Game.assign_class_variable_image(), Game.assign_class_variable_copied()
    Sound.init(), BGM.init()

    Score.load()

    title, stage, end = Title('TITLE'), Stage('GAME'), End('END')

    while True:
        if SYS.mode('TITLE'):
            title.run()

        elif SYS.mode('GAME'):
            stage.run()

        elif SYS.mode('END'):
            end.run()
