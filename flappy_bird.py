"""Xem AI đang chơi (có giao diện pygame)."""
import argparse
import os
import pygame

from config import GameConfig, TrainingConfig
from genetic import GeneticAlgorithm
from neural_network import NeuralNetwork
from bird import Bird
from game import Game


def create_population():
    birds = []
    for _ in range(TrainingConfig.POPULATION_SIZE):
        brain = NeuralNetwork()
        bird = Bird(brain=brain)
        birds.append(bird)
    return birds


def draw_game(screen, birds, game, generation,
                best_time_ever, best_score_ever,
                selection_method="tournament"):
    screen.fill((135, 206, 235))

    for pipe in game.pipes:
        pygame.draw.rect(screen, (0, 180, 0), pipe.top_rect)
        pygame.draw.rect(screen, (0, 180, 0), pipe.bottom_rect)

    for bird in birds:
        if bird.alive:
            pygame.draw.rect(screen, (255, 255, 0), bird.rect)

    font = pygame.font.SysFont("Arial", 22)

    alive = sum(bird.alive for bird in birds)
    current_time = max(bird.frames_alive for bird in birds)
    current_score = max(bird.pipes_passed for bird in birds)

    lines = [
        f"[{selection_method}] Gen: {generation}  Alive: {alive}",
        f"Time: {current_time} (Best: {best_time_ever})",
        f"Score: {current_score} (Best: {best_score_ever})",
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (10, 10 + i * 28))
    pygame.display.flip()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--selection", choices=["tournament", "roulette"],
                   default=TrainingConfig.SELECTION_METHOD)
    p.add_argument("--pos", default=None,
                   help='Window position, e.g. "50,100"')
    return p.parse_args()


def main():
    args = parse_args()
    if args.pos:
        # Phải set trước pygame.init() mới có tác dụng
        os.environ["SDL_VIDEO_WINDOW_POS"] = args.pos
    pygame.init()
    screen = pygame.display.set_mode(
        (GameConfig.WIDTH, GameConfig.HEIGHT)
    )
    pygame.display.set_caption(
        f"Flappy Bird - {args.selection}"
    )
    clock = pygame.time.Clock()

    ga = GeneticAlgorithm(selection_method=args.selection)
    generation = 1
    birds = create_population()
    game = Game()

    best_time_ever = 0
    best_score_ever = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if game.all_birds_dead(birds):
            gen_best_time = max(b.frames_alive for b in birds)
            gen_best_score = max(b.pipes_passed for b in birds)

            if gen_best_time > best_time_ever:
                best_time_ever = gen_best_time
            if gen_best_score > best_score_ever:
                best_score_ever = gen_best_score

            print(
                f"[{args.selection}] Gen: {generation} | "
                f"Time: {gen_best_time} | Score: {gen_best_score} | "
                f"Best Time Ever: {best_time_ever} | "
                f"Best Score Ever: {best_score_ever}"
            )

            birds = ga.create_next_generation(birds)
            generation += 1
            game = Game()
        else:
            game.update_birds(birds)

        # Cập nhật best-ever live để hiển thị kịp thời
        live_best_time = max(b.frames_alive for b in birds)
        live_best_score = max(b.pipes_passed for b in birds)
        draw_best_time = max(best_time_ever, live_best_time)
        draw_best_score = max(best_score_ever, live_best_score)

        draw_game(
            screen, birds, game, generation,
            draw_best_time, draw_best_score,
            selection_method=args.selection
        )
        clock.tick(GameConfig.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
