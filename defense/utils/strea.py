# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年10月23日13时
# 说明:
# 总结:

from functools import update_wrapper
from flask import Response, current_app


class StreamView(object):
    """A decorator for flask view."""

    def __init__(self, view_function):
        self.view_function = view_function
        update_wrapper(self, self.view_function)

    def __call__(self, *args, **kwargs):
        return_value = self.view_function(*args, **kwargs)
        try:
            response = iter(return_value)
        except TypeError:
            # the return value is not iterable
            response = return_value
            current_app.logger.warning(
                "The stream view %r isn't iterable." % self)
        else:
            # the return value is iterable
            response = Response(return_value, direct_passthrough=True)
        return response


stream_view = StreamView