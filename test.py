import numpy as np
import numexpr as ne
import torch
import time

# Assuming V and W are NumPy arrays
V = np.array([[1, 1], [2, 2], [3, 3]])
W = np.array([[4, 4], [5, 5], [6, 6]])

# Use broadcasting to create matrix A
A = V[:, np.newaxis] - W

#r shape n1 n2 2 i,j,: vector from w[i] to v[j]
r = V[:, np.newaxis] - W # r
r_norm = np.sum((r**2),axis=2)
masked_r = (r_norm < 10)
print(r[masked_r])
