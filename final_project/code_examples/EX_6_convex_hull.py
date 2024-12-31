La función <<ConvexHull>> calcula el cierre convexo de una nube de puntos, utilizando el algoritmo Quickhull.
<DELIMITADOR>
BackgroundColor((230,230,255))
Grid()

n_points = 15
points = [[2*np.random.rand()-1 for _ in range(2)] for _ in range(n_points)]

Points(points, color = (0,0,0))
hull = ConvexHull(points)
Points(hull, color = (0,100,200))

Polygon(hull, color = (0,255,255), opacity=0.3)