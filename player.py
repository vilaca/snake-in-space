
import pygame


class Player:
    __LEFT_TURN = 1
    __RIGHT_TURN = 2
    __FORWARD = 3

    def __init__(self):
        self.__direction = self.__FORWARD
        self.__left_pressed = False
        self.__right_pressed = False
        self.__fire = False

    def turning_left(self):
        return self.__direction == self.__LEFT_TURN

    def turning_right(self):
        return self.__direction == self.__RIGHT_TURN

    def firing(self):
        return self.__fire

    def input(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.__fire = True
            elif event.key == pygame.K_LEFT:
                self.__left_pressed = True
                self.__direction = self.__LEFT_TURN
            elif event.key == pygame.K_RIGHT:
                self.__right_pressed = True
                self.__direction = self.__RIGHT_TURN

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.__left_pressed = False
                self.__direction = self.__RIGHT_TURN if self.__right_pressed else self.__FORWARD

            elif event.key == pygame.K_RIGHT:
                self.__right_pressed = False
                self.__direction = self.__LEFT_TURN if self.__left_pressed else self.__FORWARD

            elif event.key == pygame.K_SPACE:
                self.__fire = False
