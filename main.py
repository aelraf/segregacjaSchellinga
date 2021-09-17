# -*- coding: utf-8 -*-
# RafKac
# 2021_09_16
# algorytm powstawania getta, czyli algorytm segregacji Schellinga ("Schelling model segregation")
# na podstawie:
# http://nifty.stanford.edu/2014/mccown-schelling-model-segregation/
# https://www.cs.cornell.edu/home/kleinber/networks-book/
# dane:
# - tablica 2D zawierająca dwa typy populacji, losowo rozmieszczonej
# - każda komórka zawiera dokładnie jeden typ populacji lub jest pusta
# - dla każdej komórki sprawdzamy, czy rezydent jest zadowolony z sąsiedztwa
#     (<=> jeśli t% jego sąsiadów jest tego samego typu)
#       - zadowolony zostaje
#       - niezadowolony przenosi się na sąsiadujące wolne miejsce
# - sprawdzamy tak długo, aż każdy jest zadowolony (czyli powstały getta)
# uwagi:
# - model upraszcza rzeczywistość, bo każdy rezydent ma indywidualną wartość zadowolenia t,
#       nie przybywa nam rezydentów oraz mamy tylko dwa ich typy
# - procentowy rozkład typów deklarujemy na starcie
# - opracujemy algorytm ze stałym rozmiarem maksymalnym populacji
import time
import pygame
import random
import Przycisk
import SuperPixel


pygame.init()
resolution = (800, 530)
window = pygame.display.set_mode(resolution)
run = True
listaRezydentow = []
listaSuperpixeli = []
lista_niezadowolonych = []
zadowolenie = 0.5
krok = 0
procent_zadowolonych = 0.0
loop = False


def koniec():
    global run

    run = False


def czy_zadowolony(x, y):
    """
    jako parametry dostajemy współrzędne sprawdzanego rezydenta
    :return: zwracamy True, jeśli procent sąsiadów danego typu jest większy, niż zadowolenie
    False w przeciwnym przypadku.
    jeśli jest pusty, to traktujemy jako zadowolony
    """
    l_diff = 0
    if listaRezydentow[x][y] == 0:
        return True
    if x - 1 >= 0 and y - 1 >= 0 and x + 1 < 100 and y + 1 < 100:
        for u in range(x-1, x+2):
            for v in range(y-1, y+2):
                if listaRezydentow[x][y] != listaRezydentow[u][v] and listaRezydentow[u][v] != 0:
                    l_diff += 1
    if l_diff/8.0 < zadowolenie:
    #    print("wartość: {}".format(l_diff/8.0))
        return False
    else:
        return True


def rysuj():
    print("rysuj()")
    i = 0
    for p in listaRezydentow:
        for k in p:
            if k == 0:
                listaSuperpixeli[i].zmianaKoloru((255, 255, 255))
            elif k == 1:
                listaSuperpixeli[i].zmianaKoloru((255, 0, 0))
            elif k == 2:
                listaSuperpixeli[i].zmianaKoloru((0, 0, 255))
            i += 1


def przenies_do_losowego(a, b):
    """
    metoda dostaje współrzędne rezydenta do przeniesienia, losuje komórkę, jeśli wylosowana jest pusta,
    to przenosi do niej rezydenta
    """
    global listaRezydentow

    losujemy = True

    while losujemy:
        x = random.randint(0, 99)
        y = random.randint(0, 99)
        if listaRezydentow[x][y] == 0:
            listaRezydentow[x][y] = listaRezydentow[a][b]
            listaRezydentow[a][b] = 0
            losujemy = False


def zmien_superpiksele():
    global listaSuperpixeli

    for x in range(100):
        for y in range(100):
            sp = listaSuperpixeli[x][y]
            if listaRezydentow[x][y] == 0:
                sp.kolor = (255, 255, 255)
            elif listaRezydentow[x][y] == 1:
                sp.kolor = (255, 0, 0)
            elif listaRezydentow[x][y] == 2:
                sp.kolor = (0, 0, 255)


