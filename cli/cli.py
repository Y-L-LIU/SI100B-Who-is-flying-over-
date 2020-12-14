import os
import logging
import multiprocessing as mp
from ..data_source.fr24_crawler import Fr24Crawler
from ..state import State


def _main():
    while True:
        ipt = input().split()
        if not ipt:
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
                    interval.value = float(interval)
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
                print('Work Interval: ', interval)
                continue
            # 显示led mode
            if ipt[1] in ['enabled', 'enable', 'mode', 'led', 'led_mode']:
                out = ['Off', 'Off', 'Off']
                for i in range(3):
                    if enabled[i]:
                        out[i] = 'On'
                print('LED Display:\n\t# of Flights: ', out[0], '\n\tTaking Off: ', out[1], '\n\tLanding: ', out[2])
        print('Invalid syntax!')


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
            os.kill(ppid)
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
                os.kill(ppid)
        # crawler
        else:
            try:
                crawler = Fr24Crawler()
                crawler.spin(loc, rng, interval)
            except KeyboardInterrupt:
                # The process is being killed, let the child process exit.
                logger.warning("Crawler exits.")
                os.kill(pid)
                os.kill(crawler_pid)


# 初始化共享内存
loc = mp.Array('d', (31.17940, 121.59043))
rng = mp.Array('d', (32.67940, 120.09043))
interval = mp.Value('d', 5.0)
enabled = mp.Array('i', (1, 1, 1))

if __name__ == "__main__":
    logger = logging.getLogger("si100b_proj:main")
    logger.setLevel("INFO")
    cli_start(logger)
