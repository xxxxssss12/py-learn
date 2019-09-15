from peewee import *
from utils.config_holder import *
from utils.logger import Logger
log = Logger("info")

# 连接数据库
db_name = ConfigHolder.get("database", "db_name")
db_username = ConfigHolder.get("database", "username")
db_password = ConfigHolder.get("database", "password")
db_host = ConfigHolder.get("database", "host")
db_port = int(ConfigHolder.get("database", "port"))
db_charset = ConfigHolder.get("database", "charset")
db = MySQLDatabase(db_name, **{
        'user': db_username,
        'host': db_host,
        'port': db_port,
        'charset': db_charset,
        'use_unicode': True,
        'password': db_password
    })

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db

class AppConfigDo(BaseModel):
    app_name = CharField(max_length=255)
    app_desc = CharField(max_length=255)
    git_url = CharField(max_length=255)
    work_root_dir = CharField(max_length=255)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0)")])

    class Meta:
        table_name = 'tb_app_config'
    def __str__(self) :
        return "AppConfigDt[id=%s, app_name=%s, app_desc=%s, git_url=%s, work_root_dir=%s, create_time=%s, update_time=%s]"%(self.id, self.app_name,self.app_desc,self.git_url,self.work_root_dir,self.create_time,self.update_time)

#查询数据库是连接
log.info("db connect start...now status is %s" % (db.is_closed())) #返回false未连接
#连接数据库
db.connect()
log.info("db connect over...now status is %s" % (db.is_closed())) #返回true表示已连接
