""" Powerful Ping-Pong v1.4.3 """

from keyinput import *


""" [Import Order]
* main > keyinput > package > object > /data/
* /data/: apis > framewatch/font > clstools > tools > _bios > _constants
"""


class Game:
    def set_obj_groups(self, init=True):
        """
        Game.__init__() 안에 self.attr_name = pg.sprite.Group() 변수들을 만들고
        그 변수들을 각 class.s에 전달, 서로 공유하도록 만듦.

        init=True: cls명에 따른 인스턴스 변수 양산, 그곳에 빈 Group() 할당.
                   첫 실행, 혹은 SYS.mode가 변경될 때(예: stage가 바뀔 때) 사용
        init=False: 기존 Group() 변수를 object.py의 cls에 각각 전송
                    게임 이어하기, 저장 후 로드, 대전 이력 확인 등에 사용 예정
        """
        for subclass in [Obj, Package, Bin, *get_subclasses(Package),
                         *get_subclasses(Obj, get_supers=False)]:
            attr_name = f'{subclass.__name__.lower()}s'  # 'Obj' → 'objs'
            if init:  # Game.objs = pg.sprite.Group()
                setattr(self, attr_name, pg.sprite.Group())
            subclass.s = getattr(self, attr_name)  # Game.objs → Obj.s

    def __init__(self, name):
        self.name = name

    def init(self):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        self.set_obj_groups(), self.create()

    def create(self):
        """객체(클래스 인스턴스)를 만드는 전용 공간. init() 안에 배치.
        """
        self.clock_f = Text(36, GREEN, rc(0, 14.5))

    def update(self):
        """게임 창, Obj 객체의 이동/상태 업데이트.
        """
        Keyinput.update(), Obj.s.update(), Package.s.update()

    def draw(self):
        """update 결과에 따라, 배경/스프라이트를 화면에 표시.
        """
        Screen.on.fill(BLACK), Obj.s.draw(Screen.on), Text.draw_all()

    def run(self):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        self.init()
        while SYS.running_check():
            self.loop(), fps.tick(FPS)
        self.off()

    def loop(self):
        """processing_time_gauge 데코레이션 사용을 대비해 따로 분리
        """
        self.update(), Framewatch.tick_all(), self.draw()
        pg.display.update()  # 모든 draw 명령을 화면에 반영

    def off(self):  # 반드시 하위 클래스 off()의 제일 아래에 배치할 것!
        """게임 종료 (강제 중지로 인한 버그/오류 방지)
        """
        SYS.mode_update(), self.set_obj_groups()


class Title(Game):
    def init(self):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        super().init()
        RAM.player, RAM.rival = {}, {}
        Audio.stop_all(), Audio.play(BGM['title'])

    def create(self):
        super().create()
        self.title_f = Text(120, CYAN, rc(0, -11), bg=BLACK,
                            fix_text=GAME_TITLE_NAME)
        # ↓ Packages ↓
        self.select_player = PackSelectPlayer(tl_px(18, 9), TOPLEFT)
        self.credits = PackCredits(' CREDITS ', rc(-16, 16), BOTTOMLEFT)
        self.leaderboard = PackLeaderboard(rc(-7, 5), CENTER)

    def draw(self):
        super().draw()
        self.title_f()

    def off(self):
        Audio.stop_all()
        super().off()
        

class Stage(Game):
    def create(self):
        super().create()
        self.score_l_f = Text(50, WHITE, rc(-7, -14.5))
        self.score_r_f = Text(50, WHITE, rc(7, -14.5))

        Field('black'), Ball('ball', SYS.rect.center, CENTER, 1)
        self.player, self.rival = Player(), Rival()

    def init(self):
        super().init()
        ROM().time.start()

        if self.name == STAGE_2:
            Audio.exchange(BGM.s['game1'], BGM.s['game2'])
        else:
            Audio.exchange(BGM.s['game2'], BGM.s['game1'])

    def update(self):
        super().update(), collision_check(Obj.s), apply_dxdy(Obj.s)
        self.score_l_f(ROM().score[LEFT]), self.score_r_f(ROM().score[RIGHT])

    def draw(self):
        super().draw()
        self.clock_f(ROM().time(1) if ROM().time() != 0 else '')

    def off(self):
        if 'Player' in ROM().win:
            ROM.save(self.player, self.rival)

        ROM.s[SYS.mode()] = ROMInner()
        ROM().time.off()

        super().off()


class Result(Game):
    def create(self):
        super().create()
        self.score_l_f = Text(50, WHITE, rc(-7, -14.5))
        self.score_r_f = Text(50, WHITE, rc(7, -14.5))
        self.left_f = Text(120, CYAN, rc(-7, -7))
        self.right_f = Text(120, CYAN, rc(7, -7))
        self.notice_f = Text(40, WHITE, rc(0, 8))
        Field('black')

    def draw(self):
        super().draw()
        self.clock_f(ROM.last[SYS.mode_previous()].time)
        self.score_l_f(ROM.last[SYS.mode_previous()].score[LEFT])
        self.score_r_f(ROM.last[SYS.mode_previous()].score[RIGHT])

        if LEFT in Score.win:
            self.left_f("WIN"), self.right_f("LOSE")
        elif RIGHT in Score.win:
            self.left_f("LOSE"), self.right_f("WIN")

        if 'Player' in Score.win:
            self.notice_f("PRESS ENTER TO CHALLENGE THE HARD MODE.")
        elif 'Rival' in Score.win:
            self.notice_f("PRESS ENTER TO TRY AGAIN.")


class Main:
    s = {}

    @classmethod
    def run(cls, *args):
        if __name__ == '__main__':
            cls.init(), cls.create(*args), cls.loop()

    @classmethod
    def init(cls):
        Screen.update_resolution()  # 화면 초기 설정
        ROM.init(True), RAM.init(Obj)
        Image.init(Obj), BGM.init(), Sound.init()

    @classmethod
    def create(cls, *args):
        for arg_list in args:
            game_cls, modes = arg_list[0], arg_list[1:]
            for mode in modes:
                cls.s[mode] = game_cls(mode)

    @classmethod
    def loop(cls):
        while True:
            for mode, game in cls.s.items():
                if SYS.mode(mode):
                    game.run()


Main.run(
    [Title, TITLE],
    [Result, RESULT],
    [Stage, STAGE_1, STAGE_2]
)
