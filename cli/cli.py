import os, signal
import sys
import json
import shutil
import logging
import multiprocessing as mp
sys.path.append('..')
from data_source.fr24_crawler import Fr24Crawler
from state import State


def _help():
    print('可用指令及用法：\n'
          '\tset \t修改全局变量\t\t\tset parm args\n'
          '\tshow\t查看全局变量\t\t\tshow parm\n'
          '\thelp\t查看帮助\t\t\t\thelp (cmd)\n'
          '\tload\t读取最新文件\t\t\tload\n'
          '\tdata\t显示读取后的文件中的数据\tdata (fields)\n'
          '全局变量及格式：\n'
          '\tloc\t\t\t搜索中心坐标\t\tlatitude longitude\n'
          '\trng\t\t\t搜索区域西北角坐标\tlatitude longitude\n'
          '\tinterval\t工作间隔\t\t\tseconds\n'
          '\tenabled \tLED显示模式\t\ton/off on/off on/off\n'
          '数据关键字：\n'
          '\tlongitude\t\t\t经度\n'
          '\tlatitude\t\t\t纬度\n'
          '\theading\t\t\t\t航向\n'
          '\taltitude\t\t\t高度\n'
          '\tground_speed\t\t地速\n'
          '\tsquawk_number\t\t应答机编码\n'
          '\tregistration_number\t国籍注册号\n'
          '\tflight_number\t\t航班号\n'
          '\tdeparture_airport\t始发机场\n'
          '\tarrival_airport\t\t目的机场\n'
          '\tvertical_speed\t\t垂直速度')


