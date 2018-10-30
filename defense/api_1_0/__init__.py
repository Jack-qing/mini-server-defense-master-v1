# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:

from flask import Blueprint

# 蓝图
api = Blueprint("api_1_0", __name__)

# 在__init__.py执行的时候，把视图加载进来，让蓝图与应用程序知道视图存在

from . import scanner, index