# -*- coding: UTF-8 -*-

import configparser
from utils.logger import Logger

log = Logger("info")

class ConfigHolder:

    cf = configparser.ConfigParser()
    is_init = False

    @classmethod
    def load(self, absolut_path) :
        self.cf.read(absolut_path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        self.is_init = True

    @classmethod
    def get(self, section, key) :
        if not self.is_init:
            log.error("get " + section + "." + key + " error: config not init!")
            raise RuntimeError("config not init!")
        return self.cf.get(section, key)