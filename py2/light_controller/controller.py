#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#


from gpiozero import LED
from time import sleep


class BaseController:

    def __init__(self):
        self.blue1 = LED(19)
        self.blue2 = LED(26)

    def work_once(self):  # 代表一次完整流程的结束,双灯快闪4次
        i = 0
        sleep(0.5)
        while i < 4:
            i = i + 1
            self.blue1.on()
            self.blue2.on()
            sleep(0.1)
            self.blue1.off()
            self.blue2.off()
            sleep(0.1)
        sleep(0.5)

    def on(self, code):  # 打开某个led灯,参数为灯的编号
        i = code
        if code == 1:
            self.blue1.on()
        elif code == 2:
            self.blue2.on()

    def off(self, code):  # 关闭某个led灯,参数为灯的编号
        if code == 1:
            self.blue1.off()
        elif code == 2:
            self.blue2.off()

    def separated(self):  # 代表显示数据的间隔，双灯快闪2次
        i = 0
        sleep(0.5)
        while i < 2:
            i = i + 1
            self.blue1.on()
            self.blue2.on()
            sleep(0.1)
            self.blue1.off()
            self.blue2.off()
            sleep(0.1)
        sleep(0.5)

    def spark(self, code, data=None):  # 代表data次标准的闪烁,参数为灯的编号
        i = 0
        while i < data:
            i = i + 1
            self.on(code)
            sleep(0.1)
            self.off(code)
            sleep(0.1)

