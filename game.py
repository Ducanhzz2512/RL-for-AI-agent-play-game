from config import GameConfig
from pipe import Pipe


class Game:
    def __init__(self):
        self.pipes = []
        self.frame = 0
        self.create_initial_pipes()

    def create_initial_pipes(self):
        self.pipes.append(Pipe(GameConfig.WIDTH + 100))
        self.pipes.append(
            Pipe(GameConfig.WIDTH + 100 + GameConfig.PIPE_DISTANCE)
        )

    def update_pipes(self):
        for pipe in self.pipes:
            pipe.update()

        self.pipes = [
            pipe for pipe in self.pipes
            if not pipe.is_off_screen()
        ]

        if len(self.pipes) > 0:
            last_pipe = self.pipes[-1]
            if last_pipe.x < GameConfig.WIDTH - GameConfig.PIPE_DISTANCE:
                self.pipes.append(Pipe(GameConfig.WIDTH))

    def get_next_pipe(self, bird):
        valid_pipes = [
            pipe for pipe in self.pipes
            if pipe.x + GameConfig.PIPE_WIDTH >= bird.x
        ]

        if valid_pipes:
            return valid_pipes[0]

        if self.pipes:
            return self.pipes[-1]

        # Fallback: không còn ống nào (hiếm), tạo ống mới
        new_pipe = Pipe(GameConfig.WIDTH)
        self.pipes.append(new_pipe)
        return new_pipe

    def update_birds(self, birds):
        for bird in birds:
            if not bird.alive:
                continue

            next_pipe = self.get_next_pipe(bird)
            bird.think(next_pipe)
            bird.update()

            for pipe in self.pipes:
                bird.check_pipe_collision(pipe)
                bird.check_pipe_passed(pipe)

        self.update_pipes()
        self.frame += 1

    def all_birds_dead(self, birds):
        return not any(bird.alive for bird in birds)
