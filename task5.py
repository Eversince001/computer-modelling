import sympy as sm
from numpy import sin
from scipy.integrate import quad

def IntegrateN(function):
    x = sm.symbols('x')
    print(sm.integrate(function, x))

def function(x):
    return sin(x) / (x + 1)

def Integrate(function):
    print(quad(function, 0, 1))