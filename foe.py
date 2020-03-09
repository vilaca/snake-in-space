
import pygame
import random
import math


class Foe:
    def __init__(self, w, rev=-1):
        self.spike_size = random.randint(4, 12)
        self.w = w
        self.v = random.randint(0, 1) == 0
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
        while True:
            r = random.randint(128, 255)
            g = random.randint(128, 255)
            b = random.randint(128, 255)
            if (r+b+g)/3 > 180:
                self.c = (r, g, b)
                break

    def update(self):
        if self.v:
            self.cy = (self.cy + 1 * self.dir) % self.w[1]
            self.x, self.y = self._update()
        else:
            self.cx = (self.cx + 1 * self.dir) % self.w[0]
            self.x, self. y = self._update()

    def _update(self):
        if self.v:
            return self.cx + int(math.cos(self.cy / self.rad_spd) * self.rad), self.cy
        else:
            return self.cx, self.cy + int(math.sin(self.cx/self.rad_spd) * self.rad)

    def draw(self, background):
        m = random.randrange(4, 8)
        for i in range(0, 20):
            r = math.pi*2/20*i
            x = math.cos(r) * self.size
            y = math.sin(r*m) * self.size
            pygame.draw.line(background, self.c, (self.x+x/2, self.y+y/2),  (self.x+x, self.y+y), self.spike_size)
        p = (255 - self.c[0], 255 - self.c[1], 255 - self.c[2])
        pygame.draw.circle(background, p, (self.x, self.y), int(self.size / 5))
