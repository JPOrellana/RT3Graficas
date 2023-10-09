from math import acos, asin, isclose, sqrt

def calcular_coordenadas_baricentricas(A, B, C, P):
    AB = [B[0] - A[0], B[1] - A[1]]
    AC = [C[0] - A[0], C[1] - A[1]]
    AP = [P[0] - A[0], P[1] - A[1]]

    areaABC = AB[0] * AC[1] - AB[1] * AC[0]
    areaPBC = AP[0] * BC[1] - AP[1] * BC[0]
    areaAPC = AP[0] * AC[1] - AP[1] * AC[0]
    areaABP = AB[0] * AP[1] - AB[1] * AP[0]

    if areaABC == 0:
        return None

    u = areaPBC / areaABC
    v = areaAPC / areaABC
    w = areaABP / areaABC

    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1 and isclose(u + v + w, 1.0):
        return (u, v, w)
    else:
        return (-1, -1, -1)

def multiplicar_matrices(matrixA, matrixB):
    rowsA = len(matrixA)
    colsA = len(matrixA[0])
    rowsB = len(matrixB)
    colsB = len(matrixB[0])

    if colsA != rowsB:
        raise ValueError("Las dimensiones de las matrices no permiten su multiplicación.")

    result = [[0 for _ in range(colsB)] for _ in range(rowsA)]

    for i in range(rowsA):
        for j in range(colsB):
            for k in range(colsA):
                result[i][j] += matrixA[i][k] * matrixB[k][j]
    return result

def subtract_vector(vectorA, vectorB):

    if len(vectorA) != len(vectorB):
        raise ValueError("Los vectores deben tener la misma longitud.")
    return [a - b for a, b in zip(vectorA, vectorB)]

def multiplicar_matriz_vector(matrix, vector):
    rows = len(matrix)
    cols = len(matrix[0])
    size = len(vector)

    if cols != size:
        raise ValueError("Las dimensiones de la matriz y el vector no permiten su multiplicación.")

    result = [0 for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            result[i] += matrix[i][j] * vector[j]
    return result




def generar_matriz_identidad(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def calcular_matriz_inversa(matrix):
    n = len(matrix)
    augmented_matrix = [row + generar_matriz_identidad(n)[i] for i, row in enumerate(matrix)]

    for i in range(n):
        pivot = augmented_matrix[i][i]
        for j in range(2 * n):
            augmented_matrix[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(2 * n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

    inverse = [row[n:] for row in augmented_matrix]
    return inverse

def add_vector(vectorA, vectorB):
    if len(vectorA) != len(vectorB):
        raise ValueError("Los vectores deben tener la misma longitud.")

    return [a + b for a, b in zip(vectorA, vectorB)]


def calcular_producto_cruz(vecA, vecB):
    if len(vecA) != 3 or len(vecB) != 3:
        raise ValueError("Los vectores deben ser de 3 componentes.")
    
    result = [
        vecA[1] * vecB[2] - vecA[2] * vecB[1],
        vecA[2] * vecB[0] - vecA[0] * vecB[2],
        vecA[0] * vecB[1] - vecA[1] * vecB[0]
    ]
    return result

def normalizar_vector(vector):
    magnitude = sqrt(sum(component ** 2 for component in vector))
    result = [component / magnitude for component in vector]
    return result

def obtener_magnitud_vector(vector):
    magnitude = sqrt(sum(component ** 2 for component in vector))
    return magnitude

def restar_vectores(vectorA, vectorB):
    if len(vectorA) != len(vectorB):
        raise ValueError("Los vectores deben tener la misma longitud.")
    result = [a - b for a, b in zip(vectorA, vectorB)]
    return result

def sumar_vectores(vectorA, vectorB):
    if len(vectorA) != len(vectorB):
        raise ValueError("Los vectores deben tener la misma longitud.")
    result = [a + b for a, b in zip(vectorA, vectorB)]
    return result

def producto_punto(A, B):
    if len(A) != len(B):
        raise ValueError("Los vectores deben tener la misma longitud")

    result = 0
    for i in range(len(A)):
        result += A[i] * B[i]
    
    return result


def reflectVector(normal, direction):
    reflect = 2 * producto_punto(normal, direction)
    reflect = [reflect * normal[i] for i in range(3)]
    reflect = subtract_vector(reflect, direction)
    reflect = normalizar_vector(reflect)

    return reflect

def multiplicar_vector_escalar(escalar, vector):
    result = [vector[i] * escalar for i in range(3)]
    return result

def dividir_vector_escalar(escalar, vector):
    result = [vector[i] / escalar for i in range(3)]
    return result

def calcular_reflejo(normal, direccion):
    reflect = 2 * producto_punto(normal, direccion)
    reflect = restar_vectores(multiplicar_vector_escalar(reflect, normal), direccion)
    reflect = normalizar_vector(reflect)
    return reflect

def calcular_refraccion(normal, incidente, n1, n2):
    c1 = producto_punto(normal, incidente)

    if c1 < 0: 
        c1 = -c1
    else:
        normal = multiplicar_vector_escalar(-1, normal)
        n1, n2 = n2, n1
    
    s2 = (n1 * (1 - c1**2) **0.5) / n2
    c2 = (1 - s2**2) **0.5

    term1 = sumar_vectores(incidente, multiplicar_vector_escalar(c1, normal))
    term2 = multiplicar_vector_escalar((1 - ((n1/n2)**2 * (1 - c1**2)))**0.5, normal)
    T = restar_vectores(multiplicar_vector_escalar(n1/n2, term1), term2)
    T = normalizar_vector(T)
    return T


def vector_scalar_mult(scalar, vector):

    return [vector[i] * scalar for i in range(3)]

def cross_product(vecA, vecB):

    if len(vecA) != 3 or len(vecB) != 3:
        raise ValueError("Los vectores deben ser de 3 componentes.")

    result = [
        vecA[1] * vecB[2] - vecA[2] * vecB[1],
        vecA[2] * vecB[0] - vecA[0] * vecB[2],
        vecA[0] * vecB[1] - vecA[1] * vecB[0]
    ]
    return result

def vector_normal(vector):
    magnitude = sqrt(sum(component ** 2 for component in vector))

    return magnitude

def reflexion_interna_total(normal, incidente, n1, n2):
    c1 = producto_punto(normal, incidente)

    if c1 < 0: 
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    return acos(c1) >= asin(n2/n1)

def fresnel(normal, incidente, n1, n2):
    c1 = producto_punto(normal, incidente)

    if c1 < 0: 
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * (1 - c1**2) **0.5) / n2
    c2 = (1 - s2**2) **0.5

    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2)))**2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1)))**2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr

    return Kr, Kt
