#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
from utils.logger import Logger
from utils.config_holder import ConfigHolder
from utils.env_holder import EnvHolder

EnvHolder.put("script.root.path", os.path.join(os.path.dirname(os.path.abspath(__file__))))

log = Logger("info")
config_path = ""

'''
try:
    config_path = sys.argv[1]
except:
    log.info("not input config_path, use default")
'''

if 0 == len(config_path):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "devops_config.ini")

ConfigHolder.load(config_path)

from utils.db_model import AppConfigDo, ServiceConfigDo

is_use_input_param = False
# param init
choose_app_id_str = sys.argv[1]
choose_service_ids = sys.argv[2]
deploy_git_branch = sys.argv[3]
is_init_dir = sys.argv[4]

choose_app_id = -1
# check is_use_input_param
if choose_app_id_str is not None and len(choose_app_id_str) > 0 \
        and choose_service_ids is not None and len(choose_service_ids) > 0 \
        and deploy_git_branch is not None and len(deploy_git_branch) > 0 \
        and is_init_dir is not None and len(is_init_dir) > 0:
    choose_app_id = int(choose_app_id_str)
    is_use_input_param = True
    print("无需手动输入参数了")

app_config_list = AppConfigDo.select()
app_config_map = {}
if not is_use_input_param:
    print("------请决定要部署的应用序号：")
    for app_config_do in app_config_list:
        print("[%s] %s(%s)" % (app_config_do.id, app_config_do.app_name, app_config_do.app_desc))
        app_config_map[app_config_do.id] = app_config_do
    choose_app_id = int(input("请选择: "))

choose_app_do = app_config_map[choose_app_id]

print("choose_app_do=%s" % choose_app_do.__str__())

service_config_list = ServiceConfigDo.select().where(ServiceConfigDo.app_id == choose_app_id)
service_config_map = {}
if not is_use_input_param:
    print("------请决定要部署的服务序号(逗号分隔)：")
    for service_config_do in service_config_list:
        print("[%s] %s(%s)" % (service_config_do.id, service_config_do.service_id, service_config_do.service_desc))
        service_config_map[service_config_do.id] = service_config_do
    choose_service_ids = input("请选择(逗号分隔): ")
print("choose_service_ids=%s" % choose_service_ids)
choose_service_idArr = choose_service_ids.split(",")
choose_service_do_list = []
for choose_service_id in choose_service_idArr:
    if choose_service_id is not None and len(choose_service_id) > 0:
        choose_service_do_list.append(service_config_map[int(choose_service_id)])
print()

if not is_use_input_param:
    deploy_git_branch = input("------请决定要部署的GIT分支(默认master): ")
if deploy_git_branch is None or len(deploy_git_branch) == 0:
    deploy_git_branch = "master"
print("deploy_git_branch=%s" % deploy_git_branch)
print()

if not is_use_input_param:
    is_init_dir = input("------请决定目录不存在是否初始化(0=否，1=是，默认初始化): ")
if is_init_dir is None or len(is_init_dir) == 0:
    is_init_dir = 1
is_init_dir = int(is_init_dir)
if is_init_dir > 1:
    is_init_dir = 1
if is_init_dir < 0:
    is_init_dir = 0
print("is_init_dir=%s" % is_init_dir)
print()

from deploy_executor import DeployExecutor

executor = DeployExecutor(choose_app_do, choose_service_do_list, deploy_git_branch, is_init_dir)
executor.do_deploy()
