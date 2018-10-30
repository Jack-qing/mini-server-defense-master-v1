# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:
from . import api
from flask import Flask, request, jsonify
import os
import threading
import json
import docker
from defense.utils.db_valu import func_Grade, pages, json_time
from defense.utils.docker_tag import get_tags
from defense.utils.re_converter import ReConverter
from defense.utils.response_code import RET
from flask_cors import cross_origin

# from page_utils import Pagination
app = Flask(__name__)
app.url_map.converters["re"] = ReConverter

progress_dict = {}


# 192.168.3.53:5000/?name=java:latest
@api.route("/")
@cross_origin()
def defense_scanner_linux():
    name = request.args.get("name")
    if ':' not in name:
        name = name + ':latest'
    file_name = name.replace('/', '@')
    docker_connection = docker.Client(base_url='unix:///var/run/docker.sock')
    print(name)
    docker_search = docker_connection.images(name)
    if not docker_search:
        return jsonify({'cod': RET.NODATA, 'imageName': 'docker not image'})
    clair_scanner = "clair-scanner_darwin_amd64 --ip 192.168.3.66  --report=./defense_scanner_json/{}.json {}".format(
        file_name, name)
    filePath = "./defense_scanner_json/{}.json".format(file_name)

    def read_JSON():
        with open(filePath, "r", encoding="utf-8") as file:
            out_clair = json.load(file)
            leve_dict = func_Grade(out_clair)
            json_time_time = json_time(out_clair)
            out_clair['level'] = leve_dict
            out_clair['dockerImage'] = docker_search
            out_clair['json_time'] = json_time_time

        with open(filePath.format(file_name), "w", encoding="utf-8") as file:
            out_str = json.dumps(out_clair)
            # out_str = re.sub("\s", "", out_str)
            file.write(out_str + '\n')
        return out_clair

    if os.path.exists(filePath):
        out_clair = read_JSON()
        return jsonify(out_clair)
    else:
        os.system(clair_scanner)
        if os.path.exists(filePath):
            out_clair = read_JSON()
            return jsonify(out_clair)
        else:
            return jsonify({'cod': RET.PARAMERR, "dockerImage": "No features have been detected in the image"})


# 192.168.3.53:5000/deljson?filename=images:json
@api.route('/deljson', methods=['GET'])
def delete_json():
    if request.method == 'GET':
        filename = request.args.get('filename')
        try:
            if os.path.exists("./defense_scanner_json/{}.json".format(filename)):
                os.remove("./defense_scanner_json/{}.json".format(filename))
                return jsonify({'cod': RET.OK, 'dockerFile': ''})
            else:
                return jsonify({'cod': RET.NODATA, 'dockerFile': 'file not exist'})
        except Exception as a:
            return jsonify({'cod': RET.DATAERR, 'dockerFile': 'file deleted error'})
    else:

        return jsonify({'cod': RET.PARAMERR, 'dockerFile': 'method not allowed'})


# DELELE
# 192.168.3.53/delete
'''
{
        "repotags": "jack777/defense-scanner:1.0",
        "size": 328973675
 }
 '''


@api.route('/delete', methods=['DELETE'])
@cross_origin()
def delete_file():
    if request.method == 'DELETE':
        filename = request.get_json()
        repotags = filename.get("repotags")
        docker_connection = docker.Client(base_url='unix:///var/run/docker.sock')
        try:
            docker_connection.remove_image(repotags)
        except:
            return jsonify({'cod': RET.NODATA, "dockerDelete": "NO DATA"})

        return jsonify({'cod': RET.OK, "dockerImageDelete": "OK"})
    else:
        return jsonify({'cod': RET.REQERR, 'dockerDelete': 'method not allowed'})


@api.route('/search')
@cross_origin()
def search_name():
    name = request.args.get('name')
    docker_connection = docker.Client(base_url='unix:///var/run/docker.sock')
    storage_space = docker_connection.images()
    ret_list = []
    for loadfont_docker in storage_space:
        ret_varet = loadfont_docker['RepoTags'][0]
        ret_vare = loadfont_docker["Size"]
        if ret_varet.startswith(name):
            ret_list.append({"repotags": ret_varet, "size": ret_vare})
    return jsonify(ret_list)


def download_images(docker_connection, name_pull):
    detail_dict = {}
    for line in docker_connection.pull(name_pull, decode=True, stream=True):
        if name_pull in progress_dict.keys():
            progress_dict.pop(name_pull)
            with open('./detail/{}'.format(name_pull), 'w') as file:
                file.write(str(0))
            return
        pull_status = line.get("status")
        pull_id = line.get("id")
        pull_detail = line.get("progressDetail")
        if pull_status == "Downloading":
            detail_dict[pull_id]['current'] = detail_dict[pull_id]['total'] * (
                    pull_detail['current'] / pull_detail['total'])
            detail = 0
            for d in detail_dict.values():
                detail += d['current'] / d['total']
            detail = "%.3f%%" % (detail / len(detail_dict) * 100)

            with open('./detail/{}'.format(name_pull), 'w') as file:
                file.write(str(detail))

        if pull_status == "Download complete":
            detail_dict[pull_id]['current'] = detail_dict[pull_id]['total']
            detail = 0
            for d in detail_dict.values():
                detail += d['current'] / d['total']
            detail = "%.3f%%" % (detail / len(detail_dict) * 100)
            with open('./detail/{}'.format(name_pull), 'w') as file:
                file.write(str(detail))

        if pull_status == "Pulling fs layer":
            detail_dict[pull_id] = {'current': 0, 'total': 100}

    with open('./detail/{}'.format(name_pull), 'w') as file:
        file.write('docker pull complete')


