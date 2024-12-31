Las imágenes se refrescan en tiempo real al realizar cualquier cambio en el código.
En este ejemplo, el reloj se quedará quieto hasta que se realice cualquier modificación.
Prueba a escribir un comentario en el código.
<DELIMITADOR>
# Color del fondo y cuadrícula
BackgroundColor((230,230,255))
Grid()

# El cuerpo del reloj (borde y centro blanco)
Points([(0,0)], pointradius=1, color=(0,0,255), opacity=0.9)
Points([(0,0)], pointradius=0.95, color=(255,255,255), opacity=1)

# Los indicadores de las horas (puntos grises)
indicator_angles = [i*math.pi/180 for i in range(0,360,30)]
indicator_positions = [0.85 * np.array([math.sin(ang), math.cos(ang)]) for ang in indicator_angles]
Points(indicator_positions)

# "time.ctime" devuelve la fecha y la hora en formato string: "Fri Nov 22 10:49:51 2024". Para construir una lista de enteros [horas, minutos, segundos]:
t = [int(i) for i in time.ctime().split(' ')[-2].split(':')]

# Obtenemos el ángulo que tiene que tener cada manecilla (en radianes)
angles = [(30,6,6)[i]*t[i]*math.pi/180 for i in range(3)]

# Éstas son las posiciones de la punta de las manecillas
points = [(math.sin(ang), math.cos(ang)) for ang in angles]

# Las agujas
[Segment([(0,0), (0.1*i+0.6)*np.array(points[i])], linewidth = (4-i)*0.01, color=(0,0,0), opacity=1) for i in range(3)]

# Alejando la cámara del reloj, para que se vea mejor
SetZoom(0.5)