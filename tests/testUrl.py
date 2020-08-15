#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.2"

__all__ = ()

from api_bridge.url import valid_url
from unittest import TestCase, main


class UrlTest(TestCase):
    def testValid(self):
        self.assertTrue(valid_url('https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400&date=today'),
                        'A valid url was deemed invalid!')

    def testInvalid(self):
        self.assertFalse(valid_url('google/maps'),
                         'A invalid url was deemed valid!')


if __name__ == '__main__': pass
