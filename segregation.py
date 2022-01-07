# -*- coding: utf-8 -*-
# RafKac
#
# klasa odpowiedzialna za samą segregację


class Segregation:
    def __init__(self, x, y):
        self.listaRezydentow = []
        self.listaSuperpixeli= []
        self.lista_niezadowolonych = []
        self.zadowolenie = 0.5
        self.krok = 0
        self.procent_zadowolonych = 0.0
        self.size_x = x
        self.size_y = y

    def czy_zadowolony(self, x, y):
        """
        jako parametry dostajemy współrzędne sprawdzanego rezydenta
        :return: zwracamy True, jeśli procent sąsiadów danego typu jest większy, niż zadowolenie
        False w przeciwnym przypadku.
        jeśli jest pusty, to traktujemy jako zadowolony
        najpierw ustalamy punkty współrzędne początku i końca "otoczenia" do przejrzenia, a później przeglądamy
        po wyliczonym otoczeniu punktu
        """
        l_diff = 0
        x_p = 0
        x_k = 0
        y_p = 0
        y_k = 0
        iterator = 0.0

        if self.listaRezydentow[x][y] == 0:
            return True
        if x - 1 < 0:
            if y - 1 < 0:
                x_p = x
                x_k = x + 1
                y_p = y
                y_k = y + 1
            elif y + 1 == self.size_y:
                x_p = x
                x_k = x + 1
                y_p = y - 1
                y_k = y
            else:
                x_p = x
                x_k = x + 1
                y_p = y - 1
                y_k = y + 1
        elif x + 1 >= self.size_x:
            if y - 1 < 0:
                x_p = x - 1
                x_k = x
                y_p = y
                y_k = y + 1
            elif y + 1 == self.size_y:
                x_p = x - 1
                x_k = x
                y_p = y - 1
                y_k = y
            else:
                x_p = x - 1
                x_k = x
                y_p = y - 1
                y_k = y + 1
        elif y - 1 < 0:
            x_p = x - 1
            x_k = x + 1
            y_p = y
            y_k = y + 1
        elif y + 1 >= self.size_x:
            x_p = x - 1
            x_k = x + 1
            y_p = y - 1
            y_k = y
        else:
            x_p = x - 1
            x_k = x + 1
            y_p = y - 1
            y_k = y + 1

        for u in range(x_p, x_k + 1):
            for v in range(y_p, y_k + 1):
                if self.listaRezydentow[x][y] != self.listaRezydentow[u][v]:
                    l_diff += 1
                iterator += 1.0
        if l_diff/iterator > self.zadowolenie:
            return False
        else:
            return True
