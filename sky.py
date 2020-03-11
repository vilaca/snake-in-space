
import math
import random
from shapely.geometry import LineString
from shapely.geometry import Point

import bubble
from explosion import ExplosionFactory
from foe import Foe
from food import FoodFactory
from stars import StarsLayer


class Sky:
    def __init__(self, screen_dim):
        self.screen_dim = screen_dim
        self.background = [
            StarsLayer(screen_dim, (100, 100, 105), 1, 3),
            StarsLayer(screen_dim, (80, 80, 120), .5, 2),
            StarsLayer(screen_dim, (55, 55, 55), .25, 1)
        ]
        self.foreground = [
            StarsLayer(screen_dim, (255, 255, 255), 1.5, 4, 22),
            StarsLayer(screen_dim, (255, 255, 255), 6, 8, 7)
        ]
        self.enemies = [
            Foe(screen_dim), Foe(screen_dim)
        ]
        self.exploding = []
        self.bubbles = [
            bubble.BubbleFactory().create_random(screen_dim)
        ]
        self.food = []

    def update(self):
        list(map(lambda s: s.update(), self.background + self.foreground))
        list(map(lambda en: en.update(), self.enemies))
        list(map(lambda en: en.update(), self.food))
        list(map(lambda en: en.update(), self.bubbles))
        self.exploding = [e for e in self.exploding if not e.update()]

    def draw_background(self, surface):
        list(map(lambda s: s.draw(surface), self.background))
        list(map(lambda e: e.draw(surface), self.exploding))

    def draw_foreground(self, surface):
        list(map(lambda en: en.draw(surface), self.food))
        list(map(lambda en: en.draw(surface), self.enemies))
        list(map(lambda en: en.draw(surface), self.bubbles))
        list(map(lambda s: s.draw(surface), self.foreground))

    def check_targets(self, line_start, line_end):
        line = LineString([(line_start[0], line_start[1]), (line_end[0], line_end[1])])
        for e in reversed(self.enemies):
            p = Point(e.x % self.screen_dim[0], e.y)
            circle = p.buffer(e.size).boundary
            hit = circle.intersection(line)
            if not hit.is_empty:
                self.enemies.remove(e)
                self.exploding.insert(0, ExplosionFactory.create_explosion(e.x, e.y))
        for e in reversed(self.food):
            if e.is_in_grace():
                continue
            p = Point(e.x % self.screen_dim[0], e.y)
            circle = p.buffer(e.size).boundary
            hit = circle.intersection(line)
            if not hit.is_empty:
                self.food.remove(e)
                self.exploding.insert(0, ExplosionFactory.create_food_explosion(e.x, e.y))
        for e in reversed(self.bubbles):
            if e.is_in_grace():
                continue
            p = Point(e.x % self.screen_dim[0], e.y)
            circle = p.buffer(e.size).boundary
            hit = circle.intersection(line)
            if not hit.is_empty:
                if e.has_children():
                    n1, n2 = e.hit()
                    explode = False
                    explode2 = False

                    if random.randint(0, 1) == 0:
                        self.food.append(FoodFactory.create(self.screen_dim, n1))
                    elif random.randint(0, 1) == 0:
                        self.bubbles.append(n1)
                    else:
                        explode = True

                    if random.randint(0, 1) == 0:
                        self.food.append(FoodFactory.create(self.screen_dim, n2))
                    elif random.randint(0, 1) == 0:
                        self.bubbles.append(n2)
                    else:
                        explode2 = True

                    if explode and explode2:
                        self.exploding.insert(0, ExplosionFactory.create_blue_explosion(e.x, e.y))
                else:
                    self.exploding.insert(0, ExplosionFactory.create_blue_explosion(e.x, e.y))
                self.bubbles.remove(e)

    def inc_enemies(self):
        self.enemies.append(Foe(self.screen_dim))

    def inc_bubbles(self):
        self.bubbles.append(bubble.BubbleFactory.create_random(self.screen_dim))

    def check_hit(self, p1):
        for e in self.enemies:
            d = math.sqrt((p1.x-e.x)**2+(p1.y-e.y)**2)
            if d < e.size + p1.size:
                return True
            if len(p1.tail) == 0:
                continue
            n = 1
            inc = p1.size / len(p1.tail)
            for seg in p1.tail:
                d = math.sqrt((seg[0] - e.x) ** 2 + (seg[1] - e.y) ** 2)
                if d < e.size + n*2:
                    return True
                n += inc
        return False

    def check_fed(self, p1):
        for e in reversed(self.food):
            d = math.sqrt((p1.x-e.x)**2+(p1.y-e.y)**2)
            if d < e.size + p1.size:
                self.food.remove(e)
                return True
        return False

