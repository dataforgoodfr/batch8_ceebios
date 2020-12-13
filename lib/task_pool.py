# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:46:37 2020

@author: Christian Marechal

"""
""" pool mulithreading manager
"""


import os

import sys
import time
import pandas as pd
from threading import Thread

import multiprocessing
import random


def work_todo_example(number, tab, toexit=True):
    """ exemple of work which can process in parallel """
    # print("work-todo", number)
    it = iter(range(0, len(tab) + 1))

    a = tab[next(it)]
    b = tab[next(it)]
    c = tab[next(it)]

    d = 0
    time.sleep(1)
    for i in range(0, 100000):
        for j in range(0, 10):
            d = a + b + c + i
    if toexit == True:
        if number == 20:
            pass  # sys.exit(0)
        sys.exit(1)


class Task_pool_p:
    """ task pool mamanger with multi processing lib """

    jobs = []
    worker = None
    pool_size = 10
    level = 0
    tot_res = 0
    tot_demande = 0

    def __init__(self, worker, pool_size, no_res_ret=True):
        self.jobs = []
        self.worker = worker
        self.pool_size = pool_size
        self.level = 0

        self.tot_demande = 0  # demande totale
        self.tot_res = 0  # resultat total

        self.tot_map = 0  # derniere map
        self.tot_map_res = 0  # resulat  map

        self.ret_ok = True

    def task_map(self, data, worker=None):
        if self.ret_ok == False:
            return False

        w = self.worker
        if worker is not None:  # different worker is possible
            w = worker
        p = multiprocessing.Process(
            target=w,
            args=(
                self.level,
                data,
            ),
        )
        self.jobs.append(p)
        p.start()
        self.tot_map += 1
        self.tot_demande += 1
        self.level += 1

        if self.level >= self.pool_size:
            for p in self.jobs:
                if self.ret_ok == False:
                    p.terminate()
                    continue
                p.join()
                try:
                    if p.exitcode == 1:
                        self.tot_res += 1
                        self.tot_map_res += 1
                    else:
                        self.ret_ok = False
                except:
                    self.ret_ok = False
                    print("bad exit")
            self.jobs = []
            self.level = 0
            self.tot_map = 0
            self.tot_map_res = 0
            return self.ret_ok
        return True

    def task_reduce(self):
        for p in self.jobs:
            if self.ret_ok == False:
                p.terminate()
                continue
            p.join()
            try:
                if p.exitcode == 1:
                    self.tot_res += 1
                    self.tot_map_res += 1
                else:
                    self.ret_ok = False
            except:
                self.ret_ok = False
                print("bad exit2")
        self.jobs = []
        self.level = 0
        self.tot_map = 0
        self.tot_map_res = 0
        print("p", self.ret_ok, self.tot_res, self.tot_demande)

        return self.ret_ok, self.tot_res


def test_Task_pool_p_example():
    """ example of use Task_pool_p class """

    total = 120
    if True:
        print("1) full scan iteration:")
        ts = time.time()
        tsx = time.time()
        for x in range(0, total):
            a = random.randint(0, 9)
            b = random.randint(0, 77)
            c = random.randint(0, 100)
            tab = [a, b, c]
            # print('iter', x)
            work_todo_example(0, tab, False)
            if time.time() - tsx > 20:
                print("-x:", x, "/", 120, round(time.time() - ts, 2))
                tsx = time.time()
        ts_fullScan = round(time.time() - ts, 2)
        print("end iteration:")

    if True:
        print("2) parallel")
        ts = time.time()
        tsx = time.time()
        job = Task_pool_p(None, 30)
        ret = True
        for x in range(0, total):
            a = random.randint(0, 9)
            b = random.randint(0, 77)
            c = random.randint(0, 100)
            tab = [a, b, c]
            job.task_map(tab, work_todo_example)
            if time.time() - tsx > 20:
                print("-x:", x, "/", 120, round(time.time() - ts, 2))
                tsx = time.time()
        ret, tot_res = job.task_reduce()
        ts_par = round(time.time() - ts, 2)
        print("end parallel:", ret, tot_res, ts_par)
        print("iteration:", ts_fullScan, " vs parallel:", ts_par)
