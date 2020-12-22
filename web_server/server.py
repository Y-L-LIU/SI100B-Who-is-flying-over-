    # // 需要导入的package
import json
import os, io, time, shutil, sys, signal
sys.path.append('..')
from data_source.fr24_crawler import Fr24Crawler 
from state import State
# //与系统设置有关的
from PIL import Image      
# //图像处理的包 
from flask import Flask, flash, request, redirect, url_for,jsonify,make_response, send_file
from flask_cors import CORS, cross_origin    
import multiprocessing as mp

#  //路由许可
UPLOAD_FOLDER = './img'     
# // 锁定目标文件夹
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}       
# //选择可用的格式 不可以全部允许因为有安全问题
# configuration
DEBUG = True
# //常规设计
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# enable CORS
cors = CORS(app, resources={r'/*': {'origins': '*'}},supports_credentials=True)      
# //很关键 允许外界请求


def start(logger):
    pid = os.fork()
    # 主进程：WEB
    if pid == 0:
        ppid = os.getppid()
        try:
            app.run(host='0.0.0.0', port=5000)
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
                os.kill(ppid,signal.SIGINT)
        # crawler
        else:
            try:
                crawler = Fr24Crawler()
                crawler.spin(loc, rng, enabled,interval)
            except KeyboardInterrupt:
                # The process is being killed, let the child process exit.
                logger.warning("Crawler exits.")
                os.kill(pid, signal.SIGINT)
                os.kill(crawler_pid, signal.SIGINT)

    # 初始化共享内存
# //获取当前目录
loc = mp.Array('d', (31.17940, 121.59043))
rng = mp.Array('d', (32.67940, 120.09043))
interval = mp.Value('d', 5)
enabled = mp.Array('i', (1, 1, 1))

@app.route('/',methods=['GET', 'POST'])
def _try():
    if request.method == 'GET':
        return send_file('index.html')
    elif request.method == 'POST':
        def deal(content):
            content = content[1:-1]
            li = content.split(',')
            li1 = []
            for i in range(2):
                li1.append(int(li[i]))
            return (li1[0],li1[1])
        di = request.json
        center = deal(di['Center'])
        eastwest =deal(di['Northeast'])
        time = int(di['time'])
        select = di['Item']
        
    #设置全局变量
        loc = mp.Array('d', center)
        rng = mp.Array('d', eastwest)
        interval = mp.Value('d', time)
    #判断模式以获得enabled的值， 然后开始多线程
        if select == "Amount." :
            dir0 = 'static/img/amount.png'
            enabled = mp.Array('i', (1,0 ,0))
        elif select == "Landing.":
            dir0 = 'static/img/landing.png'
            enabled = mp.Array('i', (0, 1, 0))
        elif select == "Taking off.":
            dir0 = 'static/img/takingoff.png'
            enabled = mp.Array('i', (0, 0, 1))
        elif select == "All displayed.":
            dir0 = 'static/img/amount.png'
            enabled = mp.Array('i', (1, 1, 1))

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, dir0)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # f.save(upload_path)
        image_data = open(upload_path, "rb").read()
        img_stream = io.BytesIO(image_data)
        img = Image.open(img_stream)
        imgByteArr = io.BytesIO()
        img.save(imgByteArr,format='PNG')
        imgByteArr = imgByteArr.getvalue()
        response = make_response(imgByteArr)
        response.headers['Content-Type'] = 'image/png'
        return response

# @app.route('/#/Use1',methods=['GET', 'POST'])
# def findpic(): 
    # method = request.method
    # res = make_response(jsonify(token=123456, gender=0, method = method))  # 设置响应体
    # res.status = '200'# 设置状态码
    # res.headers['Access-Control-Allow-Origin'] = "*"# 设置允许跨域
    # res.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    # return res  

    # return render_template('upload.html')

