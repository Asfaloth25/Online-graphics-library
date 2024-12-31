Para representar las regiones de Voronoi de una nube de puntos, se puede usar la siguiente función:
<DELIMITADOR>
Grid()
SetZoom(0.75)

# Ahora mismo, esta librería soporta hasta 1000 puntos. 
# Es una restricción añadida para limitar la carga computacional del servidor.
n_points = 15
points = [2*np.random.rand(2)-1 for _ in range(n_points)]

Voronoi(points, opacity=0.9)