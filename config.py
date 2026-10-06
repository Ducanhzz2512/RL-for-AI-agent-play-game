class GameConfig:
    WIDTH = 800
    HEIGHT = 600
    FPS = 60

    BIRD_X = 100
    BIRD_SIZE = 30

    GRAVITY = 0.5
    JUMP_STRENGTH = -8

    PIPE_WIDTH = 80
    PIPE_GAP = 180
    PIPE_SPEED = 4
    PIPE_DISTANCE = 300


class TrainingConfig:
    POPULATION_SIZE = 200
    GENERATIONS = 1000
    TOURNAMENT_SIZE = 3
    SELECTION_METHOD = "tournament"  # "tournament" hoặc "roulette"
    MUTATION_RATE = 0.1
    MUTATION_AMOUNT = 0.15
    ELITISM = True
    MAX_FRAMES = 10000
