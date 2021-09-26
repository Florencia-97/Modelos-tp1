def solucion():
    n_prendas = 0
    m_incompatibilidades = 0
    _incompatibles = {}
    _tiempo_prendas = [0] * 20 # Arreglar
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
                _incompatibles[n_1] = _incompatibles.get(n_1, []) + [n_2]
                _incompatibles[n_2] = _incompatibles.get(n_2, []) + [n_1]
            if tipo_de_comando == 'n':
                n_1 = parametros[1]
                tiempo = parametros[2]
                _tiempo_prendas[(int(n_1) - 1)] = int(tiempo)
    print(_tiempo_prendas)

solucion()