# 192.168.3.53:5000/image_pull?name=java
@api.route("/images_pull")
@cross_origin()
def docker_images_pull():
    name_pull = request.args.get("name")
    if ":" not in name_pull:
        name_pull = name_pull + ":latest"
    docker_connection = docker.Client(base_url='unix:///var/run/docker.sock')
    try:
        t = threading.Thread(target=download_images, args=(docker_connection, name_pull,))
        t.start()
        return jsonify({'cod': RET.OK, "dockerPull,Downloading": "downloading"})
    except Exception as e:
        return jsonify({'cod': RET.DBERR, "message": "manifest for  not found Error"})


# 192.168.3.53:5000/progress?name=java
@api.route("/progress")
@cross_origin()
def docker_images_detail():
    name_pull = request.args.get("name")
    if ":" not in name_pull:
        name_pull = name_pull + ":latest"
    if os.path.exists('./detail/{}'.format(name_pull)):
        with open('./detail/{}'.format(name_pull), 'r') as file:
            value = file.read()
    else:
        value = '0'

    return jsonify({'cod': RET.OK, "image": name_pull, 'detail': value})


# 192.168.3.53:5000/stop?name=java
@api.route("/stop")
@cross_origin()
def docker_images_stop():
    name_pull = request.args.get("name")
    if ":" not in name_pull:
        name_pull = name_pull + ":latest"
    progress_dict[name_pull] = 'stop'

    return jsonify({'cod': RET.OK, "image": name_pull, 'stop': 'ok'})



# 192.168.3.53:5000/storage?page=1
@api.route("/storage")
@cross_origin()
def docker_loadfont():
    page_storage = request.args.get('page')
    try:
        page_storage = int(page_storage)
    except:
        return jsonify({'cod': RET.NODATA, "storageImagePage": "error"})
    docker_connec = docker.Client(base_url='unix:///var/run/docker.sock')
    storage_space = docker_connec.images()
    ret_list = []
    for loadfont_docker in storage_space:
        ret_varet = loadfont_docker['RepoTags'][0]
        ret_vare = loadfont_docker["Size"]
        ret_list.append({"repotags": ret_varet, "size": ret_vare})
        pages_storage, pages_num, page_num = pages(page_storage, 10, ret_list, [])
        data = {
            'page': page_num,
            'count': pages_num,
            'data': pages_storage
        }
    res = dict(Mirror_list=data)
    return jsonify(res)


# 192.168.3.53:5000/images?image_name=redis:latest
@api.route("/images")
@cross_origin()
def docker_tag():
    image_name = request.args.get('image_name')
    if not image_name or len(image_name.split('/')) > 2:
        return jsonify({'cod': RET.PARAMERR, "tag images": "Parameter error"})
    data = get_tags(image_name)
    return jsonify(data)


# 192.168.3.53:5000/pages/ubuntu:latest?page=2
@api.route('/pages/<username>')
@cross_origin()
def page_vulnerabicity(username):
    page_page = request.args.get('page')
    try:
        page_page = int(page_page)
    except:
        return jsonify({'cod': RET.NODATA, "imagePage": "error"})
    if os.path.exists("./defense_scanner_json"):
        with open("./defense_scanner_json/{}.json".format(username), "r", encoding="utf-8") as file:
            out_json = json.load(file)
            unapproved = out_json['vulnerabilities']
            page_list, pages_num, page_num = pages(page_page, 6, unapproved, [])
            data = {
                'page': page_num,
                'count': pages_num,
                'data': page_list
            }
            return jsonify(data)


@api.route('pause/')
@cross_origin()
def pause_container():
    pauses = request.args.get('name')
    docker_connection = docker.Client(base_url='unix:///var/run/docker.sock')
    docker_pause = docker_connection.pause(pauses)
    print("+++====")
    print(docker_pause)
    # return jsonify({'cod': RET.NODATA, "dockerPause": "NO DATA"})
    return jsonify({'cod': RET.OK, "dockerPause": "OK"})


@api.route('unpause/')
@cross_origin()
def Unpause_container():
    unpauses = request.args.get('name')
    docker_connection = docker.Client(base_url='unix:///var/run/docker.sock')
    docker_unpause = docker_connection.pause(unpauses)
    print("------")
    print(docker_unpause)
    # return jsonify({'cod': RET.NODATA, "dockerUnPause": "NO DATA"})
    return jsonify({'cod': RET.OK, "dockerUnPause": "OK"})
