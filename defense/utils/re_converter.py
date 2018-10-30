# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:

from werkzeug.routing import BaseConverter


# 自定义转换器
class ReConverter(BaseConverter):
    """自定义的支持传入正则表达式的转换器"""

    def __init__(self, url_map, *args):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 将传入进来的参数args (是我们在route中定义的正则表达式)保存到对像的是regex属性中
        self.regex = args[0]  # [0]就是我们定义的正则表达式

    def to_python(self, value):
        """从正则表达式提取参数，经过to_python的调用，将调用的结果返回，再传给视图函数"""
        pass

    def to_url(self, value):
        pass