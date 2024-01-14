"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys

from resource_management import *
from resource_management.core.logger import Logger

Logger.initialize_logger()
reload(sys)
sys.setdefaultencoding('utf-8')

# server configurations
config = Script.get_config()

# 生命一些常量
# conf_dir = "/etc/"
dinky_home = "/opt/soft/dinky" # dinky 安装目录
dinky_conf_dir = dinky_home + "/conf" # dinky 配置文件目录
dinky_log_dir = dinky_home + "/logs" # dinky 日志目录
dinky_bin_dir = dinky_home + "/" # dinky 启动脚本目录
dinky_lib_jars = dinky_home + "/lib/*" # dinky lib目录
dinky_extends_flink_jars = dinky_home + "/extends/*" # dinky extends目录
dinky_pidfile_dir = dinky_home + "/run/" # dinky pid目录
dinky_init_mysql_sqlfile_name = dinky_home + "/sql/dinky-mysql.sql" # dinky mysql 初始化脚本
dinky_init_pgsqll_sqlfile_name = dinky_home + "/sql/dinky-pg.sql" # dinky pgsql 初始化脚本
dinky_application_main_config_file = "application.yml" # dinky application.yml 配置文件
dinky_application_main_config_template_file = dinky_application_main_config_file + ".j2" # dinky application.yml 配置文件模板
dinky_application_mysql_config_file = "application-mysql.yml" # dinky application-mysql.yml 配置文件
dinky_application_mysql_config_template_file = dinky_application_mysql_config_file + ".j2" # dinky application-mysql.yml 配置文件模板
dinky_application_pgsql_config_file = "application-pgsql.yml" # dinky application-pgsql.yml 配置文件
dinky_application_pgsql_config_template_file = dinky_application_pgsql_config_file + ".j2" # dinky application-pgsql.yml 配置文件模板
dinky_pid_filename = "dinky.pid" # dinky pid文件名
start_script_name = "auto.sh" # dinky 启动脚本名
start_script_template_file = start_script_name + ".j2" # dinky 启动脚本模板

# 获取 dinky-application-server.xml 配置文件中的配置信息
# 1.创建一个空字典
dinky_env_map = {}
# 2.将 dinky-application-server.xml 配置文件中的配置信息添加到字典中
dinky_env_map.update(config['configurations']['dinky-application-server'])


# 获取 dinky 用户和用户组
dinky_user = dinky_env_map['dinky.user']
dinky_group = dinky_env_map['dinky.group']
# 获取 dinky 使用的 flink 版本号
dinky_flink_big_version = dinky_env_map['flink.big.version']

# 获取 dinky 服务使用的端口号
dinky_server_port = dinky_env_map['server.port']

# 声明数据库相关配置信息的字典 并将 dinky-application-server.xml 配置文件中的配置信息添加到字典中
dinky_database_config = {'dinky_database_type': dinky_env_map['spring.profiles.active'],
                         'dinky_database_username': dinky_env_map['spring.datasource.database.username'],
                         'dinky_database_password': dinky_env_map['spring.datasource.database.password']}


# 判断数据库类型 拼接数据库连接信息 的 url 并设置 class driver 信息
if 'mysql' == dinky_database_config['dinky_database_type']:
    # mysql 数据库连接信息
    dinky_database_config['dinky_database_driver'] = 'com.mysql.jdbc.Driver'
    dinky_database_config['dinky_database_url'] = 'jdbc:mysql://' + dinky_env_map['spring.datasource.database.host'] \
                                                  + ':' + dinky_env_map['spring.datasource.database.port'] \
                                                  + '/' + dinky_env_map['spring.datasource.database.name'] \
                                                  + '?useUnicode=true&characterEncoding=UTF-8'
else:
    # pgsql 数据库连接信息
    dinky_database_config['dinky_database_driver'] = 'org.postgresql.Driver'
    dinky_database_config['dinky_database_url'] = 'jdbc:postgresql://' + dinky_env_map[
        'spring.datasource.database.host'] \
                                                  + ':' + dinky_env_map['spring.datasource.database.port'] \
                                                  + '/' + dinky_env_map['spring.datasource.database.name'] \
                                                  + '?stringtype=unspecified'
