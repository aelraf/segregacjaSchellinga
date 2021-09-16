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


pygame.init()
resolution  = (800, 600)
window = pygame.display.set_mode(resolution)
run = True
listaRezydentow = []
zadowolenie = 0.5


def main():
    """

    """


if __name__ == '__main__':
    main()
