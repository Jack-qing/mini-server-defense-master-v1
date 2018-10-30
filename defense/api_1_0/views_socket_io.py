#!/usr/bin/env python
# encoding: utf-8 
# @version: 
# @author: liduo
# @license: 
# @file: socket.py
# @time: 2018/5/20 下午4:05
from defense import socketio as socket_io
from flask import request
from flask_socketio import emit

import json, time
import docker
from defense.utils.response_code import RET


def docker_pull(to_sid, docker_name):
    if ":" not in docker_name:
        docker_pull = docker_name + ":latest"
    else:
        docker_pull = docker_name
    docker_connection = docker.Client(base_url='unix:///var/run/docker.sock')
    try:
        detail_dict = {}
        for line in docker_connection.pull(docker_pull, decode=True, stream=True):
            pull_status = line.get("status")
            pull_id = line.get("id")
            pull_detail = line.get("progressDetail")
            if pull_status == "Downloading":
                detail_dict[pull_id]['current'] = detail_dict[pull_id]['total'] * (
                        pull_detail['current'] / pull_detail['total'])
                detail = 0
                for d in detail_dict.values():
                    detail += d['current'] / d['total']
                detail = detail / len(detail_dict.keys())
                data = json.dumps({'cod': RET.OK, 'image': docker_pull, 'detail': detail})
                emit(docker_name, data, broadcast=True)
            if pull_status == "Download complete":
                detail_dict[pull_id]['current'] = detail_dict[pull_id]['total']
                detail = 0
                for d in detail_dict.values():
                    detail += d['current'] / d['total']
                detail = detail / len(detail_dict.keys())
                data = json.dumps({'cod': RET.OK, 'image': docker_pull, 'detail': detail})
                emit(docker_name, data, broadcast=True)
            if pull_status == "Pulling fs layer":
                detail_dict[pull_id] = {'current': 0, 'total': 100}

        data = json.dumps({'cod': RET.DATAEXIST, "dockerPull,LocalAlready": "local"})
        emit(docker_name, data, broadcast=True)
    except Exception as e:
        data = json.dumps({'cod': RET.DBERR, "dockerPull": "error"})
        emit(docker_name, data, broadcast=True)


@socket_io.on('connect', namespace='/pull_images')
# socket_io必须有connect
def connect():
    print('socket已连接')


@socket_io.on('pull_images', namespace='/pull_images')
def pull_images(data):
    docker_name = data.get('name')
    sid = request.sid
    # print('pull_images')
    # print(docker_name)
    # print(sid)
    docker_pull(sid, docker_name)
