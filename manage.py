# !/usr/bin/python3
# -*-coding:utf-8-*-
# @Author: Jack_zhu
# @Time: 2018年09月20日11时
# 说明:
# 总结:

from flask_migrate import Migrate
from flask_script import Manager
from defense import create_app

app = create_app("develop")

# 管理工具对象
manager = Manager(app)  # 管理app
Migrate(app)  # 迁移

if __name__ == '__main__':
    manager.run()
    # app.run("0.0.0.0", debug=True)
    # socketio.run(app, "0.0.0.0", debug=True)
