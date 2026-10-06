import random
import math


class NeuralNetwork:
    INPUT_SIZE = 4
    HIDDEN_SIZE = 4
    OUTPUT_SIZE = 1

    GENOME_SIZE = (
        INPUT_SIZE * HIDDEN_SIZE
        + HIDDEN_SIZE
        + HIDDEN_SIZE * OUTPUT_SIZE
        + OUTPUT_SIZE
    )  # = 25

    def __init__(self, genome=None):
        if genome is None:
            self.genome = [
                random.uniform(-1, 1)
                for _ in range(self.GENOME_SIZE)
            ]
        else:
            self.genome = genome.copy()

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-max(-60, min(60, x))))

    def tanh(self, x):
        return math.tanh(x)

    def predict(self, inputs):
        index = 0
        hidden = []

        for _ in range(self.HIDDEN_SIZE):
            value = 0
            for i in range(self.INPUT_SIZE):
                value += inputs[i] * self.genome[index]
                index += 1

            value += self.genome[index]
            index += 1

            hidden.append(self.tanh(value))

        output = 0
        for i in range(self.HIDDEN_SIZE):
            output += hidden[i] * self.genome[index]
            index += 1

        output += self.genome[index]

        return self.sigmoid(output)

    def should_jump(self, inputs):
        return self.predict(inputs) > 0.5
