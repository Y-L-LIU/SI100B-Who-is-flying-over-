import json
import os
import requests
import time
from matplotlib import pyplot as plt
from typing import List, Tuple, Dict, Any


class Plotter:
    def __init__(self):
        # 初始化容器
        self.__min = None
        self.__max = None
        self.__flights = {}
        # 用于数据更新时划定范围
        self.__latest_file = None
        # 时间counter
        self.__n = 1
        # 用于传入共享内存检测更新
        self.__loc = [None, None]
        self.__rng = [None, None]
        self.__interval = None

    def reload(self):
        # 第一次先读取所有现有文件
        data_dir = os.listdir('data')
        data_dir.sort()
        # 如果不是第一次 从指定的latest file开始reload
        if self.__latest_file:
            data_dir = data_dir[data_dir.index(self.__latest_file) + 1:]
        for filename in data_dir:
            with open('data/' + filename) as f:
                flights = json.loads(f.read())
                data = flights.pop(0)
            # 这里认为第一次读取时data中坐标不会改变 后面get_data再进行相关操作
            self.__min = data['range'][0]
            self.__max = data['range'][1]
            for flight in flights:
                if flight['registration_number'] not in self.__flights:
                    self.__flights[flight['registration_number']] = {}
                    self.__flights[flight['registration_number']]['latitude'] = [flight['latitude']]
                    self.__flights[flight['registration_number']]['longitude'] = [flight['longitude']]
                    self.__flights[flight['registration_number']]['heading'] = [flight['heading']]
                    self.__flights[flight['registration_number']]['n'] = [self.__n]
                else:
                    self.__flights[flight['registration_number']]['latitude'].append(flight['latitude'])
                    self.__flights[flight['registration_number']]['longitude'].append(flight['longitude'])
                    self.__flights[flight['registration_number']]['heading'].append(flight['heading'])
                    self.__flights[flight['registration_number']]['n'].append(self.__n)
            self.__n += 1
        self.__latest_file = data_dir[-1]

    def get_data(self):
        data_dir = os.listdir('data')
        data_dir.sort()
        data_dir = data_dir[data_dir.index(self.__latest_file) + 1:]
        for filename in data_dir:
            with open('data/' + filename) as f:
                flights = json.loads(f.read())
                data = flights.pop(0)
            
            self.__min = data['range'][0]
            self.__max = data['range'][1]
            for flight in flights:
                if flight['registration_number'] not in self.__flights:
                    self.__flights[flight['registration_number']] = {}
                    self.__flights[flight['registration_number']]['latitude'] = [flight['latitude']]
                    self.__flights[flight['registration_number']]['longitude'] = [flight['longitude']]
                    self.__flights[flight['registration_number']]['heading'] = [flight['heading']]
                    self.__flights[flight['registration_number']]['n'] = [self.__n]
                else:
                    self.__flights[flight['registration_number']]['latitude'].append(flight['latitude'])
                    self.__flights[flight['registration_number']]['longitude'].append(flight['longitude'])
                    self.__flights[flight['registration_number']]['heading'].append(flight['heading'])
                    self.__flights[flight['registration_number']]['n'].append(self.__n)
            self.__n += 1
        self.__latest_file = data_dir[-1]

    def draw(self):
        for flight in self.__flights:
            plt.plot(self.__flights[flight]['longitude'], self.__flights[flight]['latitude'], linewidth=7, zorder=-1)
            plt.quiver(self.__flights[flight]['longitude'], self.__flights[flight]['latitude'], 1, 1,
                       [int(i / self.__n * 255) for i in self.__flights[flight]['n']],
                       angles=self.__flights[flight]['heading'], units='dots', pivot='mid',
                       headwidth=300, headlength=500, headaxislength=450, scale=0.1)

            plt.text(self.__flights[flight]['longitude'][-1], self.__flights[flight]['latitude'][-1],
                     flight)
        plt.xlim(self.__min[0], self.__max[0])
        plt.ylim(self.__min[1], self.__max[1])
        plt.savefig('web_server/static/img/amount.png')
        plt.savefig('web_server/static/img/takingoff.png')
        plt.savefig('web_server/static/img/landing.png')
        plt.cla()
       
    def spin(self, loc, rng, mode, interval):
        c = self.update_settings(loc, rng, mode, interval)
        if c:
            self.get_data()
        self.draw()

    def update_settings(self, loc, rng, interval):
        c = True
        if self.__loc[0] != loc[0] or self.__loc[1] != loc[1] or self.__rng[0] != rng[0] or self.__rng[1] != rng[1]:
            self.reload()
            # return的checker 表示reload过了 此次spin跳过get_data
            c = False
        self.__loc[0] = loc[0]
        self.__loc[1] = loc[1]
        self.__rng[0] = rng[0]
        self.__rng[1] = rng[1]
        self.__interval = interval.value
        return c


