from typing import Tuple, List
from dataclasses import dataclass
import numpy as np


@dataclass
class Bitmap:
    width: int
    height: int
    pixels: List[int]
    mask: np.ndarray = None

    def __post_init__(self):
        if self.width * self.height > len(self.pixels) * 8:
            raise ValueError(f"The bitmap height does not match the description "
                             f"{self.width * self.height} <= {len(self.pixels) * 8}")

        # Precompute the mask from the bitmask constants
        self.mask = np.zeros((self.height, self.width), dtype=np.bool8)
        for i in range(self.width):
            for j in range(self.height):
                idx = i * ((self.height + 7) // 8) + (j // 8)
                self.mask[j, i] = (self.pixels[idx] << j % 8) & 0x80

    def paste(
        self, img: np.ndarray, x: int, y: int,
        fg: Tuple[float, float, float] = (1., 1., 1.),
        bg: Tuple[float, float, float] = (0., 0., 0.)
    ) -> np.ndarray:
        img_y, img_x, img_z = img.shape
        for i, yi in enumerate(range(y, y + self.height)):
            if yi < 0:
                continue
            elif yi > img_y:
                break
            for j, xi in enumerate(range(x, x + self.width)):
                if xi < 0:
                    continue
                elif xi > img_x:
                    break
                if self.mask[i, j]:
                    img[yi, xi] = fg
                else:
                    img[yi, xi] = bg
        return img


Font1206 = {
    " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "!": [0x00, 0x00, 0x00, 0x00, 0x3F, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "\"": [0x00, 0x00, 0x30, 0x00, 0x40, 0x00, 0x30, 0x00, 0x40, 0x00, 0x00, 0x00],
    "#": [0x09, 0x00, 0x0B, 0xC0, 0x3D, 0x00, 0x0B, 0xC0, 0x3D, 0x00, 0x09, 0x00],
    "$": [0x18, 0xC0, 0x24, 0x40, 0x7F, 0xE0, 0x22, 0x40, 0x31, 0x80, 0x00, 0x00],
    "%": [0x18, 0x00, 0x24, 0xC0, 0x1B, 0x00, 0x0D, 0x80, 0x32, 0x40, 0x01, 0x80],
    "&": [0x03, 0x80, 0x1C, 0x40, 0x27, 0x40, 0x1C, 0x80, 0x07, 0x40, 0x00, 0x40],
    "'": [0x10, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "(": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x80, 0x20, 0x40, 0x40, 0x20],
    ")": [0x00, 0x00, 0x40, 0x20, 0x20, 0x40, 0x1F, 0x80, 0x00, 0x00, 0x00, 0x00],
    "*": [0x09, 0x00, 0x06, 0x00, 0x1F, 0x80, 0x06, 0x00, 0x09, 0x00, 0x00, 0x00],
    "+": [0x04, 0x00, 0x04, 0x00, 0x3F, 0x80, 0x04, 0x00, 0x04, 0x00, 0x00, 0x00],
    ",": [0x00, 0x10, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "-": [0x04, 0x00, 0x04, 0x00, 0x04, 0x00, 0x04, 0x00, 0x04, 0x00, 0x00, 0x00],
    ".": [0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "/": [0x00, 0x20, 0x01, 0xC0, 0x06, 0x00, 0x38, 0x00, 0x40, 0x00, 0x00, 0x00],
    "0": [0x1F, 0x80, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x1F, 0x80, 0x00, 0x00],
    "1": [0x00, 0x00, 0x10, 0x40, 0x3F, 0xC0, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00],
    "2": [0x18, 0xC0, 0x21, 0x40, 0x22, 0x40, 0x24, 0x40, 0x18, 0x40, 0x00, 0x00],
    "3": [0x10, 0x80, 0x20, 0x40, 0x24, 0x40, 0x24, 0x40, 0x1B, 0x80, 0x00, 0x00],
    "4": [0x02, 0x00, 0x0D, 0x00, 0x11, 0x00, 0x3F, 0xC0, 0x01, 0x40, 0x00, 0x00],
    "5": [0x3C, 0x80, 0x24, 0x40, 0x24, 0x40, 0x24, 0x40, 0x23, 0x80, 0x00, 0x00],
    "6": [0x1F, 0x80, 0x24, 0x40, 0x24, 0x40, 0x34, 0x40, 0x03, 0x80, 0x00, 0x00],
    "7": [0x30, 0x00, 0x20, 0x00, 0x27, 0xC0, 0x38, 0x00, 0x20, 0x00, 0x00, 0x00],
    "8": [0x1B, 0x80, 0x24, 0x40, 0x24, 0x40, 0x24, 0x40, 0x1B, 0x80, 0x00, 0x00],
    "9": [0x1C, 0x00, 0x22, 0xC0, 0x22, 0x40, 0x22, 0x40, 0x1F, 0x80, 0x00, 0x00],
    ":": [0x00, 0x00, 0x00, 0x00, 0x08, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    ";": [0x00, 0x00, 0x00, 0x00, 0x04, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "<": [0x00, 0x00, 0x04, 0x00, 0x0A, 0x00, 0x11, 0x00, 0x20, 0x80, 0x40, 0x40],
    "=": [0x09, 0x00, 0x09, 0x00, 0x09, 0x00, 0x09, 0x00, 0x09, 0x00, 0x00, 0x00],
    ">": [0x00, 0x00, 0x40, 0x40, 0x20, 0x80, 0x11, 0x00, 0x0A, 0x00, 0x04, 0x00],
    "?": [0x18, 0x00, 0x20, 0x00, 0x23, 0x40, 0x24, 0x00, 0x18, 0x00, 0x00, 0x00],
    "@": [0x1F, 0x80, 0x20, 0x40, 0x27, 0x40, 0x29, 0x40, 0x1F, 0x40, 0x00, 0x00],
    "A": [0x00, 0x40, 0x07, 0xC0, 0x39, 0x00, 0x0F, 0x00, 0x01, 0xC0, 0x00, 0x40],
    "B": [0x20, 0x40, 0x3F, 0xC0, 0x24, 0x40, 0x24, 0x40, 0x1B, 0x80, 0x00, 0x00],
    "C": [0x1F, 0x80, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x30, 0x80, 0x00, 0x00],
    "D": [0x20, 0x40, 0x3F, 0xC0, 0x20, 0x40, 0x20, 0x40, 0x1F, 0x80, 0x00, 0x00],
    "E": [0x20, 0x40, 0x3F, 0xC0, 0x24, 0x40, 0x2E, 0x40, 0x30, 0xC0, 0x00, 0x00],
    "F": [0x20, 0x40, 0x3F, 0xC0, 0x24, 0x40, 0x2E, 0x00, 0x30, 0x00, 0x00, 0x00],
    "G": [0x0F, 0x00, 0x10, 0x80, 0x20, 0x40, 0x22, 0x40, 0x33, 0x80, 0x02, 0x00],
    "H": [0x20, 0x40, 0x3F, 0xC0, 0x04, 0x00, 0x04, 0x00, 0x3F, 0xC0, 0x20, 0x40],
    "I": [0x20, 0x40, 0x20, 0x40, 0x3F, 0xC0, 0x20, 0x40, 0x20, 0x40, 0x00, 0x00],
    "J": [0x00, 0x60, 0x20, 0x20, 0x20, 0x20, 0x3F, 0xC0, 0x20, 0x00, 0x20, 0x00],
    "K": [0x20, 0x40, 0x3F, 0xC0, 0x24, 0x40, 0x0B, 0x00, 0x30, 0xC0, 0x20, 0x40],
    "L": [0x20, 0x40, 0x3F, 0xC0, 0x20, 0x40, 0x00, 0x40, 0x00, 0x40, 0x00, 0xC0],
    "M": [0x3F, 0xC0, 0x3C, 0x00, 0x03, 0xC0, 0x3C, 0x00, 0x3F, 0xC0, 0x00, 0x00],
    "N": [0x20, 0x40, 0x3F, 0xC0, 0x0C, 0x40, 0x23, 0x00, 0x3F, 0xC0, 0x20, 0x00],
    "O": [0x1F, 0x80, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x1F, 0x80, 0x00, 0x00],
    "P": [0x20, 0x40, 0x3F, 0xC0, 0x24, 0x40, 0x24, 0x00, 0x18, 0x00, 0x00, 0x00],
    "Q": [0x1F, 0x80, 0x21, 0x40, 0x21, 0x40, 0x20, 0xE0, 0x1F, 0xA0, 0x00, 0x00],
    "R": [0x20, 0x40, 0x3F, 0xC0, 0x24, 0x40, 0x26, 0x00, 0x19, 0xC0, 0x00, 0x40],
    "S": [0x18, 0xC0, 0x24, 0x40, 0x24, 0x40, 0x22, 0x40, 0x31, 0x80, 0x00, 0x00],
    "T": [0x30, 0x00, 0x20, 0x40, 0x3F, 0xC0, 0x20, 0x40, 0x30, 0x00, 0x00, 0x00],
    "U": [0x20, 0x00, 0x3F, 0x80, 0x00, 0x40, 0x00, 0x40, 0x3F, 0x80, 0x20, 0x00],
    "V": [0x20, 0x00, 0x3E, 0x00, 0x01, 0xC0, 0x07, 0x00, 0x38, 0x00, 0x20, 0x00],
    "W": [0x38, 0x00, 0x07, 0xC0, 0x3C, 0x00, 0x07, 0xC0, 0x38, 0x00, 0x00, 0x00],
    "X": [0x20, 0x40, 0x39, 0xC0, 0x06, 0x00, 0x39, 0xC0, 0x20, 0x40, 0x00, 0x00],
    "Y": [0x20, 0x00, 0x38, 0x40, 0x07, 0xC0, 0x38, 0x40, 0x20, 0x00, 0x00, 0x00],
    "Z": [0x30, 0x40, 0x21, 0xC0, 0x26, 0x40, 0x38, 0x40, 0x20, 0xC0, 0x00, 0x00],
    "[": [0x00, 0x00, 0x00, 0x00, 0x7F, 0xE0, 0x40, 0x20, 0x40, 0x20, 0x00, 0x00],
    "\\": [0x00, 0x00, 0x70, 0x00, 0x0C, 0x00, 0x03, 0x80, 0x00, 0x40, 0x00, 0x00],
    "]": [0x00, 0x00, 0x40, 0x20, 0x40, 0x20, 0x7F, 0xE0, 0x00, 0x00, 0x00, 0x00],
    "^": [0x00, 0x00, 0x20, 0x00, 0x40, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00],
    "_": [0x00, 0x10, 0x00, 0x10, 0x00, 0x10, 0x00, 0x10, 0x00, 0x10, 0x00, 0x10],
    "`": [0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "a": [0x00, 0x00, 0x02, 0x80, 0x05, 0x40, 0x05, 0x40, 0x03, 0xC0, 0x00, 0x40],
    "b": [0x20, 0x00, 0x3F, 0xC0, 0x04, 0x40, 0x04, 0x40, 0x03, 0x80, 0x00, 0x00],
    "c": [0x00, 0x00, 0x03, 0x80, 0x04, 0x40, 0x04, 0x40, 0x06, 0x40, 0x00, 0x00],
    "d": [0x00, 0x00, 0x03, 0x80, 0x04, 0x40, 0x24, 0x40, 0x3F, 0xC0, 0x00, 0x40],
    "e": [0x00, 0x00, 0x03, 0x80, 0x05, 0x40, 0x05, 0x40, 0x03, 0x40, 0x00, 0x00],
    "f": [0x00, 0x00, 0x04, 0x40, 0x1F, 0xC0, 0x24, 0x40, 0x24, 0x40, 0x20, 0x00],
    "g": [0x00, 0x00, 0x02, 0xE0, 0x05, 0x50, 0x05, 0x50, 0x06, 0x50, 0x04, 0x20],
    "h": [0x20, 0x40, 0x3F, 0xC0, 0x04, 0x40, 0x04, 0x00, 0x03, 0xC0, 0x00, 0x40],
    "i": [0x00, 0x00, 0x04, 0x40, 0x27, 0xC0, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00],
    "j": [0x00, 0x10, 0x00, 0x10, 0x04, 0x10, 0x27, 0xE0, 0x00, 0x00, 0x00, 0x00],
    "k": [0x20, 0x40, 0x3F, 0xC0, 0x01, 0x40, 0x07, 0x00, 0x04, 0xC0, 0x04, 0x40],
    "l": [0x20, 0x40, 0x20, 0x40, 0x3F, 0xC0, 0x00, 0x40, 0x00, 0x40, 0x00, 0x00],
    "m": [0x07, 0xC0, 0x04, 0x00, 0x07, 0xC0, 0x04, 0x00, 0x03, 0xC0, 0x00, 0x00],
    "n": [0x04, 0x40, 0x07, 0xC0, 0x04, 0x40, 0x04, 0x00, 0x03, 0xC0, 0x00, 0x40],
    "o": [0x00, 0x00, 0x03, 0x80, 0x04, 0x40, 0x04, 0x40, 0x03, 0x80, 0x00, 0x00],
    "p": [0x04, 0x10, 0x07, 0xF0, 0x04, 0x50, 0x04, 0x40, 0x03, 0x80, 0x00, 0x00],
    "q": [0x00, 0x00, 0x03, 0x80, 0x04, 0x40, 0x04, 0x50, 0x07, 0xF0, 0x00, 0x10],
    "r": [0x04, 0x40, 0x07, 0xC0, 0x02, 0x40, 0x04, 0x00, 0x04, 0x00, 0x00, 0x00],
    "s": [0x00, 0x00, 0x06, 0x40, 0x05, 0x40, 0x05, 0x40, 0x04, 0xC0, 0x00, 0x00],
    "t": [0x00, 0x00, 0x04, 0x00, 0x1F, 0x80, 0x04, 0x40, 0x00, 0x40, 0x00, 0x00],
    "u": [0x04, 0x00, 0x07, 0x80, 0x00, 0x40, 0x04, 0x40, 0x07, 0xC0, 0x00, 0x40],
    "v": [0x04, 0x00, 0x07, 0x00, 0x04, 0xC0, 0x01, 0x80, 0x06, 0x00, 0x04, 0x00],
    "w": [0x06, 0x00, 0x01, 0xC0, 0x07, 0x00, 0x01, 0xC0, 0x06, 0x00, 0x00, 0x00],
    "x": [0x04, 0x40, 0x06, 0xC0, 0x01, 0x00, 0x06, 0xC0, 0x04, 0x40, 0x00, 0x00],
    "y": [0x04, 0x10, 0x07, 0x10, 0x04, 0xE0, 0x01, 0x80, 0x06, 0x00, 0x04, 0x00],
    "z": [0x00, 0x00, 0x04, 0x40, 0x05, 0xC0, 0x06, 0x40, 0x04, 0x40, 0x00, 0x00],
    "{": [0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x7B, 0xE0, 0x40, 0x20, 0x00, 0x00],
    "|": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xF0, 0x00, 0x00, 0x00, 0x00],
    "}": [0x00, 0x00, 0x40, 0x20, 0x7B, 0xE0, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00],
    "~": [0x40, 0x00, 0x80, 0x00, 0x40, 0x00, 0x20, 0x00, 0x20, 0x00, 0x40, 0x00],
}


Font1608 = {
    " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "!": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xCC, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "\"": [0x00, 0x00, 0x08, 0x00, 0x30, 0x00, 0x60, 0x00, 0x08, 0x00, 0x30, 0x00, 0x60, 0x00, 0x00, 0x00],
    "#": [0x02, 0x20, 0x03, 0xFC, 0x1E, 0x20, 0x02, 0x20, 0x03, 0xFC, 0x1E, 0x20, 0x02, 0x20, 0x00, 0x00],
    "$": [0x00, 0x00, 0x0E, 0x18, 0x11, 0x04, 0x3F, 0xFF, 0x10, 0x84, 0x0C, 0x78, 0x00, 0x00, 0x00, 0x00],
    "%": [0x0F, 0x00, 0x10, 0x84, 0x0F, 0x38, 0x00, 0xC0, 0x07, 0x78, 0x18, 0x84, 0x00, 0x78, 0x00, 0x00],
    "&": [0x00, 0x78, 0x0F, 0x84, 0x10, 0xC4, 0x11, 0x24, 0x0E, 0x98, 0x00, 0xE4, 0x00, 0x84, 0x00, 0x08],
    "'": [0x08, 0x00, 0x68, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "(": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xE0, 0x18, 0x18, 0x20, 0x04, 0x40, 0x02, 0x00, 0x00],
    ")": [0x00, 0x00, 0x40, 0x02, 0x20, 0x04, 0x18, 0x18, 0x07, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "*": [0x02, 0x40, 0x02, 0x40, 0x01, 0x80, 0x0F, 0xF0, 0x01, 0x80, 0x02, 0x40, 0x02, 0x40, 0x00, 0x00],
    "+": [0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x0F, 0xF8, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x00],
    ",": [0x00, 0x01, 0x00, 0x0D, 0x00, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "-": [0x00, 0x00, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80],
    ".": [0x00, 0x00, 0x00, 0x0C, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "/": [0x00, 0x00, 0x00, 0x06, 0x00, 0x18, 0x00, 0x60, 0x01, 0x80, 0x06, 0x00, 0x18, 0x00, 0x20, 0x00],
    "0": [0x00, 0x00, 0x07, 0xF0, 0x08, 0x08, 0x10, 0x04, 0x10, 0x04, 0x08, 0x08, 0x07, 0xF0, 0x00, 0x00],
    "1": [0x00, 0x00, 0x08, 0x04, 0x08, 0x04, 0x1F, 0xFC, 0x00, 0x04, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00],
    "2": [0x00, 0x00, 0x0E, 0x0C, 0x10, 0x14, 0x10, 0x24, 0x10, 0x44, 0x11, 0x84, 0x0E, 0x0C, 0x00, 0x00],
    "3": [0x00, 0x00, 0x0C, 0x18, 0x10, 0x04, 0x11, 0x04, 0x11, 0x04, 0x12, 0x88, 0x0C, 0x70, 0x00, 0x00],
    "4": [0x00, 0x00, 0x00, 0xE0, 0x03, 0x20, 0x04, 0x24, 0x08, 0x24, 0x1F, 0xFC, 0x00, 0x24, 0x00, 0x00],
    "5": [0x00, 0x00, 0x1F, 0x98, 0x10, 0x84, 0x11, 0x04, 0x11, 0x04, 0x10, 0x88, 0x10, 0x70, 0x00, 0x00],
    "6": [0x00, 0x00, 0x07, 0xF0, 0x08, 0x88, 0x11, 0x04, 0x11, 0x04, 0x18, 0x88, 0x00, 0x70, 0x00, 0x00],
    "7": [0x00, 0x00, 0x1C, 0x00, 0x10, 0x00, 0x10, 0xFC, 0x13, 0x00, 0x1C, 0x00, 0x10, 0x00, 0x00, 0x00],
    "8": [0x00, 0x00, 0x0E, 0x38, 0x11, 0x44, 0x10, 0x84, 0x10, 0x84, 0x11, 0x44, 0x0E, 0x38, 0x00, 0x00],
    "9": [0x00, 0x00, 0x07, 0x00, 0x08, 0x8C, 0x10, 0x44, 0x10, 0x44, 0x08, 0x88, 0x07, 0xF0, 0x00, 0x00],
    ":": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x0C, 0x03, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    ";": [0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "<": [0x00, 0x00, 0x00, 0x80, 0x01, 0x40, 0x02, 0x20, 0x04, 0x10, 0x08, 0x08, 0x10, 0x04, 0x00, 0x00],
    "=": [0x02, 0x20, 0x02, 0x20, 0x02, 0x20, 0x02, 0x20, 0x02, 0x20, 0x02, 0x20, 0x02, 0x20, 0x00, 0x00],
    ">": [0x00, 0x00, 0x10, 0x04, 0x08, 0x08, 0x04, 0x10, 0x02, 0x20, 0x01, 0x40, 0x00, 0x80, 0x00, 0x00],
    "?": [0x00, 0x00, 0x0E, 0x00, 0x12, 0x00, 0x10, 0x0C, 0x10, 0x6C, 0x10, 0x80, 0x0F, 0x00, 0x00, 0x00],
    "@": [0x03, 0xE0, 0x0C, 0x18, 0x13, 0xE4, 0x14, 0x24, 0x17, 0xC4, 0x08, 0x28, 0x07, 0xD0, 0x00, 0x00],
    "A": [0x00, 0x04, 0x00, 0x3C, 0x03, 0xC4, 0x1C, 0x40, 0x07, 0x40, 0x00, 0xE4, 0x00, 0x1C, 0x00, 0x04],
    "B": [0x10, 0x04, 0x1F, 0xFC, 0x11, 0x04, 0x11, 0x04, 0x11, 0x04, 0x0E, 0x88, 0x00, 0x70, 0x00, 0x00],
    "C": [0x03, 0xE0, 0x0C, 0x18, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x10, 0x08, 0x1C, 0x10, 0x00, 0x00],
    "D": [0x10, 0x04, 0x1F, 0xFC, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x08, 0x08, 0x07, 0xF0, 0x00, 0x00],
    "E": [0x10, 0x04, 0x1F, 0xFC, 0x11, 0x04, 0x11, 0x04, 0x17, 0xC4, 0x10, 0x04, 0x08, 0x18, 0x00, 0x00],
    "F": [0x10, 0x04, 0x1F, 0xFC, 0x11, 0x04, 0x11, 0x00, 0x17, 0xC0, 0x10, 0x00, 0x08, 0x00, 0x00, 0x00],
    "G": [0x03, 0xE0, 0x0C, 0x18, 0x10, 0x04, 0x10, 0x04, 0x10, 0x44, 0x1C, 0x78, 0x00, 0x40, 0x00, 0x00],
    "H": [0x10, 0x04, 0x1F, 0xFC, 0x10, 0x84, 0x00, 0x80, 0x00, 0x80, 0x10, 0x84, 0x1F, 0xFC, 0x10, 0x04],
    "I": [0x00, 0x00, 0x10, 0x04, 0x10, 0x04, 0x1F, 0xFC, 0x10, 0x04, 0x10, 0x04, 0x00, 0x00, 0x00, 0x00],
    "J": [0x00, 0x03, 0x00, 0x01, 0x10, 0x01, 0x10, 0x01, 0x1F, 0xFE, 0x10, 0x00, 0x10, 0x00, 0x00, 0x00],
    "K": [0x10, 0x04, 0x1F, 0xFC, 0x11, 0x04, 0x03, 0x80, 0x14, 0x64, 0x18, 0x1C, 0x10, 0x04, 0x00, 0x00],
    "L": [0x10, 0x04, 0x1F, 0xFC, 0x10, 0x04, 0x00, 0x04, 0x00, 0x04, 0x00, 0x04, 0x00, 0x0C, 0x00, 0x00],
    "M": [0x10, 0x04, 0x1F, 0xFC, 0x1F, 0x00, 0x00, 0xFC, 0x1F, 0x00, 0x1F, 0xFC, 0x10, 0x04, 0x00, 0x00],
    "N": [0x10, 0x04, 0x1F, 0xFC, 0x0C, 0x04, 0x03, 0x00, 0x00, 0xE0, 0x10, 0x18, 0x1F, 0xFC, 0x10, 0x00],
    "O": [0x07, 0xF0, 0x08, 0x08, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x08, 0x08, 0x07, 0xF0, 0x00, 0x00],
    "P": [0x10, 0x04, 0x1F, 0xFC, 0x10, 0x84, 0x10, 0x80, 0x10, 0x80, 0x10, 0x80, 0x0F, 0x00, 0x00, 0x00],
    "Q": [0x07, 0xF0, 0x08, 0x18, 0x10, 0x24, 0x10, 0x24, 0x10, 0x1C, 0x08, 0x0A, 0x07, 0xF2, 0x00, 0x00],
    "R": [0x10, 0x04, 0x1F, 0xFC, 0x11, 0x04, 0x11, 0x00, 0x11, 0xC0, 0x11, 0x30, 0x0E, 0x0C, 0x00, 0x04],
    "S": [0x00, 0x00, 0x0E, 0x1C, 0x11, 0x04, 0x10, 0x84, 0x10, 0x84, 0x10, 0x44, 0x1C, 0x38, 0x00, 0x00],
    "T": [0x18, 0x00, 0x10, 0x00, 0x10, 0x04, 0x1F, 0xFC, 0x10, 0x04, 0x10, 0x00, 0x18, 0x00, 0x00, 0x00],
    "U": [0x10, 0x00, 0x1F, 0xF8, 0x10, 0x04, 0x00, 0x04, 0x00, 0x04, 0x10, 0x04, 0x1F, 0xF8, 0x10, 0x00],
    "V": [0x10, 0x00, 0x1E, 0x00, 0x11, 0xE0, 0x00, 0x1C, 0x00, 0x70, 0x13, 0x80, 0x1C, 0x00, 0x10, 0x00],
    "W": [0x1F, 0xC0, 0x10, 0x3C, 0x00, 0xE0, 0x1F, 0x00, 0x00, 0xE0, 0x10, 0x3C, 0x1F, 0xC0, 0x00, 0x00],
    "X": [0x10, 0x04, 0x18, 0x0C, 0x16, 0x34, 0x01, 0xC0, 0x01, 0xC0, 0x16, 0x34, 0x18, 0x0C, 0x10, 0x04],
    "Y": [0x10, 0x00, 0x1C, 0x00, 0x13, 0x04, 0x00, 0xFC, 0x13, 0x04, 0x1C, 0x00, 0x10, 0x00, 0x00, 0x00],
    "Z": [0x08, 0x04, 0x10, 0x1C, 0x10, 0x64, 0x10, 0x84, 0x13, 0x04, 0x1C, 0x04, 0x10, 0x18, 0x00, 0x00],
    "[": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0xFE, 0x40, 0x02, 0x40, 0x02, 0x40, 0x02, 0x00, 0x00],
    "\\": [0x00, 0x00, 0x30, 0x00, 0x0C, 0x00, 0x03, 0x80, 0x00, 0x60, 0x00, 0x1C, 0x00, 0x03, 0x00, 0x00],
    "]": [0x00, 0x00, 0x40, 0x02, 0x40, 0x02, 0x40, 0x02, 0x7F, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "^": [0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x40, 0x00, 0x40, 0x00, 0x40, 0x00, 0x20, 0x00, 0x00, 0x00],
    "_": [0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01],
    "`": [0x00, 0x00, 0x40, 0x00, 0x40, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "a": [0x00, 0x00, 0x00, 0x98, 0x01, 0x24, 0x01, 0x44, 0x01, 0x44, 0x01, 0x44, 0x00, 0xFC, 0x00, 0x04],
    "b": [0x10, 0x00, 0x1F, 0xFC, 0x00, 0x88, 0x01, 0x04, 0x01, 0x04, 0x00, 0x88, 0x00, 0x70, 0x00, 0x00],
    "c": [0x00, 0x00, 0x00, 0x70, 0x00, 0x88, 0x01, 0x04, 0x01, 0x04, 0x01, 0x04, 0x00, 0x88, 0x00, 0x00],
    "d": [0x00, 0x00, 0x00, 0x70, 0x00, 0x88, 0x01, 0x04, 0x01, 0x04, 0x11, 0x08, 0x1F, 0xFC, 0x00, 0x04],
    "e": [0x00, 0x00, 0x00, 0xF8, 0x01, 0x44, 0x01, 0x44, 0x01, 0x44, 0x01, 0x44, 0x00, 0xC8, 0x00, 0x00],
    "f": [0x00, 0x00, 0x01, 0x04, 0x01, 0x04, 0x0F, 0xFC, 0x11, 0x04, 0x11, 0x04, 0x11, 0x00, 0x18, 0x00],
    "g": [0x00, 0x00, 0x00, 0xD6, 0x01, 0x29, 0x01, 0x29, 0x01, 0x29, 0x01, 0xC9, 0x01, 0x06, 0x00, 0x00],
    "h": [0x10, 0x04, 0x1F, 0xFC, 0x00, 0x84, 0x01, 0x00, 0x01, 0x00, 0x01, 0x04, 0x00, 0xFC, 0x00, 0x04],
    "i": [0x00, 0x00, 0x01, 0x04, 0x19, 0x04, 0x19, 0xFC, 0x00, 0x04, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00],
    "j": [0x00, 0x00, 0x00, 0x03, 0x00, 0x01, 0x01, 0x01, 0x19, 0x01, 0x19, 0xFE, 0x00, 0x00, 0x00, 0x00],
    "k": [0x10, 0x04, 0x1F, 0xFC, 0x00, 0x24, 0x00, 0x40, 0x01, 0xB4, 0x01, 0x0C, 0x01, 0x04, 0x00, 0x00],
    "l": [0x00, 0x00, 0x10, 0x04, 0x10, 0x04, 0x1F, 0xFC, 0x00, 0x04, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00],
    "m": [0x01, 0x04, 0x01, 0xFC, 0x01, 0x04, 0x01, 0x00, 0x01, 0xFC, 0x01, 0x04, 0x01, 0x00, 0x00, 0xFC],
    "n": [0x01, 0x04, 0x01, 0xFC, 0x00, 0x84, 0x01, 0x00, 0x01, 0x00, 0x01, 0x04, 0x00, 0xFC, 0x00, 0x04],
    "o": [0x00, 0x00, 0x00, 0xF8, 0x01, 0x04, 0x01, 0x04, 0x01, 0x04, 0x01, 0x04, 0x00, 0xF8, 0x00, 0x00],
    "p": [0x01, 0x01, 0x01, 0xFF, 0x00, 0x85, 0x01, 0x04, 0x01, 0x04, 0x00, 0x88, 0x00, 0x70, 0x00, 0x00],
    "q": [0x00, 0x00, 0x00, 0x70, 0x00, 0x88, 0x01, 0x04, 0x01, 0x04, 0x01, 0x05, 0x01, 0xFF, 0x00, 0x01],
    "r": [0x01, 0x04, 0x01, 0x04, 0x01, 0xFC, 0x00, 0x84, 0x01, 0x04, 0x01, 0x00, 0x01, 0x80, 0x00, 0x00],
    "s": [0x00, 0x00, 0x00, 0xCC, 0x01, 0x24, 0x01, 0x24, 0x01, 0x24, 0x01, 0x24, 0x01, 0x98, 0x00, 0x00],
    "t": [0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x07, 0xF8, 0x01, 0x04, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00],
    "u": [0x01, 0x00, 0x01, 0xF8, 0x00, 0x04, 0x00, 0x04, 0x00, 0x04, 0x01, 0x08, 0x01, 0xFC, 0x00, 0x04],
    "v": [0x01, 0x00, 0x01, 0x80, 0x01, 0x70, 0x00, 0x0C, 0x00, 0x10, 0x01, 0x60, 0x01, 0x80, 0x01, 0x00],
    "w": [0x01, 0xF0, 0x01, 0x0C, 0x00, 0x30, 0x01, 0xC0, 0x00, 0x30, 0x01, 0x0C, 0x01, 0xF0, 0x01, 0x00],
    "x": [0x00, 0x00, 0x01, 0x04, 0x01, 0x8C, 0x00, 0x74, 0x01, 0x70, 0x01, 0x8C, 0x01, 0x04, 0x00, 0x00],
    "y": [0x01, 0x01, 0x01, 0x81, 0x01, 0x71, 0x00, 0x0E, 0x00, 0x18, 0x01, 0x60, 0x01, 0x80, 0x01, 0x00],
    "z": [0x00, 0x00, 0x01, 0x84, 0x01, 0x0C, 0x01, 0x34, 0x01, 0x44, 0x01, 0x84, 0x01, 0x0C, 0x00, 0x00],
    "{": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x3E, 0xFC, 0x40, 0x02, 0x40, 0x02],
    "|": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "}": [0x00, 0x00, 0x40, 0x02, 0x40, 0x02, 0x3E, 0xFC, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "~": [0x00, 0x00, 0x60, 0x00, 0x80, 0x00, 0x80, 0x00, 0x40, 0x00, 0x40, 0x00, 0x20, 0x00, 0x20, 0x00],
}


Font1612 = {
    "0": [0x00, 0x00, 0x3F, 0xFC, 0x3F, 0xFC, 0x30, 0x0C, 0x30, 0x0C, 0x30, 0x0C, 0x30, 0x0C, 0x30, 0x0C,
          0x30, 0x0C, 0x30, 0x0C, 0x30, 0x0C, 0x30, 0x0C, 0x30, 0x0C, 0x3F, 0xFC, 0x3F, 0xFC, 0x00, 0x00],
    "1": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x00,
          0x30, 0x00, 0x3F, 0xFC, 0x3F, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "2": [0x00, 0x00, 0x39, 0xFC, 0x39, 0xFC, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C,
          0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x3F, 0x8C, 0x3F, 0x8C, 0x00, 0x00],
    "3": [0x00, 0x00, 0x38, 0x1C, 0x38, 0x1C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C,
          0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x3F, 0xFC, 0x3F, 0xFC, 0x00, 0x00],
    "4": [0x00, 0x00, 0x3F, 0x80, 0x3F, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80,
          0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x80, 0x3F, 0xFC, 0x3F, 0xFC, 0x00, 0x00],
    "5": [0x00, 0x00, 0x3F, 0xBC, 0x3F, 0xBC, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C,
          0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0xFC, 0x31, 0xFC, 0x00, 0x00],
    "6": [0x00, 0x00, 0x3F, 0x9C, 0x3F, 0x9C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C,
          0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0xFC, 0x31, 0xFC, 0x00, 0x00],
    "7": [0x00, 0x00, 0x38, 0x00, 0x38, 0x00, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00,
          0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x3F, 0xFC, 0x3F, 0xFC, 0x00, 0x00],
    "8": [0x00, 0x00, 0x3F, 0xFC, 0x3F, 0xFC, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C,
          0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x3F, 0xFC, 0x3F, 0xFC, 0x00, 0x00],
    "9": [0x00, 0x00, 0x3F, 0x9C, 0x3F, 0x9C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C,
          0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x31, 0x8C, 0x3F, 0xFC, 0x3F, 0xFC, 0x00, 0x00],
    ":": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x30,
          0x18, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
}


Font3216 = {
    "0": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC,  # "0",0
          0x30, 0x00, 0x00, 0x0C, 0x30, 0x00, 0x00, 0x0C, 0x30, 0x00, 0x00, 0x0C, 0x30, 0x00, 0x00, 0x0C,
          0x30, 0x00, 0x00, 0x0C, 0x30, 0x00, 0x00, 0x0C, 0x30, 0x00, 0x00, 0x0C, 0x30, 0x00, 0x00, 0x0C,
          0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "1": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # "1",1
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00,
          0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "2": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3C, 0x01, 0xFF, 0xFC, 0x3C, 0x01, 0xFF, 0xFC,  # "2",2
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x3F, 0xFF, 0x80, 0x0C, 0x3F, 0xFF, 0x80, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "3": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x3C, 0x38, 0x00, 0x00, 0x3C,  # "3",3
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "4": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0x80, 0x00, 0x3F, 0xFF, 0x80, 0x00,  # "4",4
          0x00, 0x01, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00,
          0x00, 0x01, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00,
          0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "5": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0x80, 0x3C, 0x3F, 0xFF, 0x80, 0x3C,  # "5",5
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x30, 0x01, 0xFF, 0xFC, 0x30, 0x01, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "6": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC,  # "6",6
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x3C, 0x01, 0xFF, 0xFC, 0x3C, 0x01, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "7": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x00,  # "7",7
          0x30, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00,
          0x30, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00,
          0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "8": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC,  # "8",8
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    "9": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0x80, 0x3C, 0x3F, 0xFF, 0x80, 0x3C,  # "9",9
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C, 0x30, 0x01, 0x80, 0x0C,
          0x3F, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    ":": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # ":",10
          0x00, 0x00, 0x00, 0x00, 0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0, 0x0C, 0x00, 0x00, 0x30,
          0x0C, 0x00, 0x00, 0x30, 0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
}

symbols = {
    "sum": Bitmap(40, 16, [
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xF1, 0x81, 0x8F, 0xFC, 0x3F,
        0xF1, 0x81, 0x8F, 0xFC, 0x30, 0x31, 0x81, 0x8C, 0x0C, 0x30, 0x01, 0x81, 0x8C, 0x0C, 0x30, 0x01,
        0x81, 0x8C, 0x0C, 0x3F, 0xF1, 0x81, 0x8C, 0x0C, 0x3F, 0xF1, 0x81, 0x8C, 0x0C, 0x00, 0x31, 0x81,
        0x8C, 0x0C, 0x00, 0x31, 0x81, 0x8C, 0x0C, 0x30, 0x31, 0x81, 0x8C, 0x0C, 0x3F, 0xF1, 0xFF, 0x8C,
        0x0C, 0x3F, 0xF1, 0xFF, 0x8C, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]),
    "signal": Bitmap(16, 8, [
        0xFE, 0x02, 0x92, 0x0A, 0x54, 0x2A, 0x38, 0xAA, 0x12, 0xAA, 0x12, 0xAA, 0x12, 0xAA, 0x12, 0xAA
    ]),
    "message": Bitmap(16, 8, [
        0x1F, 0xF8, 0x10, 0x08, 0x18, 0x18, 0x14, 0x28, 0x13, 0xC8, 0x10, 0x08, 0x10, 0x08, 0x1F, 0xF8
    ]),
    "battery": Bitmap(16, 8, [
        0x0F, 0xFE, 0x30, 0x02, 0x26, 0xDA, 0x26, 0xDA, 0x26, 0xDA, 0x26, 0xDA, 0x30, 0x02, 0x0F, 0xFE
    ]),
    "bluetooth": Bitmap(8, 8, [
        0x18, 0x54, 0x32, 0x1C, 0x1C, 0x32, 0x54, 0x18
    ]),
    "gprs": Bitmap(8, 8, [
        0xC3, 0x99, 0x24, 0x20, 0x2C, 0x24, 0x99, 0xC3
    ]),
    "alarm": Bitmap(8, 8, [
        0xC3, 0xBD, 0x42, 0x52, 0x4E, 0x42, 0x3C, 0xC3
    ])
}


Font1206 = {k: Bitmap(6, 12, v) for k, v in Font1206.items()}
Font1608 = {k: Bitmap(8, 16, v) for k, v in Font1608.items()}
Font1612 = {k: Bitmap(12, 16, v) for k, v in Font1612.items()}
Font3216 = {k: Bitmap(16, 32, v) for k, v in Font3216.items()}


def put_string(
        img: np.ndarray, x: int, y: int, s: str,
        fg: Tuple[float, float, float] = (1., 1., 1.), bg: Tuple[float, float, float] = (0., 0., 0.),
        font=None
    ) -> np.ndarray:
    if font is None:
        font = Font1206
    for c in s:
        bm = font[c]
        bm.paste(img, x, y, fg, bg)
        x += bm.width
    return img
