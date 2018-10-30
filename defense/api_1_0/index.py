# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日11时
# 说明:
# 总结:

from . import api

from flask import current_app


@api.route("/index")
def index():
    # logging.error("fhdsof")  # 错误级别
    # logging.warn("")  # 警告级别
    # logging.info("")  # 消息提示级别
    # logging.debug()  # 调试级别
    current_app.logger.error("error msg")
    current_app.logger.warn("warn msg")
    current_app.logger.info("info msg")
    current_app.logger.debug("debug msg")
    return "index page"