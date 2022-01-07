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

import Przycisk
import SuperPixel
from segregation import Segregation

pygame.init()
resolution = (800, 530)
window = pygame.display.set_mode(resolution)
run = True


listaSuperpixeli = []
buttons_tab = []


loop = False
size_x = 100
size_y = 100


segregacja = Segregation(100, 100)


def koniec():
    global run

    run = False


def rysuj(lista_rezydentow):
    i = 0
    for p in lista_rezydentow:
        for k in p:
            if k == 0:
                listaSuperpixeli[i].zmianaKoloru((255, 255, 255))
            elif k == 1:
                listaSuperpixeli[i].zmianaKoloru((255, 0, 0))
            elif k == 2:
                listaSuperpixeli[i].zmianaKoloru((0, 0, 255))
            i += 1


def zmien_superpiksele():
    global listaSuperpixeli

    for x in range(size_x):
        for y in range(size_y):
            sp = listaSuperpixeli[x][y]
            if segregacja.listaRezydentow[x][y] == 0:
                sp.kolor = (255, 255, 255)
            elif segregacja.listaRezydentow[x][y] == 1:
                sp.kolor = (255, 0, 0)
            elif segregacja.listaRezydentow[x][y] == 2:
                sp.kolor = (0, 0, 255)


def start():
    global loop

    loop = True


def stop():
    global loop

    loop = False


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
                        segregacja.losuj()
                        rysuj(segregacja.listaRezydentow)
                    elif p.nazwa == "stop":
                        stop()


def text_with_residents(zad, k, x, y, procent_zad):
    """
    metoda odpowiada za wyświetlanie rezydentów
    oraz warunków startowych
    """
    global window

    text_color = (122, 209, 217)
    bg_color = (60, 25, 60)

    text_zadowolenie = str(zad)
    text_iteracja = str(k)
    text_size_x = str(x)
    text_size_y = str(y)
    text_zadowolonych = str(procent_zad)

    font = pygame.font.Font('freesansbold.ttf', 15)
    text1 = font.render("Zadowolenie: {}".format(text_zadowolenie), True, text_color, bg_color)
    text2 = font.render("X: {}".format(text_size_x), True, text_color, bg_color)
    text3 = font.render("Y: {}".format(text_size_y), True, text_color, bg_color)
    text4 = font.render("% zadowol.: {}".format(text_zadowolonych), True, text_color, bg_color)
    text5 = font.render("iteracja: {}".format(text_iteracja), True, text_color, bg_color)

    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect4 = text4.get_rect()
    textRect5 = text5.get_rect()

    textRect1.center = (590, 60)
    textRect2.center = (590, 80)
    textRect3.center = (590, 100)
    textRect4.center = (590, 120)
    textRect5.center = (590, 140)

    window.blit(text1, textRect1)
    window.blit(text2, textRect2)
    window.blit(text3, textRect3)
    window.blit(text4, textRect4)
    window.blit(text5, textRect5)


def main():
    global listaSuperpixeli, buttons_tab
    global run, loop

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

    for i in range(size_x):
        for j in range(size_y):
            s_p = SuperPixel.SuperPixel(x, y)
            x += 5
            listaSuperpixeli.append(s_p)
        x = 10
        y += 5

    while run:
        clock += pygame.time.Clock().tick(60)/1000

        buttons_actions()

        while loop:
            buttons_actions()
            text_with_residents(
                zad=segregacja.zadowolenie,
                k=segregacja.krok,
                procent_zad=segregacja.procent_zadowolonych,
                x=segregacja.size_x,
                y=segregacja.size_y
            )
            segregacja.dodaj_do_listy_niezadowolonych()

            print("Zadowolonych: {}, niezadowolonych: {}".format(segregacja.zadowolony, segregacja.niezadowolony))
            segregacja.licz_procent_zadowolonych()
            segregacja.krok += 1

            segregacja.losowe_przenoszenie_niezadowolonych()

            if segregacja.krok % 5 == 0:
                rysuj(segregacja.listaRezydentow)
                pygame.time.delay(50)
                for p in listaSuperpixeli:
                    p.draw(window)
                pygame.display.update()
            print("krok: {}".format(segregacja.krok))
            if segregacja.zadowolony >= segregacja.size_x * segregacja.size_y:
                loop = False

            segregacja.zeroj_niezadowolonych()

        window.fill((60, 25, 60))
        text_with_residents(
            zad=segregacja.zadowolenie,
            k=segregacja.krok,
            x=segregacja.size_x,
            y=segregacja.size_y,
            procent_zad=segregacja.procent_zadowolonych
        )
        for p in listaSuperpixeli:
            p.draw(window)

        for p in buttons_tab:
            p.draw(window)

        pygame.display.update()


if __name__ == '__main__':
    main()
