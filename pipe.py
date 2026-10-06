import random
import pygame

from config import GameConfig


class Pipe:
    def __init__(self, x):
        self.x = x
        margin = 100
        self.gap_y = random.randint(
            margin,
            GameConfig.HEIGHT - GameConfig.PIPE_GAP - margin
        )

    @property
    def top_rect(self):
        return pygame.Rect(
            self.x,
            0,
            GameConfig.PIPE_WIDTH,
            self.gap_y
        )

    @property
    def bottom_rect(self):
        return pygame.Rect(
            self.x,
            self.gap_y + GameConfig.PIPE_GAP,
            GameConfig.PIPE_WIDTH,
            GameConfig.HEIGHT
        )

    def update(self):
        self.x -= GameConfig.PIPE_SPEED

    def is_off_screen(self):
        return self.x + GameConfig.PIPE_WIDTH < 0