class Fr24Crawler:
    def __init__(self):
        self.__data = None
        self.__interval = None
        self.__bounds = None
        self.__headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
            'Host': 'data-live.flightradar24.com'}
        self.plotter = Plotter()

    def get_data_once(self):
        r = requests.get('https://data-live.flightradar24.com/zones/fcgi/feed.js?' + self.__bounds,
                         headers=self.__headers)
        response = json.loads(r.text)
        del response['full_count']
        del response['version']
        del response['stats']
        output = [self.__data]
        for flight in response:
            # 每一个flight里面的内容依次是：
            # 0  ICAO 24-bit address      str      国际民航组织24位飞机地址（不需要）
            # 1  longitude                float    经度
            # 2  latitude                 float    纬度
            # 3  track/heading            int      航向
            # 4  calibrated altitude      int      高度
            # 5  ground speed             int      地速
            # 6  squawk number            str      应答机编码
            # 7  ADS-B receiver code      str      广播式自动相关监视接收器编码（不需要）
            # 8  type                     str      飞机型号（不需要）
            # 9  registration number      str      国籍注册号
            # 10 some code?               int      未知编码（不需要）
            # 11 departure airport        str      始发机场
            # 12 arrival airport          str      目的机场
            # 13 flight number            str      航班号
            # 14 unknown 0 or 1           int/bool 未知（不需要？）
            # 15 vertical speed           int      垂直速度（不需要）
            # 16 airline flight number    str      非IATA航班号（不需要）
            # 17 unknown 0 or 1           int/bool 未知（不需要？）
            # 18 airline                  str      航空公司（不需要）

            output.append({'longitude': response[flight][1], 'latitude': response[flight][2],
                           'heading': response[flight][3], 'altitude': response[flight][4],
                           'ground_speed': response[flight][5], 'squawk_number': response[flight][6],
                           'registration_number': response[flight][9], 'flight_number': response[flight][13],
                           'departure_airport': response[flight][11], 'arrival_airport': response[flight][12],
                           'vertical_speed': response[flight][15]})
        t = time.time_ns()
        output[0]['time'] = t
        with open('data/' + str(t) + ".json", mode='w') as f:
            f.write(json.dumps(output))

    def spin(self, loc: Tuple[float, float], rng, interval):
        while True:
            ct = time.time()
            self.update_settings(loc, rng, interval)
            self.get_data_once()
            c = self.plotter.update_settings(loc, rng, interval)
            if c:
                self.plotter.get_data()
            self.plotter.draw()
            dt = time.time() - ct
            n = 1
            while self.__interval * n - dt < 0:
                n += 1
            time.sleep(self.__interval * n - dt)

    def update_settings(self, loc, rng, interval):
        # loc->location rng->range
        # loc:(latitude经度, longitude纬度)
        # rng: mode=0(西北角坐标) (latitude经度, longitude纬度)
        #      mode=1(长方形长高) (length长, height高)单位是nm海里
        d_latitude = rng[0] - loc[0]
        d_longitude = loc[1] - rng[1]
        min_latitude = loc[0] - d_latitude
        min_longitude = loc[1] - d_longitude
        max_latitude = loc[0] + d_latitude
        max_longitude = loc[1] + d_longitude
        # data是当作接口的一个东西 存在json文件列表的第0项里
        self.__interval = interval.value
        self.__data = {'location': [loc[0], loc[1]],
                       'range': ((min_latitude, min_longitude), (max_latitude, max_longitude))}
        # bounds和headers用于后面的url
        self.__bounds = 'bounds={},{},{},{}&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&' \
                        'estimated=1&maxage=14400&gliders=1&stats=1'.format(max_latitude, min_latitude,
                                                                            min_longitude, max_longitude)

