import numpy as np

def parsear_documento(incompatibles, tiempo_prendas):
    n_prendas = 0
    m_incompatibilidades = 0
    tiempo_prendas = [0] * 20 # Arreglar
    with open('./enunciado.txt', 'r') as archivo:
        for linea in archivo:
            parametros = linea.strip().split(' ')
            tipo_de_comando = parametros[0]
            if tipo_de_comando == 'c':
                continue
            if tipo_de_comando == 'p':
                n_prendas, m_incompatibilidades = parametros[2], parametros[3]
            if tipo_de_comando == 'e':
                n_1 = parametros[1]
                n_2 = parametros[2]
                incompatibles[n_1] = incompatibles.get(n_1, []) + [n_2]
                incompatibles[n_2] = incompatibles.get(n_2, []) + [n_1]
            if tipo_de_comando == 'n':
                n_1 = parametros[1]
                tiempo = parametros[2]
                tiempo_prendas[(int(n_1) - 1)] = int(tiempo)

def buscar_solucion(incompatibles, tiempo_prendas):
    sol = []
    lavado_numero = 1
    for prenda, incompatibles in incompatibles.items():
        sol.append((prenda, lavado_numero))
        lavado_numero += 1
    return sol

def escribir_solucion(solucion):
    with open('./entrega_1.txt', 'w') as archivo:
        for entrada in solucion:
            archivo.write(f'{entrada[0]} , {entrada[1]}\n')

def main():
    incompatibles = {}
    tiempo_prendas = []
    parsear_documento(incompatibles, tiempo_prendas)
    solucion = buscar_solucion(incompatibles, tiempo_prendas)
    escribir_solucion(solucion)

main()