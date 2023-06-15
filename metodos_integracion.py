def ReglaTrapecioSimple(a, b, func):
    return (b-a)*(func(a)+func(b))/2

def ReglaTrapecioCompuesta(a, b, func, n):
    h = (b - a) / n
    sumatoria = 0
    for i in range(1, n):
        sumatoria += func(a + i * h)
    return (b - a) * (func(a) + 2 * sumatoria + func(b)) / (2 * n)

def ReglaSimpsonUnTercioSimple(a, b, func):
    return (b - a) * (func(a) + 4 * func((a + b) / 2) + func(b)) / 6

def ReglaSimpsonUnTercioCompuesta(a, b, func, n):
    h = (b - a) / n
    m = h / 2
    sumatoria1 = 0
    sumatoria2 = 0
    for i in range(0, n):
        sumatoria1 += func(a + h * i + m)
    for i in range(1, n):
        sumatoria2 += func(a + h * i)
    return (b - a) * (func(a) + 4 * sumatoria1 + 2 * sumatoria2 + func(b)) / (6 * n)

def ReglaSimpsonTresOctavosSimple(a, b, func):
    return (b - a) * (func(a) + 3 * func(a + (b - a) / 3) + 3 * func(a + ((b - a) / 3) * 2) + func(b)) / 8

def ReglaSimpsonTresOctavosCompuesta(a, b, func, n):
    h = (b - a) / n
    y = h / 3
    z = y * 2
    sumatoria1 = 0
    sumatoria2 = 0
    for i in range(0, n):
        sumatoria1 += func(a + (h * i) + y) + func(a + (h * i) + z)
    for i in range(1, n):
        sumatoria2 += func(a + h * i)
    return ((b - a) / (8 * n)) * (func(a) + 3 * sumatoria1 + 2 * sumatoria2 + func(b))