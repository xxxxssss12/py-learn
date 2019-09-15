#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
from utils.logger import Logger
from utils.config_holder import ConfigHolder

log = Logger("info")
config_path = ""

try :
    config_path = sys.argv[1]
except :
    log.info("not input config_path, use default")

if 0 == len(config_path):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "devops_config.ini")
ConfigHolder.load(config_path)

from utils.db_model import AppConfigDo, ServiceConfigDo

app_config_list = AppConfigDo.select()
print("------请选择要部署的应用序号：")
for app_config_do in app_config_list:
    print("[%s] %s(%s)"%(app_config_do.id, app_config_do.app_name, app_config_do.app_desc))
choose_app_id = int(input("请选择: "))
print()

service_config_list = ServiceConfigDo.select().where(ServiceConfigDo.app_id == choose_app_id)
print("------请选择要部署的服务序号(逗号分隔)：")
for service_config_do in service_config_list:
    print("[%s] %s(%s)"%(service_config_do.id, service_config_do.service_id, service_config_do.service_desc))
choose_service_ids = input("请选择(逗号分隔): ")
print(choose_service_ids)
print()

choose_git_branch = input("------请选择要部署的GIT分支(默认master): ")
if choose_git_branch is None or len(choose_git_branch) == 0:
    choose_git_branch="master"
print(choose_git_branch)
print()

is_init_dir = input("------目录不存在是否初始化(0=否，1=是，默认初始化): ")
if is_init_dir is None or len(is_init_dir) == 0 :
    is_init_dir = 1
is_init_dir = int(is_init_dir)
if is_init_dir > 1:
    is_init_dir = 1
if is_init_dir < 0:
    is_init_dir = 0
print(is_init_dir)
print()

