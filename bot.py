#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from multiprocessing.managers import BaseProxy


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
real_pos = Point(0, 0)


class BotManager(BaseManager):
    pass

BotManager.register('order_pos', lambda: order_pos, proxytype=PointProxy)
BotManager.register('real_pos', lambda: real_pos, proxytype=PointProxy)

if __name__ == '__main__':
    manager = BotManager(address='./bot.sock', authkey=bytes('42', 'ascii'))
    server = manager.get_server()
    server.serve_forever()
