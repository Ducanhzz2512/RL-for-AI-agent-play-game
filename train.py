"""Train GA không giao diện, chạy nhanh."""
import argparse
from genetic import GeneticAlgorithm
from bird import Bird
from neural_network import NeuralNetwork
from game import Game
from config import TrainingConfig


def create_population():
    birds = []
    for _ in range(TrainingConfig.POPULATION_SIZE):
        brain = NeuralNetwork()
        bird = Bird(brain=brain)
        birds.append(bird)
    return birds


def train(selection_method=None):
    ga = GeneticAlgorithm(selection_method=selection_method)
    tag = ga.selection_method
    best_time_ever = 0
    best_score_ever = 0

    # FIX BUG quan trọng: population phải tạo 1 lần ngoài vòng lặp,
    # nếu tạo lại mỗi generation thì tiến hóa bị reset.
    birds = create_population()

    for generation in range(1, TrainingConfig.GENERATIONS + 1):
        game = Game()

        while not game.all_birds_dead(birds):
            if game.frame >= TrainingConfig.MAX_FRAMES:
                break
            game.update_birds(birds)

        # Best theo fitness = thời gian tồn tại
        current_best = max(birds, key=lambda b: ga.calculate_fitness(b))
        time_alive = current_best.frames_alive
        # Score = số cột đã qua (tính riêng, có thể thuộc con chim khác)
        gen_best_score = max(b.pipes_passed for b in birds)

        if time_alive > best_time_ever:
            best_time_ever = time_alive

        if gen_best_score > best_score_ever:
            best_score_ever = gen_best_score

        print(
            f"[{tag}] Gen: {generation:4d} | "
            f"Time: {time_alive:5d} | "
            f"Score: {gen_best_score:3d} | "
            f"Best Time Ever: {best_time_ever:5d} | "
            f"Best Score Ever: {best_score_ever:3d}"
        )

        birds = ga.create_next_generation(birds)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selection", choices=["tournament", "roulette"],
                    default=TrainingConfig.SELECTION_METHOD)
    train(selection_method=ap.parse_args().selection)
