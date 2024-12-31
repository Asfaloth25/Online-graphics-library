La función <<Kernel>> calcula el núcleo de un polígono dado por sus vértices.
Los polígonos se definen en el sentido de las agujas del reloj.
<DELIMITADOR>
BackgroundColor((230,230,255))
Grid()
SetZoom(0.5) # Alejando la cámara
CenterCamera((2,1.5)) # Centrando la cámara en el punto (2,1.5) para ver el polígono

vertices = [
    (0,2),
    (1,1),
    (0,0),
    (2,1),
    (3,0),
    (3,1),
    (4,2),
    (3,2),
    (3,3),
    (2,2)
]

Polygon(vertices, color=(100,100,200))
kernel = Kernel(vertices)
Polygon(kernel, color=(20,255,100))