import sympy as sm

def Diff(function):
    x = sm.symbols('x')
    print(sm.diff(function, x))
