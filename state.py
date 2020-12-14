import os
import json
import time
from typing import Tuple
from light_controller.controller import *


class State:

    def __init__(self):
        # fl_count: 航班总数
        # to_count: 起飞数量
        # ld_count: 降落数量
        self.__fl_count = 0
        self.__to_count = 0
        self.__ld_count = 0
        # init的时候并不需要get data 但记得把light_controller相关的东西init一下
        self.__light_controller = BaseController()
        self.__interval = None
        self.__enabled = None

    def get_data_once(self):
        try:
            # 打开最新文件
            data_dir = os.listdir('data_source/data')
            for filename in data_dir:
                filename = int(filename[:-6])
            #             with open('data_source/data/' + str(max(data_dir)) + '.json') as f:
            with open('data_source/data/' + str(max(data_dir))) as f:
                flights = json.loads(f.read())
                data = flights.pop(0)
                # data:{'location':[latitude, longitude], [[min_latitude, min_longitude], [max_latitude, max_longitude]}
                # 暂时应该没有什么用 只是在这里留一个接口
            self.__fl_count = len(flights)
            self.__to_count = 0
            self.__ld_count = 0
            for flight in flights:
                if flight['vertical_speed'] > 0 and flight['altitude'] < 6000:
                    self.__to_count += 1
                if flight['vertical_speed'] < 0 and flight['altitude'] < 6000:
                    self.__ld_count += 1
        except ValueError:
            print('没有数据！')

    def light_sequence(self, mode, data=None):
        # mode = 1 用于表示航班总数
        # mode = 2 用于表示起飞数量
        # mode = 3 用于表示降落数量
        # mode = 4 用于表示数据的间隔
        # mode = 5 用于表示一次完整流程的结束
        # data作为一个数据输入口
        if mode == 1:
            i = data / 10
            j = data % 10
            self.__light_controller.spark(1, i)
            self.__light_controller.spark(2, j)
        elif mode == 2:
            i = data / 10
            j = data % 10
            self.__light_controller.spark(1, i)
            self.__light_controller.spark(2, j)
        elif mode == 3:
            i = data / 10
            j = data % 10
            self.__light_controller.spark(1, i)
            self.__light_controller.spark(2, j)
        elif mode == 4:
            self.__light_controller.separated()
        elif mode == 5:
            self.__light_controller.work_once()

    def spin(self, enabled: Tuple[bool, bool, bool], interval):
        while True:
            self.update_settings(enabled, interval)
            ct = time.time()
            self.get_data_once()
            if self.__enabled[0]:
                self.light_sequence(1, self.__fl_count)
                if self.__enabled[1] or self.__enabled[2]:
                    self.light_sequence(4)
            if self.__enabled[1]:
                self.light_sequence(2, self.__to_count)
                if self.__enabled[2]:
                    self.light_sequence(4)
            if self.__enabled[2]:
                self.light_sequence(3, self.__ld_count)
            self.light_sequence(5)
            dt = time.time() - ct
            time.sleep(self.__interval - dt)

    def update_settings(self, enabled, interval):
        self.__enabled = enabled
        self.__interval = interval
