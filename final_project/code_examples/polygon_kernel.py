SetZoom(0.75)
Grid()
BackgroundColor((200,200,255))

points = [(0,0), (1,1), (2,0), (2,1), (1,2), (0,1)]

Points(points, opacity=1, pointcolor=(0,255,0))
Polygon(points, linewidth=0.004, linecolor=(0,255,0))

CenterCamera((1,1))

kernel = PolygonKernel(points)
Polygon(kernel, linewidth=0.002, linecolor=(0,0,255))