""" Project PPP v0.1 """

import sys
from object import *


class Keyinput:
    __Lclick = Framewatch('ANTI-MASHING', min_sec=0.2)

    @classmethod
    def update(cls):
        """키 설정
        """
        cls.input_keep(pg.key.get_pressed())

        for event in pg.event.get():
            cls.input_once(event)

    @classmethod
    def input_keep(cls, key):
        """키 설정
        """
        if key[pg.K_UP] or key[pg.K_w]:
            if SYS.mode() == 'GAME':
                Player.get(RIGHT).move(UP)

        if key[pg.K_DOWN] or key[pg.K_s]:
            if SYS.mode() == 'GAME':
                Player.get(RIGHT).move(DOWN)

        if key[pg.K_LEFT] or key[pg.K_a]:
            pass

        if key[pg.K_RIGHT] or key[pg.K_d]:
            pass

        if pg.mouse.get_pressed(num_buttons=3)[0]:
            pass
        if pg.mouse.get_pressed(num_buttons=3)[1]:
            pass
        if pg.mouse.get_pressed(num_buttons=3)[2]:
            pass

    @classmethod
    def input_once(cls, event):
        """키 설정
        """
        if event.type == QUIT:  # [x]를 클릭하면 게임 종료
            pg.quit(), sys.exit()

        if event.type == KEYDOWN:
            if event.key == pg.K_F11:  # F11 누르면 전체화면/창모드 전환
                Screen.update_resolution()

            if event.key == pg.K_UP or event.key == pg.K_w:
                pass

        elif event.type == KEYUP:
            if event.key == pg.K_ESCAPE:  # ESC 누르면 게임 종료
                pg.quit(), sys.exit()

            if event.key == pg.K_RETURN:
                if SYS.mode() in ['TITLE', 'END']:
                    SYS.mode('GAME')  # ENTER 누르면 게임 시작

        elif event.type == MOUSEBUTTONUP:
            pass

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and cls.__Lclick.check():  # click Left
                pass

            elif event.button == 2:  # click Middle
                pass

            elif event.button == 3:  # click Right
                pass

            elif event.button >= 4 and event.button % 2 == 0:  # wheel UP
                pass

            elif event.button >= 5 and event.button % 2 == 1:  # wheel DOWN
                pass
