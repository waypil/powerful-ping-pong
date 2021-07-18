""" APIS """

import pickle

from data.framewatch import *
from data.font import *


class _Call(type):
    def __call__(cls, mode=None):
        mode = SYS.mode() if mode is None else mode
        return cls.s[mode]


class ROMInner:
    def __init__(self):
        self.mode = SYS.mode()
        
        self.win = ()  # (LEFT, 'Player')
        self.player_is = None
        self.time = Stopwatch()
        self.score = {LEFT: 0, RIGHT: 0}
        self.skin = {LEFT: (), RIGHT: ()}
    
    def win_check(self):
        if self.score[LEFT] >= WIN_SCORE:
            if self.player_is == LEFT:
                self.win = (LEFT, 'Player')
            else:
                self.win = (LEFT, 'Rival')
        elif self.score[RIGHT] >= WIN_SCORE:
            if self.player_is == RIGHT:
                self.win = (RIGHT, 'Player')
            else:
                self.win = (RIGHT, 'Rival')
        else:
            self.win = ()
        return self.win


class ROM(metaclass=_Call):
    best = {}
    last = {}
    s = {}

    @classmethod
    def init(cls, boot=False):
        for mode in MODES:
            cls.s[mode] = ROMInner()
            cls.best[mode] = cls.last[mode] = None

        if boot:  # 실행되는 곳이 if __name__ == '__main__' 안일 경우
            ROM.load()

    @classmethod
    def save(cls, paddle_a, paddle_b):
        mode = SYS.mode()
        
        cls().time = cls().time(2)
        cls().skin[paddle_a.imgkey] = (paddle_a.imgfile, paddle_a.imgkey)
        cls().skin[paddle_b.imgkey] = (paddle_b.imgfile, paddle_b.imgkey)

        if cls.best[mode] is None or \
                (cls().win and cls.best[mode].time > cls().time):
            cls.best[mode], cls.last[mode] = cls(), cls()
            cls._save_savefile()
        else:
            cls.last[mode] = cls()

    @classmethod
    def load(cls):
        cls._load_savefile()

    @classmethod
    def _save_savefile(cls):
        with open('save.file', 'wb') as savefile:  # 파일로 저장
            pickle.dump(cls.best, savefile)

    @classmethod
    def _load_savefile(cls):
        try:
            with open("save.file", "rb") as savefile:  # 세이브 파일 불러오기
                cls.best = pickle.load(savefile)
        except Exception:  # 세이브 파일이 없을 경우
            pass


class RAM:
    attrs = ('name', 'imgkey')

    @classmethod
    def init(cls, objs):  # Obj
        for subclass in get_subclasses(objs, get_supers=False):
            setattr(cls, subclass.__name__.lower(), {})

    @classmethod
    def save(cls, *objs):
        for obj in objs:
            if not hasattr(cls, obj.clsname().lower()):
                setattr(cls, obj.clsname().lower(), {})

            for attr in cls.attrs:
                getattr(cls, obj.clsname().lower())[attr] = getattr(obj, attr)

    @classmethod
    def load(cls, *objs):
        for obj in objs:
            try:
                args = []
                for attr in cls.attrs:
                    args.append(getattr(cls, obj.clsname().lower())[attr])
                obj.set_sprite(*args)

                if obj.clsname('Player'):
                    ROM().player_is = obj.imgkey
                # setattr(cls, obj.clsname().lower(), {})
            except KeyError:
                pass


class Score:
    font = None
    win = ()

    @classmethod
    def plus(cls, position, score=1):
        ROM().score[position] += score

        if ROM().player_is == position:
            Sound['score_up'].play()
        else:
            Sound['score_down'].play()

        cls.win = ROM().win_check()

        if cls.win:
            SYS.mode_change(RESULT)
