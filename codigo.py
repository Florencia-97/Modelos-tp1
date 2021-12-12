import numpy as np

def remover_elemento(l, elem):
    return [x for x in l if x != elem]

class Solucion:
    def __init__(self, archivo):
        self._archivo = archivo
        self._tiempo_prendas = []
        self._compatibles = {}
        self._n_prendas = 0
        self._m_incompatibilidades = 0
        self._solucion = set()
        self._tiempo = 0

    def _cargar_settings(self, n, m):
        self._n_prendas = int(n)
        self._tiempo_prendas = [0] * self._n_prendas
        self._m_incompatibilidades = int(m)
        for prenda_n in range(1, self._n_prendas + 1):
            comp = [str(num_p) for num_p in range (1, self._n_prendas + 1) if str(prenda_n) != str(num_p)]
            self._compatibles[str(prenda_n)] = comp

    def _comando_incompatibilidad(self, n_1, n_2):
        self._m_incompatibilidades -= 1
        self._compatibles[n_1].remove(n_2)
        self._compatibles[n_2].remove(n_1)

    def _comando_tiempo_prenda(self, n_1, tiempo):
        self._tiempo_prendas[(int(n_1) - 1)] = int(tiempo)
    
    def _parsear_documento(self):
        with open(self._archivo, 'r') as archivo:
            for linea in archivo:
                parametros = linea.strip().split(' ')
                tipo_de_comando = parametros[0]
                if tipo_de_comando == 'c':
                    continue
                if tipo_de_comando == 'p':
                    self._cargar_settings(*parametros[2:])
                elif tipo_de_comando == 'e':
                    self._comando_incompatibilidad(*parametros[1:])
                elif tipo_de_comando == 'n':
                    self._comando_tiempo_prenda(*parametros[1:])

    def _tiempo_de_lavado_de(self, numero_ropa):
        return self._tiempo_prendas[int(numero_ropa) - 1]

    # def _cantidad_de_prendas_posibles(self, numero_ropa):
    #     """No se utiliza, prueba para ordenar de otra forma"""
    #     prenda = str(int(numero_ropa) - 1)
    #     return len(self._compatibles.get(prenda, []))

    def _sort(self, s):
        return self._tiempo_de_lavado_de(s[0])

    def _buscar_solucion(self):
        self._solucion = set()
        lavado_numero = 1
        lista_compatibles = sorted(list(self._compatibles.items()), key=self._sort, reverse=True)
        for prenda, compatibles in lista_compatibles:
            if self.prenda_ya_anotada(prenda):
                continue
            self._solucion.add((prenda, lavado_numero))
            prendas_a_agregar = self.prendas_posibles(prenda, compatibles)
            for _pp in prendas_a_agregar:
                self._solucion.add((_pp, lavado_numero))
            self._tiempo += self._mayor_tiempo_de_lavado_entre(prendas_a_agregar + [prenda])
            lavado_numero += 1
    
    def _mayor_tiempo_de_lavado_entre(self, prendas):
        return max(self._tiempo_de_lavado_de(p) for p in prendas)

    def prenda_ya_anotada(self, prenda):
        return any([prenda == s[0] for s in self._solucion])

    # def _tiempo_prendas_compatibles(self, prenda, prendas):
    #     cont = self._tiempo_de_lavado_de(prenda)
    #     for p in prendas:
    #         if p in self._compatibles[prenda]:
    #             cont += self._tiempo_de_lavado_de(p)
    #     return cont
    
    def prendas_posibles(self, prenda, prendas_compatibles):
        prendas_a_agregar = []
        compatibles = sorted(prendas_compatibles, key=self._tiempo_de_lavado_de, reverse =True)
        for _prenda in compatibles:
            if self.prenda_ya_anotada(_prenda):
                continue
            if self._prenda_puede_entrar_en(_prenda, prendas_a_agregar):
                prendas_a_agregar.append(_prenda)
        return prendas_a_agregar
    
    def _prenda_puede_entrar_en(self, prenda, posibles):
        posibles_prendas = self._compatibles[prenda]
        return not any([(p not in posibles_prendas) for p in posibles])
    
    def _escribir_solucion(self):
        with open('./entrega_3.txt', 'w') as archivo:
            for entrada in self._solucion:
                archivo.write(f'{entrada[0]} {entrada[1]}\n')


    def resolver(self):
        tiempo_prendas = self._parsear_documento()
        self._buscar_solucion()
        self._escribir_solucion()
        print(self._tiempo)

def main():
    archivo = './tercer_problema.txt'
    solucion = Solucion(archivo)
    solucion.resolver()

main()
