from Matrix import Matrix
import numpy as np

def Sigmoid(weightedInput: float) -> float:
    '''The sigmoid function to map the weighted value between 1 and 0'''
    return 1/(1 + np.exp(-weightedInput))

def dSigmoid(sigVal: float) -> float:
    """The derivative of the sigmoid function"""
    return sigVal * (1 - sigVal)

class NeuralNetwork:
    """This class represents the neural network making use of a matrix to store the weights of each layer"""
    def __init__(self, inputs: int, hidden: int, outputs: int):
        self.inputs = inputs
        self.hidden = hidden
        self.outputs = outputs

        self.weights_ih = Matrix(self.hidden, self.inputs) # Weights Between input layer and hidden layer
        self.weights_ho = Matrix(self.outputs, self.hidden) # Weights between hidden layer and output layer

        self.weights_ih.randomize()
        self.weights_ho.randomize()

        self.bias_h = Matrix(self.hidden, 1) # biases for hidden layer
        self.bias_o = Matrix(self.outputs, 1) # biases for output layer
        self.bias_h.randomize()
        self.bias_o.randomize()
        self.alpha = 0.1 # Learning Rate

    def feedForward(self, input: list):
        """This is the inference method. Once the network is trained, this method should yield the predictions"""
        inputs = Matrix.fromArray(input)

        hidden = Matrix.multiply(self.weights_ih, inputs)
        hidden.add(self.bias_h)
        hidden.map(Sigmoid)

        output = Matrix.multiply(self.weights_ho, hidden)
        output.add(self.bias_o)
        output.map(Sigmoid)

        return Matrix.toArray(output)
    
    def train(self, inputs, targets):
        """This is where backpropagation is performed to adapt the weights """
        inputs = Matrix.fromArray(inputs)

        hidden = Matrix.multiply(self.weights_ih, inputs)
        hidden.add(self.bias_h)
        hidden.map(Sigmoid)

        output = Matrix.multiply(self.weights_ho, hidden)
        output.add(self.bias_o)
        output.map(Sigmoid)
    
        targets = Matrix.fromArray(targets)

        o_error = Matrix.Subtract(targets, output)
        output.map(dSigmoid)
        gradients = output.map(dSigmoid, output)
        gradients.elemMultiply(o_error)
        gradients.scale(self.alpha)
        
        hidden_t = hidden.transpose(hidden)
        who_deltas = Matrix.multiply(gradients, hidden_t)

        # make the adjustments
        self.weights_ho.add(who_deltas)
        self.bias_o.add(gradients)


        who_tr = self.weights_ho.transpose(self.weights_ho)
        h_error = Matrix.multiply(who_tr, o_error)

        hidden_gradients = hidden.map(dSigmoid, hidden)
        hidden_gradients.elemMultiply(h_error)
        hidden_gradients.scale(self.alpha)

        inputs_t = inputs.transpose(inputs)
        wih_eltas = Matrix.multiply(hidden_gradients, inputs_t)

        self.weights_ih.add(wih_eltas)
        self.bias_h.add(hidden_gradients)

         