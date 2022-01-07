# -*- coding: utf-8 -*-
# RafKac
#
# klasa odpowiedzialna za samą segregację
import random


class Segregation:
    def __init__(self, x, y):
        self.zadowolenie = 0.5
        self.krok = 0
        self.procent_zadowolonych = 0.0
        self.size_x = x
        self.size_y = y

        self.zadowolony = 0
        self.niezadowolony = 0

        self.listaRezydentow = [[0] * self.size_x for _ in range(self.size_y)]
        self.lista_niezadowolonych = [[0] * self.size_x for _ in range(self.size_y)]
        self.lista_niezadowolonych = []

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

    def sprawdzanie_zadowolenia(self):
        """
        Zliczamy zadowolonych i niezadowolonych oraz dodajemy odpowiednie wartości do lista_niezadowolonych:
        0 - niezadowolony
        1 - zadowolony
        """
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.czy_zadowolony(x, y):
                    self.zadowolony += 1
                    self.lista_niezadowolonych[x][y] = 1
                else:
                    self.niezadowolony += 1
                    self.lista_niezadowolonych[x][y] = 0

    def zeroj_niezadowolonych(self):
        self.zadowolony = 0
        self.niezadowolony = 0

    def licz_procent_zadowolonych(self):
        self.procent_zadowolonych = self.zadowolony * 100 / (self.size_x * self.size_y)

    def losuj(self):
        """
        dla listy rezydentów losuje, czy w danym miejscu będzie przedstawiciel pierwszej czy drugiej populacji,
        czy też wolne miejsce
        1 - pierwsza populacja
        2 - druga populacja
        0 - wolne miejsce
        :return:
        """
        print("losuj()")
        krok = 0
        for i in range(self.size_x):
            for j in range(self.size_y):
                los = random.random()
                if los < 1.0 / 3.0:
                    self.listaRezydentow[i][j] = 0
                elif 1.0 / 3.0 < los < 2.0 / 3.0:
                    self.listaRezydentow[i][j] = 1
                else:
                    self.listaRezydentow[i][j] = 2

    def przenies_do_losowego(self, a, b):
        """
        metoda dostaje współrzędne rezydenta do przeniesienia, losuje komórkę, jeśli wylosowana jest pusta,
        to przenosi do niej rezydenta
        """
        los = True

        while los:
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            if self.listaRezydentow[x][y] == 0:
                self.listaRezydentow[x][y] = self.listaRezydentow[a][b]
                self.listaRezydentow[a][b] = 0
                los = False

    def dodaj_do_listy_niezadowolonych(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.czy_zadowolony(x, y):
                    self.zadowolony += 1
                    self.lista_niezadowolonych[x][y] = 1
                else:
                    self.niezadowolony += 1
                    self.lista_niezadowolonych[x][y] = 0

    def losowe_przenoszenie_niezadowolonych(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                maruda = self.lista_niezadowolonych[x][y]
                if maruda == 0:
                    self.przenies_do_losowego(x, y)


