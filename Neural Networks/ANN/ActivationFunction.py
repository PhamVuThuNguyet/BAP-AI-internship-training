import numpy as np


class ActivationFunction:
    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def tanh(z):
        return np.tanh(z)

    @staticmethod
    def relu(z):
        return max(0.0, z)

    @staticmethod
    def leaky_relu(z):
        if z > 0:
            return z
        else:
            return 0.01 * z

    @staticmethod
    def softmax(z):
        exp = np.exp(z - z.max())
        return np.divide(exp, np.sum(exp, axis=0))

    def derivative_sigmoid(self, z):
        sigmoid = self.sigmoid(z)
        return sigmoid * (1 - sigmoid)

    def derivative_tanh(self, z):
        tanh = self.tanh(z)
        return 1 - pow(tanh, 2)

    @staticmethod
    def derivative_relu(z):
        if z >= 0:
            return 1
        else:
            return 0

    @staticmethod
    def derivative_leaky_relu(z):
        if z >= 0:
            return 1
        else:
            return 0.01

    def derivative_softmax(self, z):
        softmax = self.softmax(z)
        return softmax * (1 - softmax)
