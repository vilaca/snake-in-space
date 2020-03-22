
import random
import pygame
import sys
import time

from pygame.locals import *

import player
import snake
import sky


def quit_requested(event):
    return event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE


def pause_requested(event):
    return event.type == pygame.KEYDOWN and event.key == pygame.K_p


def pause_cancel_requested(event):
    return event.type == pygame.KEYDOWN and event.key == pygame.K_p


def listen_keys(p1, paused):
    for event in pygame.event.get():
        if quit_requested(event):
            pygame.quit()
            sys.exit()
        if not paused:
            if pause_requested(event):
                paused = True
                time.sleep(1)
                continue
            p1.input(event)
        else:
            if pause_cancel_requested(event):
                paused = False
                continue
    return paused


def main():
    pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
    pygame.init()  # turn all of pygame on.
    screen_dim = (1360, 768)
    display = pygame.display.set_mode(screen_dim, FULLSCREEN | HWSURFACE if not sys.gettrace() else HWSURFACE)
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    uc = snake.Snake(screen_dim[0]/3, screen_dim[1]/2, screen_dim[0], screen_dim[1])
    clock = pygame.time.Clock()
    scene = sky.Sky(screen_dim)
    p1 = player.Player()
    paused = False

    import os
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print("__location__")
    print(__location__)
    print("__location__")

    pygame.mixer.init()
    kick = pygame.mixer.Sound(__location__+"\\samples\\kick.wav")
    kick808 = pygame.mixer.Sound(__location__+"\\samples\\kick_808.wav")
    clap = pygame.mixer.Sound(__location__+"\\samples\\clap.wav")
    hh = pygame.mixer.Sound(__location__+"\\samples\\hh.wav")
    chip = pygame.mixer.Sound(__location__+"\\samples\\perc.wav")

    seq = 0
    micro_seq = 0
    while True:
        paused = listen_keys(p1, paused)
        if paused:
            continue

        if len(scene.enemies) < 50 and random.randint(0, 160) == 0:
            scene.inc_enemies()

        if len(scene.bubbles) == 0 and random.randint(0, 160) == 0:
            scene.inc_bubbles()

        surface = pygame.Surface(screen_dim)

        if p1.turning_left():
            uc.go_left()
        if p1.turning_right():
            uc.go_right()
        if p1.firing():
            uc.fire()
        else:
            uc.stop_firing()

        scene.update(uc.x, uc.y)

        if scene.check_hit(uc):
            uc.hit()

        if scene.check_fed(uc):
            uc.fed()

        scene.draw_background(surface)

        if p1.firing():
            line_start, line_end = uc.draw(surface)
            scene.check_targets(line_start, line_end)
        else:
            uc.draw(surface)

        scene.draw_foreground(surface)

        display.blit(surface, (0, 0))
        pygame.display.flip()

        clock.tick(75)

        if micro_seq % 20 == 0:
            if seq % 16 == 0:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(kick808)
            if seq % 16 == 0 or seq % 16 == 2 or seq % 16 == 11:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(kick)
            if seq % 16 == 6 or seq % 16 == 8 or seq % 16 == 14:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(hh)
            if seq % 16 == 4 or seq % 16 == 10 or seq % 16 == 14:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(chip)
            if seq % 16 == 4 or seq % 16 == 12:
                pygame.mixer.Sound.play(clap)
                pygame.mixer.music.stop()
            seq += 1
        micro_seq += 1

main()
