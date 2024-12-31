El código de Python que haya en estas celdas se ejecutará, generando una imagen.
<DELIMITADOR>
# Añadiendo una cuadrícula, cambiando el color del fondo y ajustando la cámara
Grid()
BackgroundColor((230,230,255))
SetZoom(0.5)

# Prueba a modificar estas rectas:
s = [
    (0, 0),
    (1.5, 1)
    ]

r = [
    (0.5,1),
    (1, -1)
]

# Dibujando las rectas
Points(r, color=(0,0,255), pointradius=0.05)
Line(r, color=(50,50,255))

Points(s, color=(255,0,0), pointradius=0.05)
Line(s, color=(255,50,50))

# Intersección de las rectas
Q = LineIntersection(r,s)

if Q is not None: # Si las rectas son paralelas, devolverá None.
    Point(Q, color=(100,255,100), pointradius=0.05)

    # Para centrar la imagen en el punto de intersección:
    # CenterCamera(Q)
