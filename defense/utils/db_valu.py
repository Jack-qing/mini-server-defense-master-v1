# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:
import json
from flask import jsonify
import math, docker, time


def func_Grade(data):
    db_value = {"High": 0, "Medium": 0, "Low": 0, "Negligible": 0, "Unknown": 0}
    for db_list in data['vulnerabilities']:
        ret_value = db_list.get("severity")
        if ret_value == "High":
            db_value["High"] += 1
        elif ret_value == "Medium":
            db_value["Medium"] += 1
        elif ret_value == "Low":
            db_value["Low"] += 1
        elif ret_value == "Negligible":
            db_value["Negligible"] += 1
        elif ret_value == "Unknown":
            db_value["Unknown"] += 1
    return db_value


def pages(page: int, num_per_page: int, data: list, error_data):
    """
    分页函数
    :param error_data: 请求页码超出范围返回的数据
    :param page: 第几页
    :param num_per_page: 每页几条
    :param data: 被分页的数据
    :return: 分页结果/总页数/当前页码
    """
    # math.ceil计算出数据可以被分为几页
    pages_num = math.ceil(len(data) / num_per_page)

    # 判断提取的页数是否超出范围
    if page > pages_num:
        return error_data, pages_num, page
    else:
        # 未超出范围则切割数据
        # 计算切割的起始位置
        start_num = num_per_page * (page - 1)
        page_list = data[start_num:start_num + num_per_page]
        return page_list, pages_num, page


def json_time(times):
    now = int(round(time.time() * 1000))
    now2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
    return now2


def db_data_bash(docker_image):
    docker_connec = docker.Client(base_url='unix:///var/run/docker.sock')
    storage_space = docker_connec.images()
    print(storage_space)
    ret_list = []
    for loadfont_docker in storage_space:
        ret_containers = loadfont_docker["Containers"]
        ret_created = loadfont_docker["Created"]
        ret_id = loadfont_docker["Id"]
        ret_varet = loadfont_docker['RepoTags']
        ret_vare = loadfont_docker["Size"]
        ret_list.append(
            {"docker_image": docker_image, "id": ret_id, "created": ret_created, "containers": ret_containers,
             "repotags": ret_varet, "size": ret_vare})
    res = dict(docker_image_data=ret_list)
    return res


