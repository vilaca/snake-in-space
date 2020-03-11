
import pygame
import random
import math


class Food:
    def __init__(self, w, cx, cy, direction, v):
        self.grace = 120
        self.v = v
        self.dir = direction
        self.cx = cx
        self.cy = cy
        self.w = w
        self.rad = random.randint(1, 200)
        self.rad_spd = random.randint(10, 50)
        self.x, self.y = self._update()
        self.size = random.randint(20, 40)
        while True:
            r = random.randint(96, 255)
            g = random.randint(96, 255)
            b = random.randint(96, 255)
            if (r+b+g)/3 > 192:
                self.c = (r, g, b)
                break

    def update(self):
        self.grace -= 1
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

    def is_in_grace(self):
        return self.grace > 0

    def draw(self, background):
        if self.is_in_grace() and self.grace & 5:
            pygame.draw.circle(background, (64, 64, 64), (self.x, self.y), self.size, 2)
            pygame.draw.circle(background, (
                255-self.c[0],
                255-self.c[1],
                255-self.c[2]
            ), (self.x, self.y), self.size - 2, int(self.size / 2))
            return
        pygame.draw.circle(background, (128, 128, 128), (self.x, self.y), self.size, 2)
        pygame.draw.circle(background, self.c, (self.x, self.y), self.size-2, int(self.size / 2))
        pygame.draw.circle(background, (128, 128, 128), (self.x, self.y), int(self.size/2)-1, 1)


class FoodFactory:
    @staticmethod
    def create_random(screen_dim):
        v = True if random.randint(0, 1) == 0 else False
        if v:
            if random.randint(0, 1) == 0:
                cy = 0
                direction = 1
            else:
                cy = screen_dim[1]
                direction = -1
            cx = random.randint(0, screen_dim[0])
        else:
            if random.randint(0, 1) == 0:
                cx = 0
                direction = 1
            else:
                cx = screen_dim[0]
                direction = -1
            cy = random.randint(0, screen_dim[1])
        return Food(screen_dim, cx, cy, direction, v)

    @staticmethod
    def create(screen_dim, n):
        return Food(screen_dim, n.x, n.y, 1, True)
