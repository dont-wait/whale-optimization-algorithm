
import numpy as np

def schaffer(X, Y):
    numer = np.square(np.sin(X**2 - Y**2)) - 0.5
    denom = np.square(1.0 + (0.001*(X**2 + Y**2)))
    return 0.5 + (numer*(1.0/denom))


def eggholder(X, Y):
    y = Y + 47.0
    a = (-1.0) * (y) * np.sin(np.sqrt(np.absolute(( X / 2.0) + y)))
    b = (-1.0) * X * np.sin(np.sqrt(np.absolute(X - y)))
    return a + b


def booth(X, Y):
    return ((X) + (2.0 * Y) - 7.0)**2 + ((2.0 * X) + (Y)- 5.0)**2


def matyas(X, Y):
    return (0.26 * (X**2 + Y**2)) - (0.48 * X * Y)


def cross_in_tray(X, Y):   
    B = np.exp(np.absolute(100.0 - (np.sqrt(X**2 + Y**2) / np.pi)))
    A = np.absolute(np.sin(X) * np.sin(Y) * B) + 1
    return -0.0001 * (A**0.1)


def levi(X, Y):
    A = np.sin(3.0 * np.pi * X)**2
    B = ((X - 1)**2) * (1 + np.sin(3.0 * np.pi * Y)**2)
    C = ((Y - 1)**2) * (1 + np.sin(2.0 * np.pi * Y)**2)
    return A + B + C