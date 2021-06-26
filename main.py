""" Project PPP v0.1.2 """

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

    def update(self):
        """게임 창, Obj 객체의 이동/상태 업데이트.
        버그 방지를 위하여 순서를 바꾸지 말 것.
        또한 dump check all과 revive check all은 합치지 말 것.
        """
        Keyinput.update()
        Obj.s.update()

    def draw(self):
        """update 결과에 따라, 배경/스프라이트를 화면에 표시.
        """
        Screen.on.fill(BLACK)
        Obj.s.draw(Screen.on)

    def run(self):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        self.init()

        while SYS.mode() == self.name:
            self.loop()
            fps.tick(FPS)

        self.off()

    @processing_time_gauge
    def loop(self):
        self.update(), self.draw(), self.time()
        pg.display.update()  # 모든 draw 명령을 화면에 반영
        SYS.mode_update()

    def off(self):
        """게임 종료 (강제 중지로 인한 버그/오류 방지)
        """
        # SYS.mode_is_changed = False
        Time.off()
        Obj.s = pg.sprite.Group()
        clean_subclasses(Obj)


class Stage(Game):
    def init(self):
        super().init()
        Score.reset()

        Background(None)
        Wall(TOP, (0, 0), TOPLEFT)
        Wall(BOTTOM, SYS.rect.bottomleft, BOTTOMLEFT)

        Ball(None, SYS.rect.center, CENTER)

        Rival(LEFT, (tl_px(3), SYS.rect.centery), MIDLEFT)
        Player(RIGHT, tuple_cal(SYS.rect.midright, tl_px(-3, 0)), MIDRIGHT)

        Time.start()

    def update(self):
        super().update()
        Obj.collision_check_all()
        Obj.apply_dxdy_all()

    def draw(self):
        super().draw()
        Score.draw()


class Title(Game):
    def draw(self):
        super().draw()
        Game.font_big.write(GAME_TITLE_NAME)
        Game.font.write("PRESS ENTER TO START GAME.")


class End(Game):
    def __init__(self, name):
        super().__init__(name)

    def init(self):
        super().init()
        Background(None)
        Wall(TOP, (0, 0), TOPLEFT)
        Wall(BOTTOM, SYS.rect.bottomleft, BOTTOMLEFT)

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

