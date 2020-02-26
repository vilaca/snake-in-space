
import pygame
import random
import math


class Food:
    def __init__(self, w, rev=-1):
        self.w = w
        self.v = True if random.randint(0, 1) == 0 else False
        if self.v:
            if random.randint(0, 1) == 0:
                self.cy = 0
                self.dir = 1
            else:
                self.cy = w[1]
                self.dir = -1
            self.cx = random.randrange(w[0])
        else:
            if random.randint(0, 1) == 0:
                self.cx = 0
                self.dir = 1
            else:
                self.cx = w[0]
                self.dir = -1
            self.cy = random.randrange(w[1])
        self.rad = random.randint(1, 200)
        self.rad_spd = random.randint(10, 50)
        self.x, self.y = self._update()
        self.size = 20 + random.randint(0, 20)
        self.c = (random.randint(16, 255), random.randint(16, 255), random.randint(16, 255))

    def update(self):
        if self.v:
            self.cy = (self.cy + 1 * self.dir) % self.w[1]
            self.x, self.y = self._update()
        else:
            self.cx = (self.cx + 1 * self.dir) % self.w[0]
            self.x, self.y = self._update()

    def _update(self):
        if self.v:
            return self.cx + int(math.sin(self.cy / self.rad_spd) * self.rad), self.cy
        else:
            return self.cx, self.cy + int(math.sin(self.cx / self.rad_spd) * self.rad)

    def draw(self, background):
        pygame.draw.circle(background, self.c, (self.x, self.y), self.size, int(self.size / 2))
