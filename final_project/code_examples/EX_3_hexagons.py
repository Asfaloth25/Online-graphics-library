Es posible utilizar bucles, así como generadores como <<range>> y <<enumerate>>.
También se puede utilizar las librerías estándares Math, Numpy (np) y Time, sin necesidad de importarlas.
Utilizar el comando <<import>> hará que el código no sea ejecutado, para prevenir inyecciones en el código.
<DELIMITADOR>
Grid(linewidth=0.02)
z = 15
SetZoom(0.1*z)

points = []
for layer in range(-5,5,1):
    for height in range(-3,4,1):
        points.append((1/z*(3*layer+ 1.5*(height%2)),1/z*(math.sqrt(5)*1.15*height)))

Voronoi(points, opacity = 0.9, pointradius=0.15/z)