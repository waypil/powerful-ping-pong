""" Project PPP v0.1.4 """

import ctypes  # 해상도 구하는 용도
import os  # 창 모드 초기 위치: 정가운데

import pygame as pg
from pygame.locals import *


pg.init()

fps = pg.time.Clock()
FPS = 100

TILE_LENGTH = 40  # 타일 한 변의 길이

GAME_TITLE_NAME = "Powerful Ping-Pong"

DANGER, WARNING, CAUTION, NOTICE, SAFETY = \
    'DANGER', 'WARNING', 'CAUTION', 'NOTICE', 'SAFETY'

OR, AND, XOR, ALL = 'or', 'and', 'xor', 'all'
IN, OVER, UNDER, BETWEEN = 'in', 'over', 'under', 'between'

UP, DOWN, LEFT, RIGHT, JUMP = 'up', 'down', 'left', 'right', 'jump'
STOP, VERT, HRZN, DIAG, FREE = 'stop', 'vert', 'hrzn', 'diag', 'free'

SAVE, LOAD = 'save', 'load'

TOP, BOTTOM = 'top', 'bottom'
TOPLEFT, BOTTOMLEFT, TOPRIGHT, BOTTOMRIGHT = 'tl', 'bl', 'tr', 'br'
MIDTOP, MIDLEFT, MIDBOTTOM, MIDRIGHT = 'mt', 'ml', 'mb', 'mr'
CENTER, CENTERX, CENTERY = 'center', 'centerx', 'centery'


WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
SKYBLUE = (93, 148, 251)


class Screen:
    rect = None  # x, y값은 항상 0으로 고정해야 하며, 절대 변경하면 안 됨.
    on = None
    __is_full_screen = None

    @classmethod
    def update_resolution(cls):
        """게임 창의 해상도를 초기화/변경.
        """
        if cls.__is_full_screen is None or cls.__is_full_screen:
            cls.__is_full_screen = False
        else:
            cls.__is_full_screen = True

        if cls.__is_full_screen:
            cls._switch_full_screen()
        else:
            cls._switch_windowed_mode()

    @classmethod
    def _switch_full_screen(cls):
        u32 = ctypes.windll.user32
        cls.rect = Rect(0, 0, u32.GetSystemMetrics(0), u32.GetSystemMetrics(1))
        cls.on = pg.display.set_mode((cls.rect.w, cls.rect.h), FULLSCREEN)
        cls.__is_full_screen = True

    @classmethod
    def _switch_windowed_mode(cls):
        cls.__centering_window()
        cls.rect = Rect(0, 0, 1280, 720)
        cls.on = pg.display.set_mode((cls.rect.w, cls.rect.h))
        cls.__is_full_screen = False

    @classmethod
    def __centering_window(cls):
        pg.display.quit()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.display.set_caption(GAME_TITLE_NAME)  # 게임 타이틀
        pg.display.init()


class SYS:
    __mode = 'TITLE'  # TITLE, GAME, END
    __mode_temp = None
    rect = Rect(0, 0, 1280, 720)

    @classmethod
    def mode(cls, *modes):
        if modes:
            return cls.__mode in modes
        else:
            return cls.__mode

    @classmethod
    def mode_change(cls, mode):
        cls.__mode_temp = mode

    @classmethod
    def mode_update(cls):
        if cls.__mode_temp is not None:
            cls.__mode = cls.__mode_temp
            cls.__mode_temp = None
