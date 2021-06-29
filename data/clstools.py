""" Tools consist of methods of class """

from data.functools import *


class Collision:
    class CollisionInner:
        def __init__(self):
            self.coll_dict = {LEFT: [], RIGHT: [], TOP: [], BOTTOM: []}

        def __call__(self):  # self.coll()
            return self.coll_dict

        def __getitem__(self, key):  # self.coll[]
            return self.coll_dict[key]

        def add(self, position: str, obj=None):
            self.coll_dict[position].append(obj)

        def clear(self, *positions):
            if ALL in positions:
                item_replace_all(self.coll_dict, [])
            else:
                for position in positions:
                    self.last[position] = []

        def clear_ex(self, *positions):
            item_replace_all(self.coll_dict, [], *positions)

    def __init__(self):
        self.last = self.CollisionInner()
        self.now = self.CollisionInner()

    def add(self, position: str, obj=None):
        self.last[position].append(obj)
        self.now[position].append(obj)

    def clear(self, *positions):
        if ALL in positions:
            item_replace_all(self.last(), [])
            item_replace_all(self.now(), [])
        else:
            for position in positions:
                self.last[position] = []
                self.now[position] = []

    def clear_ex(self, *positions):
        item_replace_all(self.last(), [], *positions)
        item_replace_all(self.now(), [], *positions)


class Text:  # 편리성 개선 필요
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


class Image:
    def __init__(self, class_name: str):
        self.sprite = {}
        self.folder_name = class_name.lower()
        self.path = f"./resources/images/{self.folder_name}"
        self.defalut_subkey = ''

        self.create_sprite_dict()

    def __str__(self):
        return str(self.sprite)

    def __getitem__(self, keys):
        sprite = self.sprite

        for key in list(keys):
            if type(sprite) is dict:
                sprite = sprite[key] if key else sprite[self.defalut_subkey]

        return sprite

    def create_sprite_dict(self):
        img_names, csv_name = self.__search_file_names()

        if csv_name:
            csv_array, csv_size = load_csv(f"{self.path}/{csv_name}")
            self.__divide_sprites_process(img_names, csv_array, csv_size)
        else:
            self.__normal_sprites_process(img_names)

    def __search_file_names(self):
        for _path_, _subfolder_names_, file_names in os.walk(self.path):
            csv_name, img_names = divide(file_names, '__tile__.csv')
            return img_names, csv_name

    def __normal_sprites_process(self, img_names):
        for img_name in img_names:
            img_sprt = pg.image.load(f"{self.path}/{img_name}").convert_alpha()
            name, _extension_ = img_name.split('.')  # 이름, 확장자(png)
            self.sprite[name] = img_sprt

    def __divide_sprites_process(self, img_names, csv_array, csv_size):
        for img_name in img_names:
            img_sprt = pg.image.load(f"{self.path}/{img_name}").convert_alpha()
            img_rect = img_sprt.get_rect()
            name, _extension_ = img_name.split('.')  # 이름, 확장자(png)

            w, h = img_rect.w // csv_size[0], img_rect.h // csv_size[1]

            for tile_x in range(csv_size[0]):
                for tile_y in range(csv_size[1]):
                    x = tile_x * w
                    y = tile_y * h

                    code = csv_array[tile_x][tile_y]
                    if code.startswith('_'):  # '_abc' → 'abc'
                        code = self.defalut_subkey = code[1:]

                    if name not in self.sprite:
                        self.sprite[name] = {}

                    self.sprite[name][code] = img_sprt.subsurface((x, y, w, h))
