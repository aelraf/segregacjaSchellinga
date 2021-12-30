# -*- coding: utf-8 -*-
# RafKac

import unittest
from unittest import TestCase

import pygame

from Przycisk import Przycisk
from SuperPixel import SuperPixel


def create_key_mock(pressed_key):
    def helper():
        tmp = [0] * 3
        tmp[pressed_key] = 1
        return tmp

    return helper


class TestsPrzycisk(TestCase):
    def test_klik_przycisk(self):
        key = Przycisk(300, 40, "buttons/nauka")
        pygame.mouse.get_pressed = create_key_mock([0])
        self.assertEqual(key.klikPrzycisk(), True)


class TestsSuperPixel(TestCase):
    def test_klik(self):
        print()
        super_P = SuperPixel(5, 5)
        super_P.klik()

        self.assertEqual(super_P.kolor, (0, 0, 0))
        self.assertNotEqual(super_P.kolor, (255, 255, 255))


if __name__ == "__main__":
    unittest.main()
