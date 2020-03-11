import random
import pygame
import math


class Bubble:
    def __init__(self, dx, dy, max_xy, x, y, size):
        self.dx = dx
        self.dy = dy
        self.size = size
        self.max_x = max_xy[0]
        self.max_y = max_xy[1]
        self.x = x
        self.y = y
        self.grace = 121
        self.slices = math.pi * -2 / 192
        self.st = 0
        self.last = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > self.max_x:
            self.dx *= -1
        if self.y < 0 or self.y > self.max_y:
            self.dy *= -1

    def draw_body(self, screen):
        r = self.slices * self.st
        r2 = self.slices * (self.st+4)
        r3 = self.slices * (self.st+8)
        c = 192
        while True:
            pygame.draw.line(screen,
                             (255, 255, 0),
                             (self.x, self.y),
                             (int(self.x + math.cos(r) * self.size), int(self.y + math.sin(r) * self.size)),
                             int(self.size/10)
                             )
            pygame.draw.line(screen,
                             (255, 0, 255),
                             (self.x, self.y),
                             (int(self.x + math.cos(r2) * self.size/2), int(self.y + math.sin(r2) * self.size/2)),
                             int(self.size/12)
                             )
            pygame.draw.line(screen,
                             (0, 255, 255),
                             (self.x, self.y),
                             (int(self.x + math.cos(r3) * self.size), int(self.y + math.sin(r3) * self.size)),
                             int(self.size/16)
                             )
            inc = 32
            r += self.slices * inc
            r2 += self.slices * inc
            r3 += self.slices * inc
            c -= inc
            if c < 0:
                break

    def draw_triangle(self, screen):
        r = self.slices * self.st
        c = 192
        last = (int(self.x + math.cos(r) * self.size), int(self.y + math.sin(r) * self.size))
        while True:
            pygame.draw.line(screen,
                             (255, 255, 255),
                             (int(self.x + math.cos(r) * self.size), int(self.y + math.sin(r) * self.size)),
                             last,
                             int(self.size/12))
            last = (int(self.x + math.cos(r) * self.size), int(self.y + math.sin(r) * self.size))
            inc = 32
            c -= inc
            r += self.slices * inc
            if c < 0:
                break

    def draw(self, screen):
        self.st += 1
        if self.st > 192:
            self.st = 0
        if self.grace > 1:
            self.grace -= 1
        if self.grace % 8 == 1:
            self.draw_triangle(screen)
            self.draw_body(screen)

    def is_in_grace(self):
        return self.grace > 1

    def has_children(self):
        return self.size > 8

    def hit(self):
        dx = -1 if random.randint(0, 1) == 0 else 1
        dy = -1 if random.randint(0, 1) == 0 else 1
        b1 = Bubble(dx, dy, (self.max_x, self.max_y), self.x, self.y, int(self.size * .6))
        b2 = Bubble(dx*-1, dy*-1, (self.max_x, self.max_y), self.x, self.y, int(self.size * .6))
        return b1, b2


class BubbleFactory:
    @staticmethod
    def create_random(max_xy):
        dx = -1 if random.randint(0, 1) == 0 else 1
        dy = -1 if random.randint(0, 1) == 0 else 1
        x = random.randint(0, max_xy[0])
        y = random.randint(0, max_xy[1])
        return Bubble(dx, dy, max_xy, x, y, 96)
