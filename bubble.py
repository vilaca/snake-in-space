import random
import pygame


class Bubble:
    def __init__(self, dx, dy, max_xy, x, y, size=64):
        self.dx = dx
        self.dy = dy
        self.size = size
        self.max_x = max_xy[0]
        self.max_y = max_xy[1]
        self.x = x
        self.y = y
        self.grace = 121

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > self.max_x:
            self.dx *= -1
        if self.y < 0 or self.y > self.max_y:
            self.dy *= -1

    def draw(self, bg):
        if self.grace > 1:
            self.grace -= 1
        if self.grace & 1:
            pygame.draw.circle(bg, (255, 255, 64), (self.x, self.y), int(self.size), 1)
            pygame.draw.circle(bg, (0, 0, 255), (self.x, self.y), int(self.size) - 1, 1)
        if self.x % 64 == 0:
            pygame.draw.circle(bg, (255, 0, 0), (self.x, self.y), int(self.size) - 2)
        elif self.y % 64 == 0:
            pygame.draw.circle(bg, (255, 255, 0), (self.x, self.y), int(self.size) - 2)
        else:
            pygame.draw.circle(bg, (0, 0, 0), (self.x, self.y), int(self.size) - 2)

    def is_in_grace(self):
        return self.grace > 1

    def has_children(self):
        return self.size > 8

    def hit(self):
        dx = -1 if random.randint(0, 1) == 0 else 1
        dy = -1 if random.randint(0, 1) == 0 else 1
        b1 = Bubble(dx, dy, (self.max_x, self.max_y), self.x, self.y, int(self.size / 2))
        b2 = Bubble(dx*-1, dy*-1, (self.max_x, self.max_y), self.x, self.y, int(self.size / 2))
        return b1, b2


class BubbleFactory:
    @staticmethod
    def create_random(max_xy):
        dx = -1 if random.randint(0, 1) == 0 else 1
        dy = -1 if random.randint(0, 1) == 0 else 1
        x = random.randint(0, max_xy[0])
        y = random.randint(0, max_xy[1])
        return Bubble(dx, dy, max_xy, x, y)
