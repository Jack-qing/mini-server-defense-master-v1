# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:

import redis

# 工程配置信息
class Config(object):
    """工程的配置信息"""
    CACHE_TYPE = 'simple'
    SECRET_KEY = "xhosido*F(DHSDF*D(SDdslfhdos"

    # redis
    REDIS_HOST = "192.168.3.66"
    REDIS_PORT = 6379

# 开发者模式
class DeveLopmentConfig(Config):
    DEBUG = True


# 生产模式快
class ProductionConfig(Config):
    pass


config_dict = {
    "develop": DeveLopmentConfig,
    "product": ProductionConfig,
}