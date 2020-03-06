
import pygame


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0

    def update(self):
        self.size += 4
        return self.size > 255

    def draw(self, background):
        p = (self.x, self.y)
        size = self.size
        w = int(self.size/32)
        pygame.draw.circle(background, (255, 255, 255), p, size, w)
        size += -w
        w = int(self.size/16)
        pygame.draw.circle(background, (255, 255, 0), p, size, w)
        size += -w
        pygame.draw.circle(background, (255, 0, 0), p, size, int(self.size/12))
