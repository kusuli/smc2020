# 2020.11.16
import math
import numpy as np

#! sigmoid
def sigmoid(x):
	return 1.0 / (1.0 + math.e ** -x)

#! softplus
def softplus(x):
	return math.log(1.0 + math.exp(x))

#! softmax
def softmax(x):
	e_x = np.exp(x - np.max(x))
	return e_x / e_x.sum()
