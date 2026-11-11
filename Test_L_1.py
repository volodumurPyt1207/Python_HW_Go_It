import numpy as np
from numpy import linalg as LA

data_matrix = np.array([[2,2],[8,2]])

eig_val, eig_vect = LA.eig(data_matrix)
print(eig_val)
print(eig_vect)