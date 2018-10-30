# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:

# 工程配置信息
class Config(object):

    pass


# 开发者模式
class DeveLopmentConfig(Config):
    DEBUG = True


# 生产模式快
class ProductionConfig(Config):
    pass


config_dict = {
    "develop": DeveLopmentConfig,
}