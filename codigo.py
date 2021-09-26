import numpy as np

def _xx():
    return [str(n) for n in range (1, 21)]

def remover_elemento(l, elem):
    return [x for x in l if x != elem]

class Solucion:
    def __init__(self):
        self._tiempo_prendas = []
        self._compatibles = {}
        self._n_prendas = 0
        self._m_incompatibilidades = 0
        self._solucion = []

    def _cargar_settings(self, n, m):
        self._n_prendas = int(n)
        self._tiempo_prendas = [0] * self._n_prendas
        self._m_incompatibilidades = int(m)

    def _comando_e(self, parametros):
        n_1 = parametros[1]
        n_2 = parametros[2]
        if n_1 == n_2:
            return
        self._compatibles[n_1] = remover_elemento(self._compatibles.get(n_1, _xx()), n_2)
        self._compatibles[n_2] = remover_elemento(self._compatibles.get(n_2, _xx()), n_1)

    def _comando_n(self, parametros):
        n_1 = parametros[1]
        tiempo = parametros[2]
        self._tiempo_prendas[(int(n_1) - 1)] = int(tiempo)
    
    def _parsear_documento(self):
        with open('./enunciado.txt', 'r') as archivo:
            for linea in archivo:
                parametros = linea.strip().split(' ')
                tipo_de_comando = parametros[0]
                if tipo_de_comando == 'c':
                    continue
                if tipo_de_comando == 'p':
                    self._cargar_settings(parametros[2], parametros[3])
                elif tipo_de_comando == 'e':
                    self._comando_e(parametros)
                elif tipo_de_comando == 'n':
                    self._comando_n(parametros)
    
    def _sort(self, s):
        numero_ropa = int(s[0]) - 1
        return self._tiempo_prendas[numero_ropa]

    def _buscar_solucion(self):
        self._solucion = set()
        lavado_numero = 1
        lista_compatibles = list(self._compatibles.items())
        lista_compatibles = sorted(lista_compatibles, key=self._sort)
        for prenda, compatibles in lista_compatibles:
            if self.prenda_ya_anotada(prenda):
                continue
            _prendas_posibles = self.prendas_posibles(prenda, compatibles)
            self._solucion.add((prenda, lavado_numero))
            for _pp in _prendas_posibles:
                self._solucion.add((_pp, lavado_numero))
            lavado_numero += 1

    def prenda_ya_anotada(self, prenda):
        for s in self._solucion:
            if prenda == s[0]:
                return True
        return False
    
    def prendas_posibles(self, prenda, prendas_compatibles):
        posibles = []
        for _prenda in prendas_compatibles:
            if self.prenda_ya_anotada(_prenda):
                continue
            if self._prenda_puede_entrar_en(_prenda, posibles):
                posibles.append(_prenda)
        return posibles
    
    def _prenda_puede_entrar_en(self, prenda, posibles):
        posibles_prenda = self._compatibles[prenda]
        for p in posibles:
            if p not in posibles_prenda:
                return False
        return True
    
    def _escribir_solucion(self):
        with open('./entrega_1.txt', 'w') as archivo:
            for entrada in self._solucion:
                archivo.write(f'{entrada[0]} , {entrada[1]}\n')

    def resolver(self):
        tiempo_prendas = self._parsear_documento()
        self._buscar_solucion()
        self._escribir_solucion()

def main():
    solucion = Solucion()
    solucion.resolver()

main()