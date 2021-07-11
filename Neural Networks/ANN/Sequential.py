import numpy as np
from ActivationFunction import *


class Sequential:
    def __init__(self):
        # architecture
        self.__no_input = 0
        self.__L = 0
        self.__model_architect = []

        # forward propagation
        self.__weight_matrix = []
        self.__bias_matrix = []
        self.__z = []
        self.__a = []

        # back propagation
        self.__derivative_weight_matrix = []
        self.__derivative_bias_matrix = []
        self.__derivative_a = []
        self.__derivative_z = []

    def __initialize_parameters(self, no_unit_last_layer: int, no_unit_new_layer: int):
        """
        initial parameters for recently added layer
        :param no_unit_last_layer: number of nodes of the last layer
        :type no_unit_last_layer: int
        :param no_unit_new_layer: number of nodes of the recently added layer
        :type no_unit_new_layer: int
        :return: None
        :rtype:
        """
        np.random.seed(1)
        # feed forward
        self.__weight_matrix.append(np.random.rand(no_unit_new_layer, no_unit_last_layer))
        self.__bias_matrix.append(np.zeros((1, no_unit_new_layer)))
        self.__a.append(np.zeros((1, no_unit_new_layer)))
        self.__z.append(np.zeros((1, no_unit_new_layer)))

        # back_prop
        self.__derivative_weight_matrix.append(np.zeros((no_unit_new_layer, no_unit_last_layer)))
        self.__derivative_bias_matrix.append(np.zeros((1, no_unit_new_layer)))
        self.__derivative_a.append(np.zeros((1, no_unit_new_layer)))
        self.__derivative_z.append(np.zeros((1, no_unit_new_layer)))

    def add(self, layer_name: str, no_unit: int, activation: str = None):
        """
        add layer to network model
        :param layer_name: name of layer, you can use "input", "hidden", "dense", "output"
        :type layer_name: string
        :param no_unit: number of nodes of this layer
        :type no_unit: int
        :param activation: activation function apply to this layer
        :type activation: string
        :return: None
        :rtype:
        """
        if layer_name == 'input':
            self.__no_input = no_unit
            self.__initialize_parameters(0, 0)
        elif self.__L == 1:
            self.__initialize_parameters(self.__no_input, no_unit)
        else:
            self.__initialize_parameters(self.__weight_matrix[-1].shape[0], no_unit)
        layer_name = "Layer " + str(self.__L) + "/Name: " + layer_name + "/Nodes: " + str(no_unit) + \
                     "/Activation: " + str(activation)
        self.__model_architect.append((layer_name, activation))
        self.__L += 1

    @staticmethod
    def __neural_activate(weights: np.ndarray, bias: np.ndarray, inp: np.ndarray):
        """
        linear activation in each neural
        :param weights:
        :type weights:
        :param bias:
        :type bias:
        :param inp:
        :type inp:
        :return:
        :rtype: np.ndarray
        """
        z = (inp @ weights.T) + bias
        return z

    def __forward_propagation(self, x_train: np.ndarray):
        """
        Function for feed forward phase
        :param x_train: input of training set
        :type x_train: np.ndarray
        :return: predicted output
        :rtype: np.ndarray
        """
        self.__a[0] = x_train
        activation_fnc = None
        for layer in range(1, self.__L):
            activation = self.__model_architect[layer][1]
            if activation == 'sigmoid':
                activation_fnc = ActivationFunction().sigmoid
            elif activation == 'tanh':
                activation_fnc = ActivationFunction().tanh
            elif activation == 'relu':
                activation_fnc = ActivationFunction().relu
            elif activation == 'leaky_relu':
                activation_fnc = ActivationFunction().leaky_relu
            elif activation == 'softmax':
                activation_fnc = ActivationFunction().softmax

            self.__z[layer] = self.__neural_activate(self.__weight_matrix[layer], self.__bias_matrix[layer],
                                                     self.__a[layer - 1])
            self.__a[layer] = activation_fnc(self.__z[layer])

        return self.__a[-1]

    def __backpropagation(self, y_train: np.ndarray, y_pred: np.ndarray):
        """
        Function for back propagation phase
        :param y_train: output of training set
        :type y_train: np.ndarray
        :param y_pred: predicted output from feed forward phase
        :type y_pred: np.ndarray
        :return: None
        :rtype:
        """
        m = y_train.shape[0]
        self.__derivative_z[-1] = y_pred - y_train
        activation_func = None
        for layer in reversed(range(1, self.__L)):

            activation = self.__model_architect[layer][1]
            if activation == 'sigmoid':
                activation_func = ActivationFunction().derivative_sigmoid
            elif activation == 'tanh':
                activation_func = ActivationFunction().derivative_tanh
            elif activation == 'relu':
                activation_func = ActivationFunction().derivative_relu
            elif activation == 'leaky_relu':
                activation_func = ActivationFunction().derivative_leaky_relu
            elif activation == 'softmax':
                activation_func = ActivationFunction().derivative_softmax
            self.__derivative_weight_matrix[layer] = (self.__derivative_z[layer].T @ self.__a[layer - 1]) / m
            self.__derivative_bias_matrix[layer] = np.sum(self.__derivative_z[layer], axis=0) / m
            if layer > 1:
                self.__derivative_a[layer - 1] = self.__derivative_z[layer] @ self.__weight_matrix[layer]
                self.__derivative_z[layer - 1] = np.multiply(self.__derivative_a[layer - 1],
                                                             activation_func(self.__z[layer - 1]))

    def __update_params(self, learning_rate: float):
        """
        update weights and bias
        :param learning_rate: learning rate
        :type learning_rate: float
        :return: None
        :rtype:
        """
        for layer in range(1, self.__L):
            self.__weight_matrix[layer] -= learning_rate * self.__weight_matrix[layer]
            self.__bias_matrix[layer] -= learning_rate * self.__bias_matrix[layer]

    def fit(self, x_train: np.ndarray, y_train: np.ndarray, epochs: int = 100, learning_rate: float = 0.01):
        """
        training model
        :param x_train: input of training set
        :type x_train: np.ndarray
        :param y_train: output of training set
        :type y_train: np.ndarray
        :param epochs: number of iterator
        :type epochs: int
        :param learning_rate: learning rate
        :type learning_rate: float
        :return: None
        :rtype:
        """
        for i in range(epochs):
            output = self.__forward_propagation(x_train)
            loss = self.__get_loss(y_train, output)
            print("epoch", i, "loss:", loss)
            self.__backpropagation(y_train, output)
            self.__update_params(learning_rate)

    @staticmethod
    def __get_loss(y_train: np.ndarray, y_pred: np.ndarray):
        """
        cost function after each epoch
        :param y_train: output of training set
        :type y_train: np.ndarray
        :param y_pred: predicted output
        :type y_pred: np.ndarray
        :return: cost
        :rtype: float
        """
        m = y_train.shape[0]
        cost = (-1 / m) * ((y_train.T @ np.log(y_pred)) + ((1 - y_train).T @ np.log(1 - y_pred)))
        return cost[0, 0]

    def predict(self, x_test: np.ndarray, threshold: float = 0.5):
        """
        test on testing set
        :param x_test: input of testing set
        :type x_test: np.ndarray
        :param threshold: threshold that divide pos and nev
        :type threshold: float
        :return: predicted labels
        :rtype: np.ndarray
        """
        output = self.__forward_propagation(x_test)
        y_pred = np.where(output >= threshold, 1, 0)
        return y_pred

    @staticmethod
    def accuracy_score(y_test: np.ndarray, y_pred: np.ndarray):
        """
        accuracy of model on testing set
        :param y_test: true output of testing set
        :type y_test: np.ndarray
        :param y_pred: predicted output of testing set
        :type y_pred: np.ndarray
        :return: accuracy score
        :rtype: float
        """
        accuracy = np.sum(np.equal(y_test, y_pred))[0] / len(y_test)
        return accuracy
