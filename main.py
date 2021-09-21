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
buttons_tab = []
zadowolenie = 0.5
krok = 0
procent_zadowolonych = 0.0
loop = False
size_x = 100
size_y = 100


def koniec():
    global run

    run = False


def czy_zadowolony(x, y):
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

    if listaRezydentow[x][y] == 0:
        return True
    if x - 1 < 0:
        if y - 1 < 0:
            x_p = x
            x_k = x + 1
            y_p = y
            y_k = y + 1
        elif y + 1 == size_y:
            x_p = x
            x_k = x + 1
            y_p = y - 1
            y_k = y
        else:
            x_p = x
            x_k = x + 1
            y_p = y - 1
            y_k = y + 1
    elif x + 1 >= size_x:
        if y - 1 < 0:
            x_p = x - 1
            x_k = x
            y_p = y
            y_k = y + 1
        elif y + 1 == size_y:
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
    elif y + 1 >= size_x:
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
            if listaRezydentow[x][y] != listaRezydentow[u][v]:
                l_diff += 1
            iterator += 1.0
    if l_diff/iterator > zadowolenie:
        return False
    else:
        return True


def rysuj():
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
        x = random.randint(0, size_x - 1)
        y = random.randint(0, size_y - 1)
        if listaRezydentow[x][y] == 0:
            listaRezydentow[x][y] = listaRezydentow[a][b]
            listaRezydentow[a][b] = 0
            losujemy = False


def zmien_superpiksele():
    global listaSuperpixeli

    for x in range(size_x):
        for y in range(size_y):
            sp = listaSuperpixeli[x][y]
            if listaRezydentow[x][y] == 0:
                sp.kolor = (255, 255, 255)
            elif listaRezydentow[x][y] == 1:
                sp.kolor = (255, 0, 0)
            elif listaRezydentow[x][y] == 2:
                sp.kolor = (0, 0, 255)


def start():
    global loop

    loop = True


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

    #loop = True
    print("losuj()")
    for i in range(size_x):
        for j in range(size_y):
            los = random.random()
            if los < 1.0/3.0:
                listaRezydentow[i][j] = 0
            elif 1.0/3.0 < los < 2.0/3.0:
                listaRezydentow[i][j] = 1
            else:
                listaRezydentow[i][j] = 2
    rysuj()


def buttons_actions():
    global run

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


def text_with_residents():
    """
    metoda odpowiada za wyświetlanie rezydentów
    oraz warunków startowych
    """
    text_first = str()


def main():
    global run, listaSuperpixeli, listaRezydentow, lista_niezadowolonych, loop, buttons_tab, procent_zadowolonych

    clock = 0
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
    iteracja = 0
    zadowolony = 0
    niezadowolony = 0

    for i in range(size_x):
        for j in range(size_y):
            s_p = SuperPixel.SuperPixel(x, y)
            x += 5
            listaSuperpixeli.append(s_p)
        x = 10
        y += 5

    listaRezydentow = [[0] * size_x for _ in range(size_y)]
    lista_niezadowolonych = [[0] * size_x for _ in range(size_y)]

    while run:
        clock += pygame.time.Clock().tick(60)/1000

        buttons_actions()

        while loop:
            buttons_actions()
            for x in range(size_x):
                for y in range(size_y):
                    if czy_zadowolony(x, y):
                        zadowolony += 1
                        lista_niezadowolonych[x][y] = 1
                    else:
                        niezadowolony += 1
                        lista_niezadowolonych[x][y] = 0
            print("Zadowolonych: {}, niezadowolonych: {}".format(zadowolony, niezadowolony))
            procent_zadowolonych = zadowolony / (size_x * size_y)
            print(procent_zadowolonych)
            iteracja += 1
            for x in range(size_x):
                for y in range(size_y):
                    maruda = lista_niezadowolonych[x][y]
                    if maruda == 0:
                        przenies_do_losowego(x, y)
            if iteracja % 5 == 0:
                rysuj()
                pygame.time.delay(50)
                for p in listaSuperpixeli:
                    p.draw(window)
                pygame.display.update()
            print("iteracja: {}".format(iteracja))
            if zadowolony >= size_x*size_y:
                loop = False
            zadowolony = 0
            niezadowolony = 0
        iteracja = 0

        window.fill((60, 25, 60))
        for p in listaSuperpixeli:
            p.draw(window)

        for p in buttons_tab:
            p.draw(window)

        pygame.display.update()


if __name__ == '__main__':
    main()
