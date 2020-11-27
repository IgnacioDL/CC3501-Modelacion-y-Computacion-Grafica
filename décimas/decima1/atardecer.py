#Ignacio Díaz

import numpy as np
import matplotlib.pyplot as plt

#funciones

def _drawRectangle(matrix, i0, j0, i1, j1, value):
    matrix[i0:i1, j0:j1] = value
    return matrix

def interpol(c1, c2, t):
    return c1 * (1-t) + c2 * t

def degradacion_horizontal(matrix, c1, c2, i0, j0, i1, j1):
    t = 0
    delta_pixeles = j1 - j0  # esta es la cantidad de intervalos

    while j0 <= j1:
        color_interpolado = interpol(c1, c2, t)
        _drawRectangle(matrix, i0, j0, i1, j0 + 1, color_interpolado)
        j0 = j0 + 1
        t = t + 1 / delta_pixeles

    return matrix


def degradacion_vertical(matrix, c1, c2, i0, j0, i1, j1):
    t = 0
    delta_pixeles = i1 - i0

    while i0 <= i1:
        color_interpolado = interpol(c1, c2, t)
        _drawRectangle(matrix, i0, j0, i0 + 1, j1, color_interpolado)
        i0 = i0 + 1
        t = t + 1 / delta_pixeles

    return matrix

def aprox(n):
    rest=n%int(n)
    if rest>=0.5:
        return int(n)+1
    else:
        return int(n)

def drawSemiCircle(matrix, i0, j0, R, value):

    new_matrix = np.copy(matrix)
    phi = np.pi / 2
    step = phi / R
    aux = R
    while aux >= 0:
        new_matrix[
        (i0 - aux):(i0 - aux + 1),
        (aprox(j0 - R * np.cos(phi))):(aprox(j0 + R * np.cos(phi)))
        ] = value

        phi -= step
        aux -= 1

    return new_matrix

#colores
color_verde = np.asarray([0,1,0])
color_azul = np.asarray([0,0,1])
color_naranjoAtardecer = np.asarray([1., 0.7725, 0.])
color_cieloAtardecer = np.asarray([0.4549, 0., 1.])
color_pastoAtardecer = np.asarray([0., 0.4705, 0.1215])

#imagen
image = np.zeros((30,30,3))
image = degradacion_vertical(image, color_cieloAtardecer, color_naranjoAtardecer, 0, 0, 15, 30)
image = degradacion_vertical(image, color_verde, color_pastoAtardecer, 15, 0, 30, 30)
image2 = drawSemiCircle(image, 14, 15, 8, [1, 1, 0])
fig = plt.figure()
plt.imshow(image2)
title = 'Atardecer'
fig.suptitle(title)
plt.show()