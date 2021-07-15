""" Powerful Ping-Pong v1.3.0 """

from keyinput import *


""" [Import Order]
* main > keyinput > package > object > /data/
* /data/: clstools/framewatch > tools > _bios > _constants
"""


class Game:
    @staticmethod
    def assign_image_in_subclass():  # 모든 이미지 로드하기
        for subclass in get_subclasses(Obj, get_subs=False):
            setattr(subclass, 'sprite', Image(subclass.__name__))

    @staticmethod
    def assign_copied_in_subclass():
        for subclass in get_subclasses(Obj, get_supers=False):  # 하위 cls들만
            setattr(subclass, 'copied', 0)

    @staticmethod
    def assign_saves_in_subclass():
        for subclass in get_subclasses(Obj, get_supers=False):  # 하위 cls들만
            setattr(subclass, 'saves', {})

    def set_obj_groups(self, init=True):
        """
        Game.__init__() 안에 self.attr_name = pg.sprite.Group() 변수들을 만들고
        그 변수들을 각 class.s에 전달, 서로 공유하도록 만듦.

        init=True: cls명에 따른 인스턴스 변수 양산, 그곳에 빈 Group() 할당.
                   첫 실행, 혹은 SYS.mode가 변경될 때(예: stage가 바뀔 때) 사용
        init=False: Group()가 담긴 기존 inst 변수를 object.py의 cls에 각각 전송
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
        self.clock = Stopwatch()
        self.clock_f = None

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
        Keyinput.update(), self.objs.update(), Package.s.update()

    def draw(self):
        """update 결과에 따라, 배경/스프라이트를 화면에 표시.
        """
        Screen.on.fill(BLACK), self.objs.draw(Screen.on), Text.draw_all()

    def time(self):
        Framewatch.tick_all()  # 프레임 시간 +0.01초
        self.clock_f(self.clock(1) if self.clock() != 0 else '')

    def run(self):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        self.init()
        while SYS.mode(self.name):
            self.loop(), fps.tick(FPS)
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
        self.set_obj_groups()


class Title(Game):
    def __init__(self, name):
        super().__init__(name)
        self.title_f = None
        # ↓ Packages ↓
        self.select_player, self.credits, self.leaderboard = None, None, None

    def init(self):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        super().init()
        SYS.playtime = None
        self.clock.off(), Game.assign_saves_in_subclass()
        Audio.stop_all(), Audio.play(BGM['title'])
        # ↓ Fonts ↓
        self.title_f.appear(), self.credits.button.f.appear()
        self.leaderboard.signboard_f.appear()

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
        super().off()
        Audio.stop_all()
        # ↓ Fonts ↓
        self.title_f.hide(), self.credits.button.f.hide()
        self.leaderboard.signboard_f.hide()
        

class Stage(Game):
    def __init__(self, name):
        super().__init__(name)
        self.left_score_f, self.right_score_f = None, None
        # ↓ Packages ↓
        self.select_player, self.credits, self.leaderboard = None, None, None

    def create(self):
        super().create()
        self.left_score_f = Text(50, WHITE, rc(-7, -14.5))
        self.right_score_f = Text(50, WHITE, rc(7, -14.5))

        Field('black'), Ball('ball', SYS.rect.center, CENTER, 1)
        Player(), Rival()

    def init(self):
        self.clock.off(), super().init(), Score.reset(), self.clock.start()

        if SYS.hard_mode:
            Audio.exchange(BGM.s['game1'], BGM.s['game2'])
        else:
            Audio.exchange(BGM.s['game2'], BGM.s['game1'])

    def update(self):
        super().update(), collision_check(self.objs), apply_dxdy(self.objs)
        if Score.win and SYS.playtime is None:
            SYS.playtime = self.clock(2)

        self.left_score_f(Score.s[LEFT]), self.right_score_f(Score.s[RIGHT])

    def off(self):
        super().off(), self.clock.pause(), Score.save()


class End(Game):
    def __init__(self, name):
        super().__init__(name)
        self.left_score_f, self.right_score_f = None, None
        self.left_f, self.right_f, self.notice_f = None, None, None

    def create(self):
        super().create()
        self.left_score_f = Text(50, WHITE, rc(-7, -14.5))
        self.right_score_f = Text(50, WHITE, rc(7, -14.5))
        self.left_f = Text(120, CYAN, rc(-7, -7))
        self.right_f = Text(120, CYAN, rc(7, -7))
        self.notice_f = Text(40, WHITE, rc(0, 8))
        Field('black')

    def init(self):
        super().init(), Score.reset(False, False)

    def draw(self):
        super().draw()
        self.clock_f(SYS.playtime)
        self.left_score_f(Score.s[LEFT]), self.right_score_f(Score.s[RIGHT])

        if LEFT in Score.win:
            self.left_f("WIN"), self.right_f("LOSE")
        elif RIGHT in Score.win:
            self.left_f("LOSE"), self.right_f("WIN")

        if 'Player' in Score.win:
            self.notice_f("PRESS ENTER TO CHALLENGE THE HARD MODE.")
            SYS.hard_mode = True
        elif 'Rival' in Score.win:
            self.notice_f("PRESS ENTER TO TRY AGAIN.")
            SYS.hard_mode = False

    def off(self):
        super().off()
        SYS.playtime = None


if __name__ == '__main__':
    Screen.update_resolution()  # 화면 초기 설정

    Game.assign_image_in_subclass(), Game.assign_copied_in_subclass()
    BGM.init(), Sound.init()

    Score.load()  # 세이브 파일 불러오기

    title, stage, end = Title('TITLE'), Stage('GAME'), End('END')

    while True:
        if SYS.mode('TITLE'):
            title.run()

        elif SYS.mode('GAME'):
            stage.run()

        elif SYS.mode('END'):
            end.run()
