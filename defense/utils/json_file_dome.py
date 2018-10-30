# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日10时
# 说明:
# 总结:

root_dir_path = "./defense_sucnner_json"
extern_name_list = [".json", ".ExportJson"]

import os
import re

def removeBlankChar(filepath):
    f1 = open(filepath, "r")
    content1 = f1.read()
    f1.close()

    content2 = re.sub("\s", "", content1)
    f2 = open(filepath, "w")
    f2.write(content2)
    f2.close()

    print( "remove blank char complete. file: %s" % filepath)
# end of removeBlankChar

def removeBlankCharOfDir(dirpath):
    filename_list = os.listdir(dirpath)
    for filename in filename_list:
        filepath = dirpath + "/" + filename
        if os.path.isdir(filepath):
            removeBlankCharOfDir(filepath)
        else:
            for extern_name in extern_name_list:
                if filepath[-len(extern_name):] == extern_name:
                    removeBlankChar(filepath)
                    break
# end of removeBlankCharOfDir

removeBlankCharOfDir(root_dir_path)
#raw_input("\n\ndone! ....")