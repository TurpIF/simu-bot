#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from multiprocessing.managers import BaseProxy
from multiprocessing.sharedctypes import Value


class Point(object):
    """
    Data structure of a shared point in 2 dimension with the angular position.

    Arguments:
    x -- Real : Position on the X axis
    y -- Real : Position on the Y axis
    a -- Radian : Angular position in direct sens
    """
    def __init__(self, x, y, a=0):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        self.a = a

    def get(self):
        """
        Return a tuple (x, y, a) of the current position.

        Returns:
        Tuple of the position
        """
        return (self.x, self.y, self.a)

    def set(self, x, y, a):
        """
        Set entirely the point.

        Arguments:
        x -- Real : Position on the X axis
        y -- Real : Position on the Y axis
        a -- Radian : Angular position in direct sens
        """
        self.x = x
        self.y = y
        self.a = a


class PointProxy(BaseProxy):
    _exposed_ = ['get', 'set']

    def __init__(self):
        super(PointProxy, self).__init__()
        self.lock = Lock()

    def get(self):
        return self

    def set(self, x, y, a):
        with self.lock:
            self._callmethod('set', (x, y, a))


order_pos = Point(0, 0)
l_order_pos = Lock()

real_pos = Point(0, 0)
l_real_pos = Lock()


def set_order_pos(x, y, a):
    """
    Give a new order to set the position.

    Arguments:
    x -- Real : Position on the X axis
    y -- Real : Position on the Y axis
    a -- Radian : Angular position in direct sens
    """
    with l_order_pos:
        order_pos.x = x
        order_pos.y = y
        order_pos.a = a


def get_order_pos():
    """
    Get the current order about the position.
    """
    with l_order_pos:
        return Point(order_pos.x, order_pos.y, order_pos.a)


def set_real_pos(x, y, a):
    """
    Update the real position.

    Arguments:
    x -- Real : Position on the X axis
    y -- Real : Position on the Y axis
    a -- Radian : Angular position in direct sens
    """
    with l_order_pos:
        order_pos.x = x
        order_pos.y = y
        order_pos.a = a


def get_real_pos():
    """
    Get the current real position.
    """
    with l_order_pos:
        return Point(real_pos.x, real_pos.y, real_pos.a)


class BotManager(BaseManager):
    pass

BotManager.register('set_order_pos', callable=set_order_pos)
BotManager.register('get_order_pos', callable=get_order_pos)
BotManager.register('set_real_pos', callable=set_real_pos)
BotManager.register('get_real_pos', callable=get_real_pos)

BotManager.register('real_pos', lambda: real_pos, proxytype=PointProxy)

if __name__ == '__main__':
    manager = BotManager(address='./bot.sock', authkey=bytes('42', 'ascii'))
    server = manager.get_server()
    server.serve_forever()
