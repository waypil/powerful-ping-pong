""" BIOS: Pygame 라이브러리를 초기화, 게임 화면/모드를 제어하는 곳 """

import ctypes  # 해상도 구하는 용도
import os  # 창 모드 초기 위치: 정가운데
from typing import Union  # 매개변수의 자료형 지정에 사용

import pygame as pg
from pygame.locals import *

from data._constants import *


pg.init()

fps = pg.time.Clock()


class SYS:
    __mode = 'TITLE'  # TITLE, GAME, END
    __mode_temp = None
    rect = Rect(0, 0, 1280, 720)

    hard_mode = False

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
        pg.display.set_caption(GAME_TITLE_NAME)  # 게임 창 상단 바
        pg.display.init()


class Mouse:
    event = None
    pos = (0, 0)


class Key:
    keep, down, up = [], [], []
