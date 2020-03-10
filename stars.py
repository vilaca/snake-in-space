
import pygame
import random


class StarsLayer:

    def __init__(self, w, color, spd, size, count=50):
        self.size = size
        self.spd = spd
        self.max_x = w[0]
        self.color = color
        self.stars = []
        for i in range(count):
            x = random.randint(0, w[0])
            y = random.randint(0, w[1])
            self.stars.append((x, y))
        self.travelled = 0

    def draw(self, background):
        for star in self.stars:
            p = (int(star[0] - self.travelled) % self.max_x, star[1])
            if self.size > 4:
                c = (0, 0, 128)
                pygame.draw.circle(background, c, p, self.size, 2)
                pygame.draw.circle(background, self.color, p, self.size-2)
            else:
                pygame.draw.circle(background, self.color, p, self.size)

    def update(self):
        self.travelled += self.spd
