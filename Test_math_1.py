import numpy as np

# Базовий вектор
v = np.array([2, 3])

# Множення на різні скаляри
scalars = [0.5, 1, 2, -1]
results = {}

print("Множення вектора v = [2, 3] на різні скаляри:\\n")
for alpha in scalars:
    result = alpha * v
    results[alpha] = result
    print(f"  {alpha} × v = {result}")
