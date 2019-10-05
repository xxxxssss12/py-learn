import os
from utils.logger import Logger
from utils.config_holder import ConfigHolder
from utils.db_model import AppConfigDo, ServiceConfigDo
from utils.env_holder import EnvHolder
import utils.zip_util as ZipUtils
from utils.file_utils import FileUtil
import datetime
log = Logger("info", name="deploy_executor")

class DeployExecutor:
    # 入参：1根目录；2git仓库url；3项目名称 4git所属分支(默认master)
    gitctrl_cmd = "/usr/local/bin/git_ctrl.sh"
    # 入参：1类型:maven/zip; 2打包根目录; 3打包子目录; 4包名 5备份目录
    package_cmd = "/usr/local/bin/package.sh"

    def __init__(self, app_config_do, service_config_do_list, deploy_git_branch, is_init_dir):
        self.app_config_do = app_config_do
        self.service_config_do_list = service_config_do_list
        self.deploy_git_branch = deploy_git_branch
        self.is_init_dir = is_init_dir

    def do_deploy(self):
        log.info("----------- 服务部署开始 -----------")
        log.info("1. git检出")
        git_url = self.app_config_do.git_url
        git_root_repo = ConfigHolder.get("work", "git_repo_root")
        temp_str = git_url.split("/")
        git_proj_dir = temp_str[len(temp_str) - 1].split(".")[0]
        os.system(
            "sh %s %s %s %s %s" % (self.gitctrl_cmd, git_root_repo, git_url, git_proj_dir, self.deploy_git_branch))
        log.info("2. 服务部署")
        for service_config_do in self.service_config_do_list:
            self.do_single_deploy(service_config_do)

        log.info("----------- 服务部署结束 -----------")
        return 1

    def do_single_deploy(self, service_config_do):
        log.info("========== 单个服务部署开始:%s ==========" % service_config_do.service_id)
        log.info("%s 1. 校验工作目录是否存在" % service_config_do.service_id)
        self.check_work_dir(service_config_do);
        log.info("%s 2. 打包" % service_config_do.service_id)
        self.pack_build(service_config_do)
        log.info("%s 3. 部署" % service_config_do.service_id)
        self.deploy_public(service_config_do);
        log.info("========== 单个服务部署结束:%s ==========" % service_config_do.service_id)
        return 1

    def pack_build(self, service_config_do):
        # 入参：1类型:maven/zip; 2打包根目录; 3打包子目录; 4包名 5备份目录
        pack_type = "zip"
        git_url = self.app_config_do.git_url
        git_root_repo = ConfigHolder.get("work", "git_repo_root")
        temp_str = git_url.split("/")
        git_proj_dir = temp_str[len(temp_str) - 1].split(".")[0]
        pack_root_path = os.path.join(git_root_repo, git_proj_dir)
        pack_child_path = service_config_do.build_child_dir
        pack_name = service_config_do.build_pack_name
        pack_backup_path = os.path.join(self.app_config_do.work_root_dir, service_config_do.work_relat_dir.replace("{PORT}", str(service_config_do.listen_port)), "backup")
        if 1 == service_config_do.build_type:
            pack_type="maven"
        os.system("sh %s %s %s %s %s %s" % (
            self.package_cmd, pack_type, pack_root_path, pack_child_path, pack_name, pack_backup_path
        ))
        pass

    def check_work_dir(self, service_config_do):
        fileUtil = FileUtil()

        log.info("%s 校验根目录是否存在" % service_config_do.service_id)
        app_root_path = self.app_config_do.work_root_dir
        if not os.path.exists(app_root_path):
            log.info("%s 根目录不存在，初始化: %s" % (service_config_do.service_id, app_root_path))
            os.makedirs(app_root_path)

        common_properties = os.path.join(app_root_path, "common.properties")
        if not os.path.exists(common_properties):
            log.info("%s common.properties初始化" % service_config_do.service_id)
            common_properties_template = os.path.join(EnvHolder.get("script.root.path"), ConfigHolder.get("work", "service_type_template_common_%s"%service_config_do.service_type))
            file_data = fileUtil.readFile(common_properties_template)
            fileUtil.writeFile(common_properties, file_data)

        service_root_path = os.path.join(self.app_config_do.work_root_dir, service_config_do.work_relat_dir.replace("{PORT}", str(service_config_do.listen_port)))
        if not os.path.exists(service_root_path):
            log.info("%s 服务运行目录不存在，初始化: %s" % (service_config_do.service_id, service_root_path))
            ZipUtils.unzip(
                os.path.join(EnvHolder.get("script.root.path"), ConfigHolder.get("work", "service_type_template_zip_%s"%service_config_do.service_type)),
                service_root_path,
                ""
            )
            log.info("%s 脚本文件初始化" % service_config_do.service_id)
            start_script_path = os.path.join(service_root_path, "start.sh")
            start_script_data = fileUtil.readFile(start_script_path)
            start_script_data = start_script_data.replace("{{APP_ROOT_PATH}}", app_root_path)
            start_script_data = start_script_data.replace("{{JAR}}", service_config_do.build_pack_name)
            start_script_data = start_script_data.replace("{{PARAMETER}}", service_config_do.start_script_template)
            fileUtil.writeFile(start_script_path, start_script_data)

            log.info("%s 配置文件初始化" % service_config_do.service_id)
            config_file_path = os.path.join(service_root_path, "config/config.properties")
            config_file_data = fileUtil.readFile(os.path.join(
                EnvHolder.get("script.root.path"),
                ConfigHolder.get("work", "service_type_template_config_%s" % service_config_do.service_type)
            ))
            config_file_data = config_file_data.replace("{service_id}", service_config_do.service_id)
            config_file_data = config_file_data.replace("{port}", str(service_config_do.listen_port))
            if config_file_data.find("{web_context_url}") != -1:
                config_file_data = config_file_data.replace("{web_context_url}", service_config_do.web_context_url)
            fileUtil.writeFile(config_file_path, config_file_data)
            log.info("%s 服务运行目录初始化完毕: %s" % (service_config_do.service_id, service_root_path))
        '''
        unzip_result = ZipUtils.unzip(
            os.path.join(EnvHolder.get("script.root.path"), ConfigHolder.get("work", "service_type_template_zip_2")),
            os.path.join(EnvHolder.get("script.root.path"), "temp/haha"),
            ""
        )
        '''
        pass

    def deploy_public(self, service_config_do):
        work_path = os.path.join(self.app_config_do.work_root_dir, service_config_do.work_relat_dir.replace("{PORT}", str(service_config_do.listen_port)))
        pack_backup_path = os.path.join(work_path, "backup")
        pack_jar_path = os.path.join(work_path, "jar")
        jar_name = service_config_do.build_pack_name
        if os.path.exists(os.path.join(pack_jar_path, jar_name)):
            dt = datetime.datetime.now()
            log.info("备份源文件: mv %s %s" % (
                os.path.join(pack_jar_path, jar_name),
                os.path.join(pack_backup_path, jar_name + dt.strftime("%Y%m%d%H%M%S"))
            ))
            os.system("mv %s %s" % (
                os.path.join(pack_jar_path, jar_name),
                os.path.join(pack_backup_path, jar_name + dt.strftime("%Y%m%d%H%M%S"))
            ))
        if not os.path.exists(os.path.join(pack_backup_path, jar_name)):
            raise RuntimeError('jar not exists!')
        log.info("发布:mv %s %s" % (
            os.path.join(pack_backup_path, jar_name),
            os.path.join(pack_jar_path, jar_name)
        ))
        os.system("mv %s %s" % (
            os.path.join(pack_backup_path, jar_name),
            os.path.join(pack_jar_path, jar_name)
        ))
        restart_file = os.path.join(work_path, "restart.sh")

        log.info("重启服务: sh %s" % restart_file)
        os.system("sh %s" % restart_file)
        pass
