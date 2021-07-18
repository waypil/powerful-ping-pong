""" Tools consist of methods of class """

from data.clstools import *


class Font:
    def __init__(self, size: int, color: tuple, xy: tuple = (0, 0),
                 align=CENTER, bg=None, is_visible=True, font=JP_RETRO,
                 fix_text=''):
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
        append(self.drafts, draft)

    def load_draft(self):
        draft = self.drafts.pop()
        self.size, self.color, self.xy, self.align, self.bg, self.text = draft

    def draw(self):
        if self.is_visible:
            while self.drafts:
                self.load_draft()
                Screen.on.blit(*self.get_surface_and_rect())  # 화면에 출력
        self.reset_to_default()

    def get_surface_and_rect(self):
        font = pg.font.Font(f"{self.path}{self.font}.ttf", self.size)
        self.image = font.render(f'{self.text}', True, self.color, self.bg)
        self.rect = set_rect(self.image, self.xy, point=self.align)
        return self.image.copy(), self.rect.copy()

    def reset_to_default(self):
        self.size = self.default_size
        self.color = self.default_color
        self.xy = self.default_xy
        self.align = self.default_align
        self.bg = self.default_bg
        self.text = self.default_text

        if self.default_text:
            self.save_draft()
