from numpy import cos, log, exp, sin, linspace, array
import matplotlib.pyplot as m
from sympy import integrate
import  sympy.abc as symbol
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from tkinter import Tk, Frame, Label, Entry, Button
from tkinter.ttk import Combobox
from scipy.interpolate import lagrange
from metodos_integracion import ReglaSimpsonTresOctavosCompuesta, ReglaSimpsonTresOctavosSimple, ReglaSimpsonUnTercioCompuesta, ReglaSimpsonUnTercioSimple, ReglaTrapecioCompuesta, ReglaTrapecioSimple

class Interfaz:

    def __init__(self) -> None:
        self.f = lambda x: 3 * x**4 - 4 * x**3 - 12 * x**2 + 5
        self.g = lambda x: cos(x)
        self.h = lambda x: x * log(x)
        self.i = lambda x: exp(2 * x) * sin(3 * x)
        self.j = lambda x: x / (x**2 + 4)
        self.metodos = [ReglaTrapecioSimple, ReglaTrapecioCompuesta, ReglaSimpsonUnTercioSimple, ReglaSimpsonUnTercioCompuesta,
           ReglaSimpsonTresOctavosSimple, ReglaSimpsonTresOctavosCompuesta]
        self.funciones = [self.f, self.g, self.h, self.i, self.j]

        self.ventana = Tk()
        self.ventana.title("Integración Numérica")
        self.ventana.resizable(0, 0)

        self.marco = Frame()
        self.marco.pack()

        Label(self.marco, text="Método").grid(row=0, column=0, padx=10, pady=10)
        self.menu_metodos = Combobox(self.marco)
        self.menu_metodos['values'] = ("Regla del Trapecio Simple", "Regla del Trapecio Compuesta", "Regla de Simpson 1/3 Simple",
                                "Regla de Simpson 1/3 Compuesta", "Regla de Simpson 3/8 Simple",
                                "Regla de Simpson 3/8 Compuesta")
        self.menu_metodos.grid(row=0, column=1)
        self.menu_metodos.config(width=30, justify="center")
        self.menu_metodos.current(0)

        Label(self.marco, text="Función").grid(row=0, column=2, padx=10, pady=10)
        self.menu_funciones = Combobox(self.marco)
        self.menu_funciones['values'] = ("3*x^4-4*x^3-12*x^2+5", "cos(x)", "x*ln(x)", "exp(2*x)*sin(3*x)", "x/(x^2+4)")
        self.menu_funciones.grid(row=0, column=3)
        self.menu_funciones.config(width=30, justify="center")
        self.menu_funciones.current(0)

        Label(self.marco, text="Límite a").grid(row=0, column=4, padx=10)
        self.campo_a = Entry(self.marco)
        self.campo_a.grid(row=0, column=5)
        self.campo_a.config(justify="center")

        Label(self.marco, text="Límite b").grid(row=0, column=6, padx=10)
        self.campo_b = Entry(self.marco)
        self.campo_b.grid(row=0, column=7)
        self.campo_b.config(justify="center")

        Label(self.marco, text="No. Intérvalos").grid(row=0, column=8, padx=10)
        self.campo_intervalos = Entry(self.marco)
        self.campo_intervalos.grid(row=0, column=9)
        self.campo_intervalos.config(justify="center")

        self.boton_calcular = Button(self.marco, text="Calcular", command=self.calcular)
        self.boton_calcular.grid(row=0, column=10, padx=10)

        self.figura = m.Figure(figsize=(12, 6), dpi=90)
        self.ax = self.figura.add_subplot(111)
        self.ax.grid(True)
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y(x)$')
        self.ax.set_title("Integración  Numérica")

        self.linea = FigureCanvasTkAgg(self.figura, self.marco)
        self.linea.get_tk_widget().grid(row=1, column=0, pady=10, columnspan=11)
        self.barra_navegacion = NavigationToolbar2Tk(self.linea, self.ventana)
        self.barra_navegacion.update()

        Label(self.marco, text="Aproximada").grid(row=2, column=0, padx=10)
        self.campo_integral_aprox = Entry(self.marco)
        self.campo_integral_aprox.grid(row=2, column=1)
        self.campo_integral_aprox.config(justify="center", width=30)

        Label(self.marco, text="Exacta").grid(row=2, column=2, padx=10)
        self.campo_integral_exac = Entry(self.marco)
        self.campo_integral_exac.grid(row=2, column=3)
        self.campo_integral_exac.config(justify="center", width=30)

        self.ventana.mainloop()

    def reestauraGrafica(self):
        self.ax.clear()
        self.ax.set_xlim([float(self.campo_a.get()), float(self.campo_b.get())])
        self.ax.grid(True)
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y(x)$')
        self.ax.set_title("Integración Numérica")
        self.ax.axhline(0, color="black")
        self.ax.axvline(0, color="black")

    def calcular(self):
        self.metodo = self.metodos[self.menu_metodos.current()]
        funcion = self.funciones[self.menu_funciones.current()]
        self.reestauraGrafica()
        if self.menu_metodos.current() % 2 == 0:
            resultado = self.metodo(float(self.campo_a.get()), float(self.campo_b.get()), funcion)
            self.graficar(float(self.campo_a.get()), float(self.campo_b.get()), funcion, m=self.menu_metodos.current())
        else:
            resultado = self.metodo(float(self.campo_a.get()), float(self.campo_b.get()), funcion, int(self.campo_intervalos.get()))
            self.graficar(float(self.campo_a.get()), float(self.campo_b.get()), funcion, int(self.campo_intervalos.get()), self.menu_metodos.current())
        self.campo_integral_aprox.delete(0, "end")
        self.campo_integral_aprox.insert(0, round(resultado, 6))
        integral = integrate(self.menu_funciones.get(), (symbol.x, float(self.campo_a.get()), float(self.campo_b.get())))
        self.campo_integral_exac.delete(0, "end")
        self.campo_integral_exac.insert(0, round(integral, 6))

    def TrapecioSimple(self, a , b, func):
        xi = linspace(a, b, 2)
        xj = linspace(a, b, 2 * 100)
        yi = func(xi)
        yj = func(xj)
        self.ax.plot(xj, yj, color='black')
        self.ax.plot(xi, yi, 'ro')
        self.ax.fill_between(xi, 0, yi)
        self.linea.draw()
    
    def TrapecioCompuesto(self, a, b, n, func):
        h = (b - a) / n
        xi = linspace(a, b, n + 1)
        xj = linspace(a, b, (n + 1) * 100)
        yi = func(xi)
        yj = func(xj)
        self.ax.plot(xj, yj, color='black')
        self.ax.plot(xi, yi, 'ro')
        for i in range(0, n, 1):
            x = linspace(a+h*i, a+h*(i+1), 2)
            y = func(x)
            self.ax.fill_between(x, 0, y)
        self.linea.draw()

    def simpsonUnTercioSimple(self, a, b, func):
        x = array([a, (a+b)/2, b])
        y = array([func(a), func((a+b)/2), func(b)])
        p = lagrange(x, y)
        xi = linspace(a, b, 100)
        yi = p(xi)
        yj = func(xi)
        self.ax.plot(xi, yj, color="black")
        self.ax.plot(x, y, 'ro')
        self.ax.fill_between(xi, 0, yi)
        self.linea.draw()

    def simpsonTercioCompuesto(self, a, b, n, func):
        h = (b - a) / n
        xi = linspace(a, b, 100)
        yi = func(xi)
        xj = linspace(a, b, n+1)
        yj = func(xj)
        for i in range(0, n, 1):
            x1 = a+h*i
            x2 = (a+h*(i+1))/2
            x3 = a+h*(i+1)
            if x1 == x2:
                x2 += 0.1
            p = lagrange([x1, x2, x3], [func(x1), func(x2), func(x3)])
            xk = linspace(x1, x3, 50)
            yk = p(xk)
            self.ax.fill_between(xk, 0, yk)
        self.ax.plot(xi, yi, color="black")
        self.ax.plot(xj, yj, 'ro')
        self.linea.draw()

    def simpson3OctavosSimple(self, a, b, func):
        x = array([a, a + (b - a) / 3, a + ((b - a) / 3) * 2, b])
        y = array([func(a), func(a + (b - a) / 3), func(a + ((b - a) / 3) * 2), func(b)])
        p = lagrange(x, y)
        xi = linspace(a, b, 100)
        yi = p(xi)
        yj = func(xi)
        self.ax.plot(xi, yj, color="black")
        self.ax.plot(x, y, 'ro')
        self.ax.fill_between(xi, 0, yi)
        self.linea.draw()

    def simpson3OctavosCompuesta(self, a, b, n, func):
        h = (b - a) / n
        y = h / 3
        z = y * 2
        xi = linspace(a, b, 100)
        yi = func(xi)
        xj = linspace(a, b, n+1)
        yj = func(xj)
        for i in range(0, n, 1):
            x1 = a+h*i
            x2 = a+(h*i)+y
            x3 = a+(h*i)+z
            x4 = a+h*(i+1)
            p = lagrange([x1, x2, x3, x4], [func(x1), func(x2), func(x3), func(x4)])
            xk = linspace(x1, x4, 50)
            yk = p(xk)
            self.ax.fill_between(xk, 0, yk)
        self.ax.plot(xi, yi, color="black")
        self.ax.plot(xj, yj, 'ro')
        self.linea.draw()

    def graficar(self, a , b, func, n=None, m=0):
        if m == 0:
            self.TrapecioSimple(a, b, func)
        elif m == 1:
            self.TrapecioCompuesto(a, b, n, func)
        elif m == 2:
            self.simpsonUnTercioSimple(a, b, func)
        elif m == 3:
            self.simpsonTercioCompuesto(a, b, n, func)
        elif m == 4:
            self.simpson3OctavosSimple(a, b, func)
        elif m == 5:
            self.simpson3OctavosCompuesta(a, b, n, func)

if __name__ == "__main__":
    Interfaz()