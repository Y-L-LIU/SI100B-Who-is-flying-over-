import os
import json
import time
from typing import Tuple
from data_source.fr24_crawler import Fr24Crawler
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

    def get_data_once(self):
        try:
            # 打开最新文件
            data_dir = os.listdir('data_source/data')
            for filename in data_dir:
                filename = int(filename[:-6])
            with open('data_source/data/' + str(max(data_dir)) + '.json') as f:
                flights = json.loads(f.read())
                data = flights.pop(0)
                # data:{'location': [latitude, longitude], [[min_latitude, min_longitude], [max_latitude, max_longitude]}
                # 暂时应该没有什么用 只是在这里留一个接口
            self.__fl_count = len(flights)
            self.__to_count = 0
            self.__ld_count = 0
            for flight in flights:
                if flight['vertical_speed'] > 0 and flight['altitude'] < 3000:
                    self.__to_count += 1
                if flight['vertical_speed'] < 0 and flight['altitude'] < 3000:
                    self.__ld_count += 1
        except ValueError:
            print('没有数据！')


    def light_sequence(self,mode,data): 
        #mode = 1 用于表示航班总数    mode = 2 用于表示起飞数量    mode = 3 用于表示降落数量   mode = 4 用于表示数据的间隔   mode = 5 用于表示一次完整流程的结束  data作为一个数据输入口
        if mode = 1:
            i = data / 10
            j = data % 10
            self.__light_controller.spark(1,i)
            self.__light_controller.spark(2.j)
        if mode = 2:
            i = data / 10
            j = data % 10
            self.__light_controller.spark(1,i)
            self.__light_controller.spark(2.j)
        if mode = 3:
            i = data / 10
            j = data % 10
            self.__light_controller.spark(1,i)
            self.__light_controller.spark(2.j)
        if mode = 4:
            self.__light_controller.separated()
        if mode = 5:
            self.__light_controller.work_once()
        

    def spin(self, interval=10):
        while True:
            self.get_data_once()
            self.light_sequence()
            time.sleep(interval)