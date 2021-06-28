""" Tools consist of methods of class """

from data.importtools import *


class Text:
    def __init__(self, fontname, size, color, xy: tuple, background=None,
                 antialias=True):
        self.size = size
        self.color = color
        self.x, self.y = xy
        self.background = background
        self.antialias = antialias
        self.fontname = fontname
        self.font = pg.font.Font(f'resources/fonts/{fontname}.ttf', size)

    def write(self, sentence, xy: tuple = (None, None)):
        text = self.font.render(
            f'{sentence}', self.antialias, self.color, self.background)

        x, y = xy
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        Screen.on.blit(text, [x, y])

    def change_size(self, size):
        self.size = size
        self.font = pg.font.Font(f'resources/{self.fontname}.ttf', size)

    def change_color(self, color):
        self.color = color

    def change_position(self, x, y):
        self.x, self.y = x, y

    def change_background(self, color):
        self.background = color

    def change_antialias(self, boolean):
        self.antialias = boolean


class Framewatch:
    """Default is 100 fps.
    """
    now = 0

    @classmethod
    def tick(cls):
        cls.now += 1

    def __init__(self, mode, min_sec=0, max_sec=0):
        if 0 < min_sec < 0.01 or 0 < max_sec < 0.01:
            raise ValueError(
                "min_sec/max_sec in Framewatch.__init__() must be large number than 0.01.max")

        self.mode = mode
        self.min_limit = int(min_sec * 100)  # use in 'ANTI-MASHING'
        self.max_limit = int(max_sec * 100)  # use in 'TIMER'

        self.running = False
        self.__preset = 0
        self.__checkpoint = None

    def check(self):  # 'TIMER' 모드에서 check를 안 하면 스톱워치가 됨.
        if self.mode == 'TIMER':
            if self.running:
                if self.max_limit == 0 or self.get_elapsed() < self.max_limit:
                    return True
                else:  # 제한 시간 초과
                    self.off()
                    print("\nTime is over!\n")
                    return False
            else:
                return False

        elif self.mode == 'ANTI-MASHING':  # 연타 방지 센서 (RestrictButtonMashing)
            elapsed = self.get_elapsed()
            if elapsed == 0:
                self.start()
                return True  # True: 연타 허용
            elif elapsed >= self.min_limit:
                self.reset()
                return True  # True: 연타 허용
            else:
                return False  # False: 연타 불허
        else:
            raise ValueError(
                "Please input mode='TIMER' or mode='ANTI-MASHING'")

    def get_elapsed(self):
        """현재까지의 스톱워치 재생 시간 취득arrange
        """
        elapsed = self.__preset
        if self.running:
            elapsed = self.__class__.now - self.__checkpoint
        return elapsed

    def start(self):  # 스톱워치 시작 (+resume)
        if not self.running:
            self.running = True
            self.__checkpoint = self.__class__.now

    def pause(self):  # 스톱워치 일시정지 (게임 일시정지 시 사용)
        if self.running:
            self.running = False
            self.__preset += self.__class__.now - self.__checkpoint

    def reset(self, start_frame=0):
        if self.running:
            self.__preset = start_frame
            self.__checkpoint = self.__class__.now - start_frame

    def off(self):
        self.running = False
        self.__preset = 0
        self.__checkpoint = None


class Time:  # Framewatch를 객체화한 클래스.
    __font = Text('GenShinGothic-Monospace-Bold', 64, WHITE, (20, 0))
    __clock = Framewatch('TIMER')
    most = 0
    current = 0  # current frame

    @classmethod
    def update(cls):
        cls.__clock.tick()
        cls.current = cls.__clock.get_elapsed()
        cls.most = max(cls.most, cls.current)

    @classmethod
    def draw(cls, convert_frame_to_second=False, ndigits=0):
        if convert_frame_to_second:
            seconds = cls.convert(ndigits)
        else:
            seconds = cls.current  # deciseconds

        cls.__font.write(seconds)

    @classmethod
    def convert(cls, ndigits=0):
        if ndigits == 0:
            seconds = cls.current // 100  # 0초
        elif ndigits == 1:
            seconds = cls.current // 10 / 10  # 0.0초
        elif ndigits == 2:
            seconds = cls.current / 100  # 0.00초
        else:
            raise ValueError("Time.convert(ndigits=) must be integer 1/2/3")
        return seconds

    @classmethod
    def get(cls, adjust_frame: int = 0):
        return cls.current + adjust_frame

    @classmethod
    def start(cls):
        cls.__clock.start()

    @classmethod
    def reset(cls, start_seconds):
        cls.current = start_seconds * 100
        cls.__clock.reset(cls.current)

    @classmethod
    def pause(cls):  # 스톱워치 일시정지 (게임 일시정지 시 사용)
        cls.__clock.pause()

    @classmethod
    def off(cls):
        cls.__clock.off()
        cls.current = 0

    @classmethod
    def go(cls, warp_seconds):
        cls.current = max(0, cls.current + warp_seconds * 100)
        cls.__clock.reset(cls.current)
