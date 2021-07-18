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
    _mode = TITLE
    _mode_temp = None
    _mode_log = ['', TITLE]

    rect = Rect(0, 0, 1280, 720)

    @classmethod
    def running_check(cls):
        return SYS._mode_temp is None or SYS._mode == SYS._mode_temp

    @classmethod
    def mode(cls, *modes):
        if modes:
            if cls._mode in modes:
                return True
            else:
                return cls._mode.split('_')[0] in modes
        else:
            return cls._mode

    @classmethod
    def mode_to_mode(cls, *modes):
        if modes:
            return cls.mode_previous(modes[0]) and cls.mode(modes[1])
        else:
            return tuple(cls._mode_log[-2:])

    @classmethod
    def mode_previous(cls, *modes):
        previous_mode = cls._mode_log[-2]
        if modes:
            if previous_mode in modes:
                return True
            else:
                return previous_mode.split('_')[0] in modes
        else:
            return previous_mode

    @classmethod
    def mode_change(cls, mode):
        cls._mode_temp = mode

    @classmethod
    def mode_update(cls):
        if cls._mode_temp is not None:
            cls._mode = cls._mode_temp
            cls._mode_log.append(cls._mode)
            cls._mode_temp = None


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


class Bin:
    s, packs, fonts = pg.sprite.Group(), pg.sprite.Group(), []
