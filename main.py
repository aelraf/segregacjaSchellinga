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
# - model upraszcza rzeczywistość, bo każdy rezydent ma indywidualną wartość zadowolenia t, nie przybywa nam rezydentów oraz mamy tylko dwa ich typy
# - procentowy rozkład typów deklarujemy na starcie
# - opracujemy algorytm ze stałym rozmiarem maksymalnym populacji

import pygame
import random

import Przycisk
import SuperPixel

pygame.init()
resolution  = (800, 600)
window = pygame.display.set_mode(resolution)
run = True
listaRezydentow = []
listaSuperpixeli = []
zadowolenie = 0.5
krok = 0
procent_zadowolonych = 0.0


def koniec():
    global run
    run = False


def rysuj():
    pass


def start():
    pass


def stop():
    pass


def losuj():
    """
    dla listy rezydentów losuje, czy w danym miejscu będzie przedstawiciel pierwszej czy drugiej populacji,
    czy też wolne miejsce
    1 - pierwsza populacja
    2 - druga populacja
    0 - wolne miejsce
    :return:
    """
    global listaRezydentow
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
    global run, listaSuperpixeli
    clock = 0
    buttonsTab = []
    p1 = Przycisk.Przycisk(700, 40, "buttons/start")
    buttonsTab.append(p1)

    x = 10
    y = 10

    for i in range(100):
        for j in range(100):
            s_p = SuperPixel.SuperPixel(x, y)
            x += 5
            listaSuperpixeli.append(s_p)
        x = 10
        y += 5

    while run:
        clock += pygame.time.Clock().tick(60)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for p in buttonsTab:
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

    for p in buttonsTab:
        p.draw(window)

    pygame.display.update()


if __name__ == '__main__':
    main()
