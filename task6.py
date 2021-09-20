import matplotlib.pyplot as plt
import numpy as np

def Graphic(y, a, b):
    fig = plt.subplots()
    x = np.linspace(a, b)
    plt.plot(x, y(x))
    plt.show()

