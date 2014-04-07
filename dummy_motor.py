#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
from multiprocessing.managers import BaseManager


class BotManager(BaseManager):
    pass

BotManager.register('order_pos')
BotManager.register('real_pos')

sleep = 0.01  # seconds
linear_speed = 10.0 * sleep  # mm/sleep

if __name__ == '__main__':
    manager = BotManager(address='./bot.sock', authkey=bytes('42', 'ascii'))
    manager.connect()

    order_pos = manager.order_pos()
    real_pos = manager.real_pos()

    try:
        while True:
            order = order_pos.get()
            pos = real_pos.get()
            print(pos)

            dx = order[0] - pos[0]
            dy = order[1] - pos[1]
            dl = dx ** 2 + dy ** 2
            if dl > linear_speed ** 2:
                scl = linear_speed / math.sqrt(dl)
                dx *= scl
                dy *= scl

            x = pos[0] + dx
            y = pos[1] + dy
            real_pos.set(x, y, 0)

            time.sleep(sleep)
    except KeyboardInterrupt:
        pass
