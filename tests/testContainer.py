#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-16"
__version__ = "0.0.0"

__all__ = ()

from api_bridge.container import Container

from unittest import TestCase


class ContainerTest(TestCase):
    def testCall(self):
        c = Container()
        self.assertEqual(
            None,
            c.value,
            'Container was not initialized empty!'
        )

        c(dict(test='case'))

        self.assertEqual(
            dict(test='case'),
            c.value,
            'Container was not initialized empty!'
        )

    def testString(self):
        c = Container()
        c(dict(test='case'))
        self.assertEqual(
            str(dict(test='case')),
            str(c),
            'String of Container was not correct!'
        )

        self.assertEqual(
            str(c),
            repr(c),
            'repr() of Container was not correct!'
        )


if __name__ == '__main__': pass
