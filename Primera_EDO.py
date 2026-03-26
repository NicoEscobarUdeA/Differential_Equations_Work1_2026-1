import numpy as np
import matplotlib.pyplot as plt

# Definir la función de la pendiente
def f(x, y):
    return (7*x*y**3 - 3*y)/9

# Crear una malla de puntos
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x, y)

# Calcular las pendientes
U = np.ones_like(X)  # Componente en x (normalizada)
V = f(X, Y)           # Componente en y (dy/dx)

# Normalizar para que las flechas tengan tamaño uniforme
norm = np.sqrt(U**2 + V**2)
U = U / norm
V = V / norm

# Graficar el campo de pendientes
plt.figure(figsize=(10, 8))
plt.quiver(X, Y, U, V, alpha=0.7)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Campo de Pendientes para dy/dx = (7xy³ - 3y)/9')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.show()

#%% CON SYMPY


import sympy as sp

# Definir variables
x = sp.Symbol('x')
y = sp.Function('y')(x)

# Definir la EDO: 3y + 9*y' = 7*x*y**3
edo = 3*y + 9*sp.diff(y, x) - 7*x*y**3

# Resolver
sol_general = sp.dsolve(edo, y)
print("Solución general:")
print(sol_general)

# Para una condición inicial específica (ejemplo: y(0)=1)
# sol_particular = sp.dsolve(edo, y, ics={y.subs(x, 0): 1})
# print("\nSolución particular:")
# print(sol_particular)

#%%

import numpy as np
import matplotlib.pyplot as plt

# Definir la solución
def y_sol(x, C, signo=1):
    """
    signo = 1 para la rama positiva, -1 para la negativa
    """
    denominador = (7/3)*x + 7/2 + C*np.exp((2/3)*x)
    # Evitar valores negativos dentro de la raíz
    if denominador <= 0:
        return np.nan
    return signo / np.sqrt(denominador)

# Valores de x
x_vals = np.linspace(-3, 3, 200)

# Graficar diferentes soluciones para distintos C
plt.figure(figsize=(12, 8))

# Rama positiva
for C in [-5, -1, 0, 1, 5]:
    y_vals = [y_sol(x, C, signo=1) for x in x_vals]
    plt.plot(x_vals, y_vals, label=f'C = {C}')

# Rama negativa (opcional)
for C in [-5, -1, 0, 1, 5]:
    y_vals = [y_sol(x, C, signo=-1) for x in x_vals]
    plt.plot(x_vals, y_vals, '--', alpha=0.5)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Familia de Soluciones de $3y + 9y\' = 7xy^3$')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(-5, 5)
plt.show()

