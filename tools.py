import matplotlib.pyplot as plt

# Математическое ожидание
def mo(x, n):
    m = 0

    for i in range(n):
        m += x[i]
    m /= n

    return m


# Дисперсия
def disp(x, n, m):
    d = 0

    for i in range(n):
        d += (x[i] - m) ** 2
    d /= (n - 1)

    return d


# Построение гистограммы
def drawHist(x, y):
    fig, ax = plt.subplots()

    ax.bar(x, y, color='C4')

    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.show()

    return True
