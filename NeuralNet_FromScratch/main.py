from NeuralNet import NeuralNetwork
from random import randint

"""The network for the XOR operation needs 2 inputs and one output. """
nn = NeuralNetwork(2, 2, 1) 
inputs = [[0, 0], [1, 0], [1, 1], [0, 1]]
targets = [[0], [1], [0], [1]]

# Run training
for epoch in range(100000):
    i = randint(0, 3)
    nn.train(inputs[i], targets[i])

# Perform inference
print(f"[0, 0]: {nn.feedForward([0, 0])}")
print(f"[1, 0]: {nn.feedForward([1, 0])}")
print(f"[1, 1]: {nn.feedForward([1, 1])}")
print(f"[0, 1]: {nn.feedForward([0, 1])}")