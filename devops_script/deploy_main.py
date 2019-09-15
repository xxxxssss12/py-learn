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
    config_path = os.getcwd() + "/devops_config.ini"
ConfigHolder.load(config_path)

host = ConfigHolder.get("database", "host")

from utils.dao_model import AppConfigDo
appConfig = AppConfigDo.get(id=1)
print(appConfig.__str__())