def _main():
    f = None
    while True:
        ipt = input().split()
        if not ipt:
            continue
        if ipt[0] in ['help', '?']:
            if len(ipt) == 1:
                _help()
                continue
            if len(ipt) > 2:
                print('Too many fields!')
                continue
            if ipt[1] == 'set':
                print('set \t修改全局变量\tset parm args')
                continue
            if ipt[1] == 'show':
                print('show\t查看全局变量\tshow parm')
                continue
            if ipt[1] == 'help':
                print('help\t查看帮助\thelp (cmd)')
                continue
            if ipt[1] == 'load':
                print('load\t读取最新文件\tload')
                continue
            if ipt[1] == 'data':
                print('data\t显示读取后的文件中的数据\tdata (fields)')
                continue
            print('No such command!')
            continue
        if ipt[0] == 'set':
            if len(ipt) < 3:
                print('Not enough fields!')
                continue
            # 修改loc
            if ipt[1] in ['loc', 'location', 'coord', 'coordinate', 'coordinates']:
                if len(ipt) == 3:
                    print('Not enough fields!')
                    continue
                if len(ipt) > 4:
                    print('Too many fields!')
                    continue
                # syntax正确：
                temp = loc[0]
                try:
                    loc[0] = float(ipt[2])
                except ValueError:
                    print('Invalid value!')
                    continue
                try:
                    loc[1] = float(ipt[3])
                except ValueError:
                    print('Invalid value!')
                    # reverse the change in case last one was successful
                    loc[0] = temp
                continue
            # 修改rng
            if ipt[1] in ['rng', 'range', 'corner']:
                if len(ipt) == 3:
                    print('Not enough fields!')
                    continue
                if len(ipt) > 4:
                    print('Too many fields!')
                    continue
                # syntax正确：
                temp = rng[0]
                try:
                    rng[0] = float(ipt[2])
                except ValueError:
                    print('Invalid value!')
                    continue
                try:
                    rng[1] = float(ipt[3])
                except ValueError:
                    print('Invalid value!')
                    # reverse the change in case last one was successful
                    rng[0] = temp
                continue
            # 修改interval
            if ipt[1] in ['interval', 'itv', 'frequency', 'freq']:
                if len(ipt) > 4:
                    print('Too many fields!')
                    continue
                # syntax正确：
                try:
                    interval.value = float(ipt[2])
                except ValueError:
                    print('Invalid value!')
                continue
            # 修改led的mode
            if ipt[1] in ['enabled', 'enable', 'mode', 'led', 'led_mode']:
                if len(ipt) < 5:
                    print('Not enough fields!')
                    continue
                if len(ipt) > 5:
                    print('Too many fields!')
                    continue
                # syntax正确：
                temp = enabled[0]
                temp1 = enabled[1]
                if ipt[2] in ['on', 'On', 'true', 'True', '1']:
                    enabled[0] = 1
                elif ipt[2] in ['off', 'Off', 'false', 'False', '0']:
                    enabled[0] = 0
                else:
                    print('Invalid value!')
                    continue
                if ipt[3] in ['on', 'On', 'true', 'True', '1']:
                    enabled[1] = 1
                elif ipt[3] in ['off', 'Off', 'false', 'False', '0']:
                    enabled[1] = 0
                else:
                    print('Invalid value!')
                    enabled[0] = temp
                    continue
                if ipt[4] in ['on', 'On', 'true', 'True', '1']:
                    enabled[2] = 1
                elif ipt[4] in ['off', 'Off', 'false', 'False', '0']:
                    enabled[2] = 0
                else:
                    print('Invalid value!')
                    enabled[0] = temp
                    enabled[1] = temp1
                continue
        if ipt[0] == 'show':
            if len(ipt) == 1:
                print('Not enough fields!')
                continue
            if len(ipt) > 2:
                print('Too many fields!')
                continue
            # 显示loc
            if ipt[1] in ['loc', 'location', 'coord', 'coordinate', 'coordinates']:
                print('Coordinate: ', loc[0], ', ', loc[1])
                continue
            # 显示rng
            if ipt[1] in ['rng', 'range', 'corner']:
                print('NW Corner Coordinate: ', rng[0], ', ', rng[1])
                continue
            # 显示interval
            if ipt[1] in ['interval', 'itv', 'frequency', 'freq']:
                print('Work Interval: ', interval.value)
                continue
            # 显示led mode
            if ipt[1] in ['enabled', 'enable', 'mode', 'led', 'led_mode']:
                out = ['Off', 'Off', 'Off']
                for i in range(3):
                    if enabled[i]:
                        out[i] = 'On'
                print('LED Display:\n\t# of Flights: ', out[0], '\n\tTaking Off: ', out[1], '\n\tLanding: ', out[2])
                continue
        if ipt[0] == 'load':
            if len(ipt) > 1:
                print('Too many fields!')
                continue
            data_dir = os.listdir('data')
            with open('data/' + max(data_dir)) as f:
                filedata = f.read()
            print('Loaded {} with {} flight(s).'.format(max(data_dir), len(filedata) - 1))
            continue
        if ipt[0] == 'data':
            flights = json.loads(filedata)
            data = flights.pop(0)
            f.close()
            f = open
            if len(ipt) == 1:
                for i in data:
                    print(i, ':', data[i])
                lines = ''
                for flight in flights:
                    for i in flight:
                        lines += str(i) + ':' + str(flight[i]) + '\t'
                    lines += '\n'
                print(lines)
                continue
            for i in ipt[1:]:
                if i not in flights[0]:
                    print('"{}" is not a valid field!'.format(i))
                    continue
            for i in data:
                print(i,':',data[i])
            lines = ''
            for flight in flights:
                for i in flight:
                    if i in ipt[1:]:
                        lines += str(i) + ':' + str(flight[i]) + '\t'
                lines += '\n'
            print(lines)
            continue
        print('Invalid syntax!\n'
              'For help, type help or ?')


def _draw():
    """
    Function `_main`:

    Implement your chart rendering in this function.
    """
    while True:
        pass


def cli_start(logger):
    pid = os.fork()
    # 主进程：CLI
    if pid == 0:
        ppid = os.getppid()
        try:
            _main()
        except KeyboardInterrupt:
            os.kill(ppid, signal.SIGINT)
    # 子进程：crawler/state
    else:
        crawler_pid = os.fork()
        # state
        if crawler_pid == 0:
            ppid = os.getppid()
            try:
                state = State()
                state.spin(enabled, interval)
            except KeyboardInterrupt:
                # 退出时删除生成的所有json文件
                shutil.rmtree('data')
                os.mkdir('data')
                os.kill(ppid, signal.SIGINT)
        # crawler
        else:
            try:
                crawler = Fr24Crawler()
                crawler.spin(loc, rng, interval)
            except KeyboardInterrupt:
                # The process is being killed, let the child process exit.
                logger.warning("Crawler exits.")
                os.kill(pid, signal.SIGINT)
                os.kill(crawler_pid, signal.SIGINT)


# 初始化共享内存
loc = mp.Array('d', (31.17940, 121.59043))
rng = mp.Array('d', (32.67940, 120.09043))
interval = mp.Value('d', 5.0)
enabled = mp.Array('i', (1, 1, 1))

if __name__ == "__main__":
    # logger = logging.getLogger("si100b_proj:main")
    # logger.setLevel("INFO")
    # cli_start(logger)
    _help()
