""" Project PPP v0.3.2 """

from keyinput import *


"""import 순서
main > keyinput > object > /data/: clstools > functools > _bios > _constants
"""


class Game:
    font = Text('GenShinGothic-Monospace-Bold', 40, WHITE, CENTER, BLACK)

    @classmethod
    def time(cls):
        Time.update()  # 프레임 시간 +0.01초
        # Time.draw(True, 2)  # 프레임 시간을 화면에 표시

    def set_sprite_groups(self, init=True):
        """
        Game.__init__() 안에 self.attr_name = pg.sprite.Group() 변수들을 만들고
        그 변수들을 각 class.s에 전달, 서로 공유하도록 만듦.

        init=True: cls명에 따른 인스턴스 변수 양산, 그곳에 빈 Group() 할당.
                   첫 실행, 혹은 SYS.mode가 변경될 때(예: stage가 바뀔 때) 사용
        init=False: Group()가 담긴 기존 inst 변수를 object.py의 cls에 각각 전송
                    게임 이어하기, 저장 후 로드, 대전 이력 확인 등에 사용 예정
        """
        for subclass in [Obj, *get_subclasses(Obj)]:
            attr_name = f'{subclass.__name__.lower()}s'  # 'Obj' → 'objs'
            if init:  # Game.objs = pg.sprite.Group()
                setattr(self, attr_name, pg.sprite.Group())
            subclass.s = getattr(self, attr_name)  # Game.objs → Obj.s 전달
        Obj.invisibles = pg.sprite.Group()

    def __init__(self, name):
        self.name = name

    def init(self):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        self.set_sprite_groups(), self.create()

    def create(self):
        """객체(클래스 인스턴스)를 만드는 전용 공간. init() 안에 배치.
        """

    def update(self):
        """게임 창, Obj 객체의 이동/상태 업데이트.
        """
        Keyinput.update(), self.objs.update()

    def draw(self):
        """update 결과에 따라, 배경/스프라이트를 화면에 표시.
        """
        Screen.on.fill(BLACK), self.objs.draw(Screen.on)

    def run(self):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        self.init()
        while SYS.mode(self.name):
            self.loop(), fps.tick(FPS)
        self.off()

    def loop(self):
        """processing_time_gauge 데코레이션 적용을 위해 따로 분리
        """
        self.update(), self.draw(), self.time()
        pg.display.update()  # 모든 draw 명령을 화면에 반영
        SYS.mode_update()

    def off(self):
        """게임 종료 (강제 중지로 인한 버그/오류 방지)
        """
        self.set_sprite_groups(), Time.off()


class Title(Game):
    def create(self):
        super().create()
        Decoration('sample_field', tl_px(18, 9), TOPLEFT)
        ButtonSelectLR(LEFT, tl_px(19, 7), TOPLEFT)
        ButtonSelectLR(RIGHT, tl_px(25, 7), TOPLEFT)
        PaddleSample(['gray', 'left'], tl_px(19, 12), TOPLEFT)
        PaddleSample(['gray', 'right'], tl_px(29, 12), TOPRIGHT)

    def draw(self):
        super().draw()
        Game.font[120][CYAN]("Powerful Ping-Pong", rc8(0, -5))  # title
        if Player.saves:
            Game.font("PRESS ENTER TO START GAME.", rc8(-3.5, 3))
        else:
            Game.font("SELECT LEFT/RIGHT AND COLOR.", rc8(-3.5, 3))


class Stage(Game):
    def create(self):
        super().create()
        Background('black')
        Ball('ball', SYS.rect.center, point=CENTER)
        Wall(TOP, tl_px(2, 0), TOPLEFT), Wall(BOTTOM, tl_px(2, 16), TOPLEFT)
        Player(), Rival()

    def init(self):
        super().init(), Score.reset(), Time.start()

    def update(self):
        super().update(), collision_check(self.objs), apply_dxdy(self.objs)

    def draw(self):
        super().draw(), Score.draw()


class End(Game):
    def create(self):
        super().create()
        Background('black')
        Wall(TOP, tl_px(2, 0), TOPLEFT), Wall(BOTTOM, tl_px(2, 16), TOPLEFT)

    def draw(self):
        super().draw(), Score.draw()
        if LEFT in Score.win:
            Game.font[120][CYAN]("WIN", rc8(-3.5, -4))
            Game.font[120][CYAN]("LOSE", rc8(3.5, -4))
        elif RIGHT in Score.win:
            Game.font[120][CYAN]("LOSE", rc8(-3.5, -4))
            Game.font[120][CYAN]("WIN", rc8(3.5, -4))

        if 'Player' in Score.win:
            Game.font("PRESS ENTER TO CHALLENGE THE HARD MODE.", rc8(0, 4))
            Rival.hard_mode = True
        elif 'Rival' in Score.win:
            Game.font("PRESS ENTER TO TRY AGAIN.", rc8(0, 4))
            Rival.hard_mode = False


if __name__ == '__main__':
    Screen.update_resolution()  # 화면 초기 설정
    load_sprites_all(Obj, Image)  # 모든 이미지 불러오기

    title, stage, end = Title('TITLE'), Stage('GAME'), End('END')

    while True:
        if SYS.mode('TITLE'):
            title.run()

        elif SYS.mode('GAME'):
            stage.run()

        elif SYS.mode('END'):
            end.run()
