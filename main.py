""" Project PPP v0.1.1 """

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

    @classmethod
    def init(cls):
        """게임 엔진을 부팅. Obj 객체 생성, 객체를 해당 클래스 그룹에 추가.
        """
        Score.reset()
        Background(None)

        Wall(TOP, (0, 0), TOPLEFT)
        Wall(BOTTOM, Screen.rect.bottomleft, BOTTOMLEFT)

        Ball(None, Screen.rect.center, CENTER)

        Rival(LEFT, (tl_px(3), Screen.rect.centery), MIDLEFT)
        Player(RIGHT, tuple_cal(Screen.rect.midright, tl_px(-3, 0)), MIDRIGHT)

        Time.start()

    @classmethod
    def update(cls):
        """게임 창, Obj 객체의 이동/상태 업데이트.
        """
        Keyinput.update()
        Obj.s.update()
        Obj.collision_check_all()
        Obj.apply_dxdy_all()

    @classmethod
    def draw(cls):
        """update 결과에 따라, 배경/스프라이트를 화면에 표시.
        """
        Obj.s.draw(Screen.on)
        Score.draw()

    @classmethod
    @processing_time_gauge
    def loop(cls):
        """1루프당 processing time을 측정하기 위해 따로 분리된 영역.
        """
        cls.update(), cls.draw(), cls.time()
        pg.display.update()  # 모든 draw 명령을 화면에 반영
        SYS.mode_update()

    @classmethod
    def run(cls):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        while SYS.mode() == 'GAME':
            cls.loop()
            fps.tick(100)  # FPS 100

    @classmethod
    def off(cls):
        """게임 실행 및 구동. (게임이 돌아가는 곳)
        """
        Time.off()
        Obj.s = pg.sprite.Group()
        clean_subclasses(Obj)


if __name__ == '__main__':
    Screen.update_resolution()
    Img.load_all()

    while True:
        while SYS.mode() == 'TITLE':
            Keyinput.update()

            Screen.on.fill(BLACK)
            Game.font_big.write(GAME_TITLE_NAME)
            Game.font.write("PRESS ENTER TO START GAME.")

            pg.display.update()
            SYS.mode_update()
            fps.tick(100)

        if SYS.mode() == 'GAME':
            Game.init(), Game.run(), Game.off()

        while SYS.mode() == 'END':
            Keyinput.update()

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

            pg.display.update()
            SYS.mode_update()
            fps.tick(FPS)
