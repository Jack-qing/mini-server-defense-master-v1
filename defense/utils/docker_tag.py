# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:

import requests
from bs4 import BeautifulSoup


def get_tags(image_name: str):
    """
    获取镜像所有标签的爬虫函数，使用requests请求hub.docker.com，使用BeautifulSoup提取页面信息
    :param image_name: 镜像名称，例如：darksheer/ubuntu、ubuntu、ubuntu:latest（不支持含有两个/的镜像名字）
    :return:所有标签，数据形如{'Tag Name': ['latest'...]}
    """
    # 传入镜像名字处理
    image_name = image_name.split(':')[0]
    # 拼接请求的url
    if '/' in image_name:
        url = 'https://hub.docker.com/r/{}/tags/'.format(image_name)
    else:
        url = 'https://hub.docker.com/r/library/{}/tags/'.format(image_name)
    # 发送请求
    resp = requests.get(url=url)
    # 获取返回的页面
    html = resp.content.decode()

    # 初始化BeautifulSoup
    soup = BeautifulSoup(html, features=r"lxml")
    # 提取含有标签名的元素
    tags_list = soup.find_all('div', attrs={
        'class': 'FlexTable__flexItem___3vmPs FlexTable__flexItemPadding___2mohd FlexTable__flexItemGrow2___3I1KN'})
    # 处理数据，组成列表
    tags = []
    for tag in tags_list:
        tags.append(tag.text)
    # 处理数据，组成字典，形如{'Tag Name': ['latest']}
    return {tags[0]:tags[1:]}
