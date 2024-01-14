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

from resource_management import *


def dinky_env():
    import params  # import 导入params.py文件

    User(params.dinky_user, action="create", groups=params.dinky_group
         , ignore_already_exists=True  # 忽略已经存在
         )  # 创建用户

    Directory(params.dinky_pidfile_dir,  # Directory执行文件夹操作
              mode=0777,
              owner=params.dinky_user,
              group=params.dinky_group,
              create_parents=True  # 父目录不存在时一起创建
              )
    Directory(params.dinky_log_dir,
              mode=0777,
              owner=params.dinky_user,
              group=params.dinky_group,
              create_parents=True
              )
    Directory(params.dinky_conf_dir,
              mode=0777,
              owner=params.dinky_user,
              group=params.dinky_group,
              create_parents=True
              )

    ## 重写 启动脚本 auto.sh 文件
    File(format(params.dinky_bin_dir + params.start_script_name),
         mode=0755,
         content=Template(params.start_script_template_file),
         owner=params.dinky_user,
         group=params.dinky_group
         )

    # 重写 application.yml 文件
    File(format(params.dinky_conf_dir + "/" + params.dinky_application_main_config_file),
         mode=0755,
         content=Template(params.dinky_application_main_config_template_file),
         owner=params.dinky_user,
         group=params.dinky_group
         )

    ## 根据 mysql 还是 pgsql 重写 application-xxx.yml 文件
    if params.dinky_database_config['dinky_database_type'] == "mysql":
        ## 重写 application-mysql.yml 文件
        File(format(params.dinky_conf_dir + "/" + params.dinky_application_mysql_config_file),
             mode=0755,
             content=Template(params.dinky_application_mysql_config_template_file),
             owner=params.dinky_user,
             group=params.dinky_group
             )
    else:
        ## 重写 application-pgsql.yml 文件
        File(format(params.dinky_conf_dir + "/" + params.dinky_application_pgsql_config_file),
             mode=755,
             content=Template(params.dinky_application_pgsql_config_template_file),
             owner=params.dinky_user,
             group=params.dinky_group
             )
