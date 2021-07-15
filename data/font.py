""" Tools consist of methods of class """

from data.tools import *


class Text:
    s = []
    hiddens = []

    @classmethod
    def draw_all(cls):
        for text in cls.s:
            text.draw()

    @classmethod
    def hide_all(cls):
        cls.visible_all(False)

    @classmethod
    def appear_all(cls):
        cls.visible_all(True)

    @classmethod
    def visible_all(cls, make_visible: bool):
        for text in cls.hiddens if make_visible else cls.s:
            text.visible(make_visible)

    @classmethod
    def available_all(cls, make_available: bool):
        for text in Bin.fonts if make_available else cls.s:
            text.available(make_available)

    def __init__(self, size: int, color: tuple, xy: tuple = (0, 0),
                 align=CENTER, bg=None, is_visible=True, font=JP_RETRO,
                 fix_text=''):
        if self not in self.__class__.s:  # 중복 담기 방지
            self.__class__.s.append(self)

        self.drafts = []

        self.path, self.font = f"resources/fonts/", font
        self.image, self.rect = None, None

        self.default_size = self.size = size
        self.default_color = self.color = color
        self.default_xy = self.xy = xy
        self.default_align = self.align = align
        self.default_bg = self.bg = bg  # Background
        self.default_text = self.text = fix_text
        self.reset_to_default()

        self.is_visible = is_visible

    def __getitem__(self, arg):
        if type(arg) is int:
            self.size = arg
        elif type(arg) is tuple:
            if len(arg) == 2:  # (x, y)
                self.xy = rc(*arg)
            elif len(arg) == 3:  # 'CYAN' = (r, g, b)
                self.color = arg
            else:
                raise AssertionError
        elif type(arg) is list:
            if len(arg) == 1:  # [(r, g, b)]
                self.bg = arg[0]
            elif len(arg) == 2:
                arg1, arg2 = arg
                if type(arg1) in [int, float] and type(arg2) in [int, float]:
                    self.xy = rc(arg1, arg2)  # [x, y]
                elif type(arg[0]) is tuple and type(arg[0]) is tuple:
                    self.color, self.bg = arg1, arg2  # [(r, g, b), (r, g, b)]
                else:
                    raise AssertionError
            elif len(arg) == 3:  # [r, g, b]
                self.bg = tuple(arg)
            else:
                raise AssertionError
        else:
            raise AssertionError
        return self

    def __call__(self, sentence=None):
        if sentence is not None:
            self.text = sentence
            self.save_draft()
        elif self.default_text:
            self.save_draft()

    def save_draft(self):
        draft = self.size, self.color, self.xy, self.align, self.bg, self.text
        self.drafts.append(draft)

    def load_draft(self):
        draft = self.drafts.pop()
        self.size, self.color, self.xy, self.align, self.bg, self.text = draft

    def draw(self):
        if self.is_visible:
            while self.drafts:
                self.load_draft()
                Screen.on.blit(*self.get_surface_and_rect())  # 화면에 출력
        self.reset_to_default()

    def hide(self):
        self.visible(False)

    def appear(self):
        self.visible(True)

    def visible(self, make_visible: bool):
        append(Text.s, self) if make_visible else remove(Text.s, self)

    def available(self, make_available: bool):
        if make_available and self in Bin.fonts:
            remove(Bin.fonts, self), append(Text.s, self)
        elif not make_available and self in Text.s:
            remove(Text.s, self), append(Bin.fonts, self)

    def get_surface_and_rect(self):
        font = pg.font.Font(f"{self.path}{self.font}.ttf", self.size)
        self.image = font.render(f'{self.text}', True, self.color, self.bg)
        self.rect = set_rect(self.image, self.xy, point=self.align)
        return self.image, self.rect

    def reset_to_default(self):
        self.size = self.default_size
        self.color = self.default_color
        self.xy = self.default_xy
        self.align = self.default_align
        self.bg = self.default_bg
        self.text = self.default_text

        if self.default_text:
            self.save_draft()
