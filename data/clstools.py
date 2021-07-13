""" Tools consist of methods of class """

from data.tools import *


class Collision:
    def __init__(self):
        self.last, self.now = [], []

    def all_add(self, obj):
        append(self.last, obj), append(self.now, obj)

    def all_in(self, obj):
        return obj in self.coll.last and obj in self.coll.now

    def all_clear(self):
        self.last, self.now = [], []


class Image:
    def __init__(self, class_name: str):
        self.sprite = {}
        self.folder_name = class_name.lower()
        self.path = f"./resources/images/{self.folder_name}"

        self.names = []
        self.subkeys = {}
        self.defalut_imgkey = ''

        self.create_sprite_dict()

    def __str__(self):
        return str(self.sprite)

    def __getitem__(self, keys):
        sprite = self.sprite
        for key in list_(keys):
            if type(sprite) is dict:
                sprite = sprite[key] if key else sprite[self.defalut_imgkey]
        return sprite

    def create_sprite_dict(self):
        try:
            img_names, csv_name = self.__search_file_names()
        except:
            os.makedirs(self.path)
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
            self.__save_filename(name)
            self.sprite[name] = img_sprt

    def __divide_sprites_process(self, img_names, csv_array, csv_size):
        for img_name in img_names:
            img_sprt = pg.image.load(f"{self.path}/{img_name}").convert_alpha()
            img_rect = img_sprt.get_rect()
            name, _extension_ = img_name.split('.')  # 이름, 확장자(png)
            self.__save_filename(name)

            w, h = img_rect.w // csv_size[0], img_rect.h // csv_size[1]

            for tile_x in range(csv_size[0]):
                for tile_y in range(csv_size[1]):
                    x, y = tile_x * w, tile_y * h

                    code = csv_array[tile_x][tile_y]
                    if code.startswith('_'):  # '_abc' → 'abc'
                        code = self.defalut_imgkey = code[1:]
                    if '|grayscale|' in code:  # '|grayscale|abc'
                        code = code.split('|')[-1]
                        img_sprt = self.grayscale(img_sprt)
                    self.__save_subkeys(code)

                    if name not in self.sprite:  # 덮어쓰기 버그 방지
                        self.sprite[name] = {}

                    self.sprite[name][code] = img_sprt.subsurface((x, y, w, h))

    def __save_filename(self, name: str):
        if 0 not in self.subkeys:  # 덮어쓰기 버그 방지
            self.subkeys[0] = []
        append(self.subkeys[0], name)

    def __save_subkeys(self, code: str):
        for i, subkey in enumerate(code.split('_'), start=1):
            if i not in self.subkeys:  # 덮어쓰기 버그 방지
                self.subkeys[i] = []
            append(self.subkeys[i], subkey)

    @staticmethod
    def grayscale(image):  # https://stackoverflow.com/a/10693616/15618166
        arr = pg.surfarray.array3d(image)
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for r, g, b in col]
                for col in arr]
        arr = np.array([[[avg, avg, avg] for avg in col] for col in avgs])
        return pg.surfarray.make_surface(arr)


class Audio:
    @classmethod
    def play(cls, audio, force_loop: bool = None):
        if force_loop is None:
            loop = -1 if audio.__class__.__name__ == 'BGM' else 0
        else:
            loop = -1 if force_loop else 0

        if not cls.playing_check(audio):
            for i in range(pg.mixer.get_num_channels() + 1):
                if pg.mixer.Channel(i).get_sound() is None:
                    pg.mixer.Channel(i).play(audio, loops=loop)
                    break

    @classmethod
    def playing_check(cls, audio):
        for i in range(pg.mixer.get_num_channels()):
            if pg.mixer.Channel(i).get_sound() == audio:
                return True
        return False

    @classmethod
    def exchange(cls, audio_a, audio_b, force_loop: bool = None):
        if force_loop is None:
            loop = -1 if audio_b.__class__.__name__ == 'BGM' else 0
        else:
            loop = -1 if force_loop else 0

        for i in range(pg.mixer.get_num_channels()):
            if pg.mixer.Channel(i).get_sound() == audio_a:
                pg.mixer.Channel(i).stop()
                pg.mixer.Channel(i).play(audio_b, loops=loop)
                break
        else:
            cls.play(audio_b, force_loop)

    @classmethod
    def stop(cls, audio):
        for i in range(pg.mixer.get_num_channels()):
            if pg.mixer.Channel(i).get_sound() == audio:
                pg.mixer.Channel(i).stop()
                break

    @classmethod
    def stop_all(cls):
        for i in range(pg.mixer.get_num_channels()):
            pg.mixer.Channel(i).stop()


class Load:  # only use in Sound & BGM class
    @classmethod
    def init(cls):  # create_sound_dict
        for sound_name in cls.__search_file_names():
            sound = pg.mixer.Sound(f"{cls.path}/{sound_name}")
            name, _extension_ = sound_name.split('.')  # 이름, 확장자(wav)
            cls.s[name] = sound

    @classmethod
    def __search_file_names(cls):
        for _path_, _subfolder_names_, file_names in os.walk(cls.path):
            return file_names


class GetItem(type):
    def __getitem__(cls, name):
        return cls.s[name]


class BGM(Load, metaclass=GetItem):
    path = f"./resources/{__qualname__.lower()}s"
    s = {}


class Sound(Load, metaclass=GetItem):
    path = f"./resources/{__qualname__.lower()}s"
    s = {}