def start():
    """
    W pojedyńczej iteracji:
     1) sprawdzamy, czy dany rezydent jest zadowolony
     2) tworzymy tablicę zadowolenia rezydentów
     3) dla niezadowolonych rezydentów przenosimy każdego z nich na dowolne wolne miejsce (losowe)
    Kończymy, jeśli wszyscy są zadowoleni.
    Wypisujemy na ekranie bierzącą wartość zadowolenia oraz numer iteracji.
    """
    global loop, lista_niezadowolonych

    zadowolony = 0
    niezadowolony = 0
    iteracja = 0

    while loop:
        for x in range(100):
            for y in range(100):
                if czy_zadowolony(x, y):
                    zadowolony += 1
                    lista_niezadowolonych[x][y] = 1
                else:
                    niezadowolony += 1
                    lista_niezadowolonych[x][y] = 0
        print("Zadowolonych: {}, niezadowolonych: {}".format(zadowolony, niezadowolony))
        iteracja += 1
        for x in range(100):
            for y in range(100):
                maruda = lista_niezadowolonych[x][y]
                if maruda == 0:
                    przenies_do_losowego(x, y)
        if iteracja % 5 == 0:
            rysuj()
            time.sleep(1)
            for p in listaSuperpixeli:
                p.draw(window)
            pygame.display.update()
        print("iteracja: {}".format(iteracja))
        if zadowolony >= 9999 or iteracja > 150:
            loop = False
        zadowolony = 0
        niezadowolony = 0
    print("koniec metody start()")


def stop():
    global loop

    loop = False


def losuj():
    """
    dla listy rezydentów losuje, czy w danym miejscu będzie przedstawiciel pierwszej czy drugiej populacji,
    czy też wolne miejsce
    1 - pierwsza populacja
    2 - druga populacja
    0 - wolne miejsce
    :return:
    """
    global listaRezydentow, loop

    loop = True
    print("losuj()")
    for i in range(100):
        for j in range(100):
            los = random.random()
            if los < 1.0/3.0:
                listaRezydentow[i][j] = 0
            elif 1.0/3.0 < los < 2.0/3.0:
                listaRezydentow[i][j] = 1
            else:
                listaRezydentow[i][j] = 2
    rysuj()


def main():
    """

    """
    global run, listaSuperpixeli, listaRezydentow, lista_niezadowolonych

    clock = 0
    buttons_tab = []
    p1 = Przycisk.Przycisk(700, 40, "buttons/start")
    buttons_tab.append(p1)
    p2 = Przycisk.Przycisk(700, 80, "buttons/losuj")
    buttons_tab.append(p2)
    p3 = Przycisk.Przycisk(700, 120, "buttons/stop")
    buttons_tab.append(p3)
    p4 = Przycisk.Przycisk(700, 160, "buttons/koniec")
    buttons_tab.append(p4)

    x = 10
    y = 10

    for i in range(100):
        for j in range(100):
            s_p = SuperPixel.SuperPixel(x, y)
            x += 5
            listaSuperpixeli.append(s_p)
        x = 10
        y += 5

    listaRezydentow = [[0] * 100 for _ in range(100)]
    lista_niezadowolonych = [[0] * 100 for _ in range(100)]

    while run:
        clock += pygame.time.Clock().tick(60)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for p in buttons_tab:
                    if p.klikPrzycisk():
                        if p.nazwa == "koniec":
                            koniec()
                        elif p.nazwa == "start":
                            start()
                        elif p.nazwa == "losuj":
                            losuj()
                        elif p.nazwa == "stop":
                            stop()

        window.fill((60, 25, 60))
        for p in listaSuperpixeli:
            p.draw(window)

        for p in buttons_tab:
            p.draw(window)

        pygame.display.update()


if __name__ == '__main__':
    main()
