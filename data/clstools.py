""" Tools consist of methods of class """

from itertools import product  # 중복순열

from data.tools import *


class Collision:
    def __init__(self):
        self.last, self.now = [], []
        self.timer = MashingTimer(False, 1)

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

    @classmethod
    def init(cls, objs):  # 모든 이미지 로드하기
        for subclass in get_subclasses(objs, get_subs=False):
            setattr(subclass, 'sprite', cls(subclass.__name__))

    def create_sprite_dict(self):
        folder_check(self.path)
        imgfile_names, csv_name = self._search_files()

        if csv_name:
            csv_array, csv_size = load_csv(f"{self.path}/{csv_name}")
            self._divide_sprites(imgfile_names, csv_array, csv_size)
        else:  # Normal mode (No divide)
            for imgfile_png in imgfile_names:
                sprt, _, imgfile = self._get_sprite_rect_imgfile(imgfile_png)
                self.sprite[imgfile] = sprt

    def _search_files(self):
        for _path_, _subfolder_names_, file_names in os.walk(self.path):
            csv_name, img_names = divide(file_names, '__tile__.csv')
            return img_names, csv_name
        
    def _get_sprite_rect_imgfile(self, imgfile_png):
        sprt = pg.image.load(f"{self.path}/{imgfile_png}").convert_alpha()
        rect = sprt.get_rect()
        imgfile, _ = imgfile_png.split('.')  # 파일 이름, 확장자(png)
        self._save_imgfile_name(imgfile)
        return sprt, rect, imgfile

    def _divide_sprites(self, imgfile_names, csv_array, csv_size):
        for imgfile_png in imgfile_names:
            sprt, rect, imgfile = self._get_sprite_rect_imgfile(imgfile_png)
            w, h = rect.w // csv_size[0], rect.h // csv_size[1]

            for tx, ty in product(range(csv_size[0]), range(csv_size[1])):
                x, y = tx * w, ty * h  # tx: tile_x, ty: tile_y

                code = csv_array[tx][ty]  # '_foo_bar'

                if code.startswith('_'):  # '_abc' → 'abc'
                    code = self.defalut_imgkey = code[1:]

                if '|grayscale|' in code:  # '|grayscale|abc'
                    code, sprt = code.split('|')[-1], self.grayscale(sprt)

                self.__save_subkeys(code)
                add(self.sprite, imgfile, code, sprt.subsurface((x, y, w, h)))

    def _save_imgfile_name(self, name: str):
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
        for sound_name in cls._search_files():
            sound = pg.mixer.Sound(f"{cls.path}/{sound_name}")
            name, _extension_ = sound_name.split('.')  # 이름, 확장자(wav)
            cls.s[name] = sound

    @classmethod
    def _search_files(cls):
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
