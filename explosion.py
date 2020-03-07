
import pygame


class _Explosion:
    def __init__(self, x, y, palette):
        self.x = x
        self.y = y
        self.size = 0
        self.palette = palette

    def update(self):
        self.size += 4
        return self.size > 255

    def draw(self, background):
        p = (self.x, self.y)
        size = self.size
        w = int(self.size/32)
        pygame.draw.circle(background, self.palette.upper, p, size, w)
        size += -w
        w = int(self.size/16)
        pygame.draw.circle(background, self.palette.middle, p, size, w)
        size += -w
        pygame.draw.circle(background, self.palette.lower, p, size, int(self.size/12))


class Palette:
    def __init__(self, upper, middle, lower):
        self.upper = upper
        self.middle = middle
        self.lower = lower


class ExplosionFactory:
    @staticmethod
    def create_explosion(x, y):
        return _Explosion(x, y, Palette(
            (255, 255, 255),
            (255, 255, 0),
            (255, 0, 0)
        ))

    @staticmethod
    def create_blue_explosion(x, y):
        return _Explosion(x, y, Palette(
            (255, 255, 255),
            (0, 255, 255),
            (0, 0, 255)
        ))
