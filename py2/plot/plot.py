from matplotlib import pyplot as plt
import os
import json


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
        self.__loc = None
        self.__rng = None
        self.__interval = None

    def reload(self):
        # 第一次先读取所有现有文件
        data_dir = os.listdir('../data')
        data_dir.sort()
        # 如果不是第一次 从指定的latest file开始reload
        if self.__latest_file:
            data_dir = data_dir[data_dir.index(self.__latest_file) + 1:]
        for filename in data_dir:
            with open('../data/' + filename) as f:
                flights = json.loads(f.read())
                data = flights.pop(0)
            # 这里认为第一次读取时data中坐标不会改变 后面get_data再进行相关操作
            self.__min = data['range'][0]
            self.__max = data['range'][1]
            for flight in flights:
                if flight['flight_number'] not in self.__flights:
                    self.__flights[flight['flight_number']] = {}
                    self.__flights[flight['flight_number']]['latitude'] = [flight['latitude']]
                    self.__flights[flight['flight_number']]['longitude'] = [flight['longitude']]
                    self.__flights[flight['flight_number']]['heading'] = [flight['heading']]
                    self.__flights[flight['flight_number']]['n'] = [self.__n]
                else:
                    self.__flights[flight['flight_number']]['latitude'].append(flight['latitude'])
                    self.__flights[flight['flight_number']]['longitude'].append(flight['longitude'])
                    self.__flights[flight['flight_number']]['heading'].append(flight['heading'])
                    self.__flights[flight['flight_number']]['n'].append(self.__n)
            self.__n += 1
        self.__latest_file = data_dir[-1]

    def get_data(self):
        data_dir = os.listdir('../data')
        data_dir.sort()
        data_dir = data_dir[data_dir.index(self.__latest_file) + 1:]
        for filename in data_dir:
            with open('../data/' + filename) as f:
                flights = json.loads(f.read())
                data = flights.pop(0)
            for flight in flights:
                if flight['flight_number'] not in self.__flights:
                    self.__flights[flight['flight_number']]['latitude'] = [flight['latitude']]
                    self.__flights[flight['flight_number']]['longitude'] = [flight['longitude']]
                    self.__flights[flight['flight_number']]['heading'] = [flight['heading']]
                    self.__flights[flight['flight_number']]['n'] = [self.__n]
                else:
                    self.__flights[flight['flight_number']]['latitude'].append(flight['latitude'])
                    self.__flights[flight['flight_number']]['longitude'].append(flight['longitude'])
                    self.__flights[flight['flight_number']]['heading'].append(flight['heading'])
                    self.__flights[flight['flight_number']]['n'].appned(self.__n)
            self.__n += 1
        self.__latest_file = data_dir[-1]

    def draw(self):
        for flight in self.__flights:
            plt.quiver(self.__flights[flight]['longitude'], self.__flights[flight]['latitude'], 1, 1,
                       [int(i / self.__n * 255) for i in self.__flights[flight]['latitude']],
                       angles=self.__flights[flight]['heading'], units='dots', pivot='mid')

            plt.plot(self.__flights[flight]['longitude'], self.__flights[flight]['latitude'], label=flight)
        # plt.xlim(self.__min[0], self.__max[0])
        # plt.ylim(self.__min[1], self.__max[1])
        plt.legend()
        plt.show()

    def spin(self, loc, rng, interval):
        c = self.update_settings(loc, rng, interval)
        if c:
            self.get_data()
        self.draw()

    def update_settings(self, loc, rng, interval):
        c = True
        if self.__loc != loc or self.__rng != rng:
            self.reload()
            # return的checker 表示reload过了 此次spin跳过get_data
            c = False
        self.__loc = loc
        self.__rng = rng
        if __name__ == '__main__':
            self.__interval = interval
        else:
            self.__interval = interval.value
        return c


if __name__ == '__main__':
    p = Plotter()
    p.spin(0, 0, 0)