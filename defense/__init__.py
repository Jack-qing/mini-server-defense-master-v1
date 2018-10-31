# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:
# 设置日志的记录等级
import logging
import redis
from flask import Flask, render_template
from logging.handlers import RotatingFileHandler
from config import config_dict
from defense.utils.re_converter import ReConverter

# 构建redis连接对象
redis_store = None

logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log.log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


# 为flask补充csrf防护机制
# csrf = CSRFProtect(app)

# socketio初始化
# socketio = SocketIO()
cache = Cache()

def create_app(config_name):
    u'''工厂模式'''

    app = Flask(__name__)

    conf = config_dict[config_name]
    # 设置flask 信息
    app.config.from_object(conf)

    # socketio.init_app(app)
    cache.init_app(app)


    # 初始化redis_store
    global redis_store
    redis_store = redis.StrictRedis(host=conf.REDIS_HOST, port=conf.REDIS_PORT)



    # 向app中添加自定义的路由转换器
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    # import defense.api_1_0
    from defense import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1_0")

    # 提供html静态文件的蓝图
    #    import defense.web_html
    #    app.register_blueprint(web_html.html)

    return app
