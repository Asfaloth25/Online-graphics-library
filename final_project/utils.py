import numpy as np
import math
import copy
from typing import Iterable

normalize_color = lambda x: np.array(x) / 255

def normalize_points(points:Iterable):
    'Recibe un iterable de puntos y devuelve un array de Numpy en el formato adecuado para el programa de OpenGL'
    MAXPOINTS = 1000
    numpoints = len(points)
    points_converted = np.array(points)
    if numpoints < MAXPOINTS:
        padding = np.zeros((MAXPOINTS-numpoints, 2), dtype='f4')
        points_converted = np.vstack([points_converted, padding])
    return points_converted, numpoints

machine_epsilon = 1e-10

def signed_area(A,B,C):
    return((B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0]))/2

def convert_line_notation(A,B):
    'Recibe dos puntos de la recta y devuelve la pendiente y la altura del corte con el eje Y'
    if A[0] == B[0]:
        raise ZeroDivisionError('La recta tiene pendiente infinita')
    m = (A[1]-B[1])/(A[0]-B[0])
    c = A[1]-m*(A[0])
    return (m, c)

def line_intersection(r:Iterable[tuple],s:Iterable[tuple]):
    if r[0][0] == r[1][0]:
        if s[0][0] == s[1][0]:
            raise ValueError(f'Both lines {r} and {s} are vertical')
        m, c = convert_line_notation(*s)
        return (r[0][0], m*r[0][0] + c)
    elif s[0][0] == s[1][0]:
        m, c = convert_line_notation(*r)
        return (s[0][0], m*s[0][0] + c)

    try:
        a, b = convert_line_notation(*r)
        c, d = convert_line_notation(*s)
    except ZeroDivisionError:
        return 

    if a == c:
        raise ValueError(f'The lines {r} and {s} do not intersect!')
    x0 = (d-b)/(a-c)
    y0 = a*x0 + b
    return (x0, y0)


def polygon_cut_semiplane(P:Iterable,s:tuple[tuple]) -> list:
    'Devuelve el polígono resultante de cortar P con el semiplano s, quedándose con los puntos a la izquierda de s.'
    if not P:
        return []
    
    l = []
    if len(P) == 1:
        return [P]
    if signed_area(*s, P[0])>=0:
        is_in=True
        l.append(P[0])
    else:
        is_in = False
            
    for i in range(1, len(P)):
        if signed_area(*s, P[i]) >= -machine_epsilon and is_in:
            l.append(P[i])
        elif signed_area(*s, P[i]) >= 0 and not is_in:
            l.append(line_intersection([P[i-1], P[i]], s))
            l.append(P[i])
            is_in = True
        elif signed_area(*s, P[i]) < machine_epsilon and is_in:
            l.append(line_intersection([P[i-1], P[i]], s))
            is_in = False
            
    if signed_area(*s, P[-1])*signed_area(*s,P[0]) <0:
        l.append(line_intersection([P[-1], P[0]], s))
            
    return l



def polygon_kernel(P:Iterable):
    if len(P) <= 1:
        return P
    
    N = copy.deepcopy(P)

    for i, vert in enumerate(P):
        N = polygon_cut_semiplane(N, (P[i-1], vert))
    return N

def is_inside_polygon(P:Iterable, point:tuple):
    below:bool
    last_below = P[0][1] < point[1]
    intersection_count = 0

    for i in range(len(P)-1):
        below = P[i][1] < point[1]
        if below + last_below == 1: # XOR(below, last_below)
            intersection_count +=  (signed_area(P[i], point, P[i-1]) * (-1)**below > 0)
        last_below = below

    # El último segmento (del último vértice al primero)
    below = P[0][1] < point[1]
    if below + last_below == 1: # XOR(below, last_below)
        intersection_count +=  (signed_area(P[i], point, P[i-1]) * (-1)**below > 0)

    return intersection_count % 2









def qh(a, b, S):
    if not S: # S es vacío
        return S
    
    KEY = lambda point: signed_area(a, b, point)
    c = max(S, key=KEY)
    S_new = [p for p in S if p not in (a,b)]
    
    return qh(c, b, [p for p in S_new if signed_area(c, b, p)>0]) + [c] + qh(a, c, [p for p in S_new if signed_area(a,c,p)>0])
    
def quickhull(P:Iterable):
    
    A, B = min(P), max(P) # Extremos de la nube de puntos
    KEY = lambda point: signed_area(A, B, point)
    left, right = [], []
    [(left, right)[KEY(point) < 0].append(point) for point in P if point not in (A,B)]

    return [B] + qh(A, B, left) + [A] + qh(B, A, right)
