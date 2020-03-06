
import pygame
import math

head_colour = (0, 180, 0)
outside_colour = (50, 210, 50)
white_colour = (255, 255, 255)
black_colour = (0, 0, 0)
red_colour = (255, 0, 0)
flash_colour = (0, 0, 255)


class Snake:

    def __init__(self, x, y, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.x = x
        self.y = y
        self.rotation = math.pi/2
        self.px, self.py = self.calc()
        self.fire_on = False
        self.tail = []
        self.over_heating = 0
        self.tick = False
        self.size = 20
        self.is_hit = False
        self.max_tail = 8

    def overheating_flash(self, tick, no_tick, normal):
        if self.over_heating != 255:
            return normal
        if self.tick:
            return tick
        return no_tick

    def draw(self, background):
        self.px, self.py = self.calc()

        def move():
            self.x += math.cos(self.rotation + math.pi / 2 + math.pi) * 5
            self.y += math.sin(self.rotation + math.pi / 2 + math.pi) * 5
            if self.x < 0:
                self.x = self.max_x
            elif self.x > self.max_x:
                self.x = 0
            if self.y < 0:
                self.y = self.max_y
            elif self.y > self.max_y:
                self.y = 0
            if len(self.tail) > self.max_tail:
                self.tail.pop(0)
            self.tail.append((int(self.x), int(self.y)))

        def draw_tail():
            colour = self.overheating_flash(flash_colour, white_colour, head_colour)
            n = 1
            inc = self.size / len(self.tail) / 2
            for seg in self.tail:
                pygame.draw.circle(background, outside_colour, (seg[0], seg[1]), int(n*2), 1)
                pygame.draw.circle(background, colour, (seg[0], seg[1]), int(n))
                n += inc

        def snake_heating_fx():
            if self.fire_on:
                self.over_heating += 1
                if self.over_heating > 255:
                    self.over_heating = 255
            else:
                self.over_heating = 0

        def draw_head():
            pygame.draw.circle(background, (0, 255, 0), (int(self.x), int(self.y)), self.size)
            eye_x = math.cos(self.rotation + math.pi * 1.12) * (18 + self.over_heating / 14)
            eye_y = math.sin(self.rotation + math.pi * 1.12) * (18 + self.over_heating / 14)
            extra = int(self.over_heating / 48)
            pygame.draw.circle(background, head_colour, (int(self.x + eye_x), int(self.y + eye_y)), 10 + extra, 5)
            c = self.overheating_flash(red_colour, white_colour, white_colour)
            pygame.draw.circle(background, c, (int(self.x + eye_x), int(self.y + eye_y)), 5 + extra)
            px2, py2 = self.calc(-math.pi / 2)
            pygame.draw.line(background, black_colour, (self.x, self.y), (self.x + px2, self.y + py2), 5)

        self.tick = not self.tick
        move()
        if self.tick and self.is_hit and not self.fire_on:
            return
        draw_tail()
        snake_heating_fx()
        draw_head()

        if self.fire_on:
            x = math.cos(self.rotation + math.pi / 2 + math.pi) * 2000
            y = math.sin(self.rotation + math.pi / 2 + math.pi) * 2000
            c = self.overheating_flash(white_colour, flash_colour, white_colour)
            pygame.draw.line(background, c, (self.x, self.y), (self.x + x, self.y + y), 1 + int(self.over_heating / 8))
            return (self.x, self.y), (self.x + x, self.y + y)

    def calc(self, rot=0):
        return math.cos(self.rotation + rot) * 30, math.sin(self.rotation + rot) * 30

    def go_left(self):
        self.rotation -= math.pi / (32 if not self.fire_on else 96 + self.over_heating / 3)

    def go_right(self):
        self.rotation += math.pi / (32 if not self.fire_on else 96 + self.over_heating / 3)

    def fire(self):
        self.fire_on = True

    def stop_firing(self):
        self.fire_on = False

    def hit(self, v):
        self.is_hit = v

    def fed(self):
        self.max_tail += 4
