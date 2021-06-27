""" Project PPP v0.1.2.2 """

from keyinput import *

"""main > keyinput > object > tools > _base 순으로 import
"""


class Game:
    font_big = Text('GenShinGothic-Monospace-Bold', 120, CYAN, tl_px(2.5, 4),
                    BLACK)
    font = Text('GenShinGothic-Monospace-Bold', 40, WHITE, tl_px(9.5, 13),
                BLACK)

    @classmethod
    def time(cls):
        Time.update()  # 프레임 시간 +0.01초
        # Time.draw(True, 2)  # 프레임 시간을 화면에 표시

    def __init__(self, name):
        self.name = name

    def init(self):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        self.set_attrs(), self.create()

    def create(self):
        """객체(클래스 인스턴스)를 만드는 전용 공간. init() 안에 배치.
        """

    def update(self):
        """게임 창, Obj 객체의 이동/상태 업데이트.
        """
        Keyinput.update()
        self.objs.update()

    def draw(self):
        """update 결과에 따라, 배경/스프라이트를 화면에 표시.
        """
        Screen.on.fill(BLACK)
        self.objs.draw(Screen.on)

    def run(self):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        self.init()

        while SYS.mode() == self.name:
            self.loop()
            fps.tick(FPS)

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
        Time.off()

    def set_attrs(self, init=True):
        """
        init=True: cls명에 따른 인스턴스 변수 양산, 그곳에 빈 Group() 할당.
                   첫 실행, 혹은 SYS.mode가 변경될 때(예: stage가 바뀔 때) 사용
        init=False: Group()가 담긴 기존 inst 변수를 object.py의 cls에 각각 전송
                    게임 이어하기, 저장 후 로드, 대전 이력 확인 등에 사용 예정
        """
        for subclass in [Obj, *get_subclasses(Obj)]:  # self.{sub_objs}
            attr_name = f'{subclass.__name__.lower()}s'
            if init:
                setattr(self, attr_name, pg.sprite.Group())
            subclass.s = getattr(self, attr_name)


class Stage(Game):
    def create(self):
        super().create()
        Background(None)

        Wall(TOP, tl_px(2, 0), TOPLEFT)
        Wall(BOTTOM, tl_px(2, 18), BOTTOMLEFT)

        Ball(None, SYS.rect.center, CENTER)

        Player(RIGHT, tuple_cal(SYS.rect.midright, tl_px(-3, 0)), MIDRIGHT)
        Rival(LEFT, (tl_px(3), SYS.rect.centery), MIDLEFT)

    def init(self):
        super().init()
        Score.reset()
        Time.start()

    def update(self):
        super().update()
        self.collision_check_all()
        self.apply_dxdy_all()

    def draw(self):
        super().draw()
        Score.draw()

    def collision_check_all(self):
        collision_check(
            [group(self.players, self.rivals), group(self.balls, self.walls)],
            [self.balls, self.walls]
        )

    def apply_dxdy_all(self):
        for obj in self.objs.sprites():
            obj.apply_dxdy()


class Title(Game):
    def draw(self):
        super().draw()
        Game.font_big.write(GAME_TITLE_NAME)
        Game.font.write("PRESS ENTER TO START GAME.")


class End(Game):
    def create(self):
        super().create()
        Background(None)
        Wall(TOP, tl_px(2, 0), TOPLEFT)
        Wall(BOTTOM, tl_px(2, 18), BOTTOMLEFT)

    def draw(self):
        super().draw()
        Score.draw()

        if Score.win == LEFT:
            Game.font_big.write("WIN", tl_px(6.5, 4))
            Game.font_big.write("LOSE", tl_px(20, 4))
            Game.font.write("PRESS ENTER TO TRY AGAIN.", tl_px(10, 13))
            Rival.hard_mode = False
        elif Score.win == RIGHT:
            Game.font_big.write("LOSE", tl_px(6, 4))
            Game.font_big.write("WIN", tl_px(20.5, 4))
            Game.font.write("PRESS ENTER TO CHALLENGE THE HARD MODE.",
                            tl_px(6, 13))
            Rival.hard_mode = True
        else:
            raise AssertionError


if __name__ == '__main__':
    Screen.update_resolution()  # 화면 초기 설정
    Img.load_all()  # 모든 이미지 불러오기

    title, stage, end = Title('TITLE'), Stage('GAME'), End('END')

    while True:
        if SYS.mode() == 'TITLE':
            title.run()

        elif SYS.mode() == 'GAME':
            stage.run()

        elif SYS.mode() == 'END':
            end.run()
