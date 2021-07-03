""" Project PPP v0.3.1 """

import sys
from object import *


class Keyinput:
    __Lclick = Framewatch('ANTI-MASHING', min_sec=0.2)

    @classmethod
    def update(cls):
        """키 설정
        """
        Mouse.pos = pg.mouse.get_pos()  # 마우스 커서 좌표 할당

        cls.input_keep(pg.key.get_pressed())

        for event in [None, *pg.event.get()]:
            cls.input_once(event)

    @classmethod
    def input_keep(cls, key):
        """키 설정
        """
        if key[pg.K_UP] or key[pg.K_w]:
            if SYS.mode('GAME'):
                Player.get().move(UP)

        if key[pg.K_DOWN] or key[pg.K_s]:
            if SYS.mode('GAME'):
                Player.get().move(DOWN)

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
        if event is None:
            Mouse.event = None

        elif event.type == QUIT:  # [x]를 클릭하면 게임 종료
            pg.quit(), sys.exit()

        elif event.type == KEYDOWN:
            if event.key == pg.K_F11:  # F11 누르면 전체화면/창모드 전환
                Screen.update_resolution()

            if event.key in [pg.K_z, pg.K_KP1]:
                if SYS.mode('GAME'):
                    Player.get().skill[1].button()

            if event.key in [pg.K_x, pg.K_KP2]:
                if SYS.mode('GAME'):
                    Player.get().skill[2].button()

            if event.key in [pg.K_c, pg.K_KP3]:
                if SYS.mode('GAME'):
                    Player.get().skill[3].button()

        elif event.type == KEYUP:
            if event.key == pg.K_ESCAPE:  # ESC 누르면 게임 종료
                pg.quit(), sys.exit()

            if event.key == pg.K_RETURN:
                if SYS.mode('TITLE', 'END') and Player.saves:
                    SYS.mode_change('GAME')  # ENTER 누르면 게임 시작

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # click Left
                Mouse.event = CLICK_LEFT_DOWN

            elif event.button == 2:  # click Middle
                Mouse.event = CLICK_MIDDLE_DOWN

            elif event.button == 3:  # click Right
                Mouse.event = CLICK_RIGHT_DOWN

            elif event.button >= 4 and event.button % 2 == 0:  # wheel UP
                Mouse.event = WHEEL_UP

            elif event.button >= 5 and event.button % 2 == 1:  # wheel DOWN
                Mouse.event = WHEEL_DOWN

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:  # click Left
                Mouse.event = CLICK_LEFT_UP

            elif event.button == 2:  # click Middle
                Mouse.event = CLICK_MIDDLE_UP

            elif event.button == 3:  # click Right
                Mouse.event = CLICK_RIGHT_UP
