import numpy as np

a = np.ndarray((2, 4))

#print(a)
a[(1, 2)] = 3
print(a)
print(a[(1, 2)])