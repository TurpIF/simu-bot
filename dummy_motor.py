#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from multiprocessing.managers import BaseManager


class BotManager(BaseManager):
    pass

BotManager.register('order_pos')
BotManager.register('real_pos')

if __name__ == '__main__':
    manager = BotManager(address='./bot.sock', authkey=bytes('42', 'ascii'))
    manager.connect()

    try:
        n = 0
        while True:
            n += 1
            pos = manager.real_pos()
            print(pos.get())
            pos.set(n, n, n)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
