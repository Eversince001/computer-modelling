import matplotlib.pyplot as plt

def Hist(x, y):
    fig, ax = plt.subplots()
    ax.bar(x, y, color='blue')
    fig.set_figwidth(7)
    fig.set_figheight(6)
    plt.show()
