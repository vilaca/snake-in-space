
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
        pygame.draw.circle(background, (255, 255, 255), (self.x, self.y), self.size, int(self.size/32))
        pygame.draw.circle(background, (255, 255, 0), (self.x, self.y), self.size - int(self.size/32), int(self.size/16))
        pygame.draw.circle(background, (255, 0, 0), (self.x, self.y), self.size - int(self.size/32)-int(self.size/16), int(self.size/12))
