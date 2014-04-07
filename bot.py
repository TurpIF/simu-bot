#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from multiprocessing.managers import BaseProxy


class Point(object):
    """
    Data structure of a shared point in 2 dimension with the angular position.

    Arguments:
    x -- Millimeter : Position on the X axis
    y -- Millimeter : Position on the Y axis
    a -- Radian : Angular position in direct sens
    """
    def __init__(self, x, y, a=0):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        self.a = a
        self.lock = Lock()

    def get(self):
        """
        Return a tuple (x, y, a) of the current position. The call is
        thread-safe due to an internal lock.

        Returns:
        Tuple of the position
        """
        with self.lock:
            return (self.x, self.y, self.a)

    def set(self, x, y, a):
        """
        Set entirely the point. The call is thread-safe due to an internal
        lock.

        Arguments:
        x -- Millimeter : Position on the X axis
        y -- Millimeter : Position on the Y axis
        a -- Radian : Angular position in direct sens
        """
        with self.lock:
            self.x = x
            self.y = y
            self.a = a


order_pos = Point(100, 100, 0)
real_pos = Point(0, 0, 0)

class BotManager(BaseManager):
    pass

BotManager.register('order_pos', lambda: order_pos, exposed=['get', 'set'])
BotManager.register('real_pos', lambda: real_pos, exposed=['get', 'set'])

if __name__ == '__main__':
    manager = BotManager(address='./bot.sock', authkey=bytes('42', 'ascii'))
    server = manager.get_server()
    server.serve_forever()
