from typing import List, Tuple, Dict, Any
import requests, json


class Fr24Crawler:

    def __init__(self, loc: Tuple[float, float], rng: float):
        # loc[0]是搜索中心的纬度latitude
        # loc[1]是经度longitude
        # rng在README上的定义非常ambiguous，姑且认为是搜索正方形边长的1/2，单位是nm海里
        # 1 n mile = 1852 m
        self.__center_latitude = loc[0]
        self.__center_longitude = loc[1]
        self.__min_latitude = None
        self.__min_longitude = None
        self.__max_latitude = None
        self.__max_longitude = None
        # bounds和headers用于后面的url
        self.__bounds = 'bounds={},{},{},{}&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&' \
                        'estimated=1&maxage=14400&gliders=1&stats=1'.format(self.__max_latitude, self.__min_latitude,
                                                                            self.__min_longitude, self.__max_longitude)
        self.__headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
            'Host': 'data-live.flightradar24.com'}
        # 后面步骤需要存储为一个文件 这里根据parameter先确定文件名（其实也可以挪到后面去？）
        self.__filename = "{},{},{}.json".format(loc[0], loc[1], rng)

    def get_data_once(self):
        response = requests.get('https://data-live.flightradar24.com/zones/fcgi/feed.js' + self.__bounds,
                                headers=self.__headers)
        # output是return或保存到文件的内容的容器
        output = []
        # 删除前两行没用的数据 以便之后for循环
        del response['full_count']
        del response['version']

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
            output.append({'longitude': flight[1], 'latitude': flight[2], 'heading': flight[3], 'altitude': flight[4],
                           'ground speed': flight[5], 'squawk number': flight[6], 'registration number': flight[9],
                           'flight number': flight[13], 'departure airport': flight[11], 'arrival airport': flight[12]})
        f = open(self.__filename, mode='w')
        f.write(json.dump(output))
    def spin(self, interval=10):
        raise NotImplementedError
