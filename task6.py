import matplotlib.pyplot as plt
import numpy as np

def Graphic(y):
    fig = plt.subplots()
    x = np.linspace(0, 0.5)
    plt.plot(x, y(x))
    plt.show()

