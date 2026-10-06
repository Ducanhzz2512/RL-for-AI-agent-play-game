import pygame

from config import GameConfig


class Bird:
    def __init__(self, brain):
        self.x = GameConfig.BIRD_X
        self.y = GameConfig.HEIGHT / 2
        self.velocity = 0
        self.brain = brain
        self.alive = True
        self.frames_alive = 0
        self.pipes_passed = 0
        self.passed_pipes = set()

    @property
    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            GameConfig.BIRD_SIZE,
            GameConfig.BIRD_SIZE
        )

    def jump(self):
        self.velocity = GameConfig.JUMP_STRENGTH

    def update(self):
        if not self.alive:
            return

        self.velocity += GameConfig.GRAVITY
        self.y += self.velocity
        self.frames_alive += 1

        if self.y < 0:
            self.alive = False

        if self.y + GameConfig.BIRD_SIZE > GameConfig.HEIGHT:
            self.alive = False

    def think(self, pipe):
        if not self.alive:
            return

        vertical_velocity = self.velocity / 10
        horizontal_distance = (pipe.x - self.x) / GameConfig.WIDTH
        top_distance = (pipe.gap_y - self.y) / GameConfig.HEIGHT
        bottom_distance = (
            pipe.gap_y + GameConfig.PIPE_GAP - self.y
        ) / GameConfig.HEIGHT

        inputs = [
            vertical_velocity,
            horizontal_distance,
            top_distance,
            bottom_distance
        ]

        if self.brain.should_jump(inputs):
            self.jump()

    def check_pipe_collision(self, pipe):
        if not self.alive:
            return

        if self.rect.colliderect(pipe.top_rect):
            self.alive = False

        if self.rect.colliderect(pipe.bottom_rect):
            self.alive = False

    def check_pipe_passed(self, pipe):
        if pipe in self.passed_pipes:
            return

        if pipe.x + GameConfig.PIPE_WIDTH < self.x:
            self.pipes_passed += 1
            self.passed_pipes.add(pipe)
