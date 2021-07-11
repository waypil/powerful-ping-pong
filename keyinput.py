""" Powerful Ping-Pong v1.0.4 """

import sys

from package import *


class Keyinput:
    @classmethod
    def update(cls):
        Mouse.pos = pg.mouse.get_pos()  # 마우스 커서 좌표 할당

        cls.input_keep(pg.key.get_pressed())

        for event in [None, *pg.event.get()]:
            cls.input_once(event)

    @classmethod
    def input_keep(cls, key):
        """모든 if를 거쳐야 하기 때문에 순서에 따른 딜레이가 존재하지 않음.
        """
        if key[pg.K_UP]:
            append(Key.keep, 'up')
        else:
            remove(Key.keep, 'up')

        if key[pg.K_DOWN]:
            append(Key.keep, 'down')
        else:
            remove(Key.keep, 'down')

        if key[pg.K_LEFT]:
            append(Key.keep, 'left')
        else:
            remove(Key.keep, 'left')

        if key[pg.K_RIGHT]:
            append(Key.keep, 'right')
        else:
            remove(Key.keep, 'right')

        if key[pg.K_a]:
            append(Key.keep, 'a')
        else:
            remove(Key.keep, 'a')

        if key[pg.K_c]:
            append(Key.keep, 'c')
        else:
            remove(Key.keep, 'c')

        if key[pg.K_d]:
            append(Key.keep, 'd')
        else:
            remove(Key.keep, 'd')

        if key[pg.K_s]:
            append(Key.keep, 's')
        else:
            remove(Key.keep, 's')

        if key[pg.K_w]:
            append(Key.keep, 'w')
        else:
            remove(Key.keep, 'w')

        if key[pg.K_x]:
            append(Key.keep, 'x')
        else:
            remove(Key.keep, 'x')

        if key[pg.K_z]:
            append(Key.keep, 'z')
        else:
            remove(Key.keep, 'z')

        if key[pg.K_1] or key[pg.K_KP1]:
            append(Key.keep, '1')
        else:
            remove(Key.keep, '1')

        if key[pg.K_2] or key[pg.K_KP2]:
            append(Key.keep, '2')
        else:
            remove(Key.keep, '2')

        if key[pg.K_3] or key[pg.K_KP3]:
            append(Key.keep, '3')
        else:
            remove(Key.keep, '3')

        if key[pg.K_RETURN] or key[pg.K_KP_ENTER]:
            append(Key.keep, 'enter')
        else:
            remove(Key.keep, 'enter')

        if key[pg.K_ESCAPE]:
            append(Key.keep, 'esc')
        else:
            remove(Key.keep, 'esc')

        if key[pg.K_F11]:
            append(Key.keep, 'F11')
        else:
            remove(Key.keep, 'F11')

    @classmethod
    def input_once(cls, event):
        """elif가 연속되기 때문에 순서에 따른 딜레이가 발생할 수 있음.
        가급적 자주 쓰는 키들을 맨 위에 배치할 것!
        """
        if event is None:
            Mouse.event, Key.down, Key.up = None, [], []

        elif event.type == KEYDOWN:
            if event.key == pg.K_UP:
                append(Key.down, 'up')
            elif event.key == pg.K_DOWN:
                append(Key.down, 'down')
            elif event.key == pg.K_LEFT:
                append(Key.down, 'left')
            elif event.key == pg.K_RIGHT:
                append(Key.down, 'right')
            elif event.key == pg.K_a:
                append(Key.down, 'a')
            elif event.key == pg.K_d:
                append(Key.down, 'd')
            elif event.key == pg.K_c:
                append(Key.down, 'c')
            elif event.key == pg.K_s:
                append(Key.down, 's')
            elif event.key == pg.K_w:
                append(Key.down, 'w')
            elif event.key == pg.K_x:
                append(Key.down, 'x')
            elif event.key == pg.K_z:
                append(Key.down, 'z')
            elif event.key in [pg.K_1, pg.K_KP1]:
                append(Key.down, '1')
            elif event.key in [pg.K_2, pg.K_KP2]:
                append(Key.down, '2')
            elif event.key in [pg.K_3, pg.K_KP3]:
                append(Key.down, '3')
            elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                append(Key.down, 'enter')
            elif event.key == pg.K_ESCAPE:
                append(Key.down, 'esc')
            elif event.key == pg.K_F11:
                append(Key.down, 'F11')

        elif event.type == KEYUP:
            if event.key == pg.K_UP:
                append(Key.up, 'up')
            elif event.key == pg.K_DOWN:
                append(Key.up, 'down')
            elif event.key == pg.K_LEFT:
                append(Key.up, 'left')
            elif event.key == pg.K_RIGHT:
                append(Key.up, 'right')
            elif event.key == pg.K_a:
                append(Key.up, 'a')
            elif event.key == pg.K_c:
                append(Key.up, 'c')
            elif event.key == pg.K_d:
                append(Key.up, 'd')
            elif event.key == pg.K_s:
                append(Key.up, 's')
            elif event.key == pg.K_w:
                append(Key.up, 'w')
            elif event.key == pg.K_x:
                append(Key.up, 'x')
            elif event.key == pg.K_z:
                append(Key.up, 'z')
            elif event.key in [pg.K_1, pg.K_KP1]:
                append(Key.up, '1')
            elif event.key in [pg.K_2, pg.K_KP2]:
                append(Key.up, '2')
            elif event.key in [pg.K_3, pg.K_KP3]:
                append(Key.up, '3')
            elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                append(Key.up, 'enter')
            elif event.key == pg.K_ESCAPE:
                append(Key.up, 'esc')
            elif event.key == pg.K_F11:
                append(Key.up, 'F11')
                
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

        elif event.type == QUIT:  # [x]를 클릭하면 게임 종료
            pg.quit(), sys.exit()
