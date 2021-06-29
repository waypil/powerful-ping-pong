""" Tools for import files/resources"""

import csv
import os

from data.functools import *


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


def load_csv(path, return_shape=True):
    csv_file = open(path, 'r', encoding='utf-8-sig')
    csv_iter = csv.reader(csv_file)
    csv_array = [row for row in map(list, zip(*csv_iter))]
    # 행열[y][x] → 열행[x][y] 변환 저장

    if return_shape:  # array_shape
        shape = (len(csv_array), len(csv_array[0]))
        return csv_array, shape
    else:
        return csv_array
