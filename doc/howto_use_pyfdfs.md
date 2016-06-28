# PyFDFS 使用教程

### 1.安装 Python 库

``` bash
# 系统初始化时已安装
pip install tornado peewee supervisor pymysql
tornado == 4.3
peewee == 2.8.0
```

### 2.运行代码

``` bash
python pyfdfs/src/server/app.py
```


### 3.使用 supervisor 管理 pyfdfs

``` bash
# 安装 supervisor
pip install supervisor    # 安装
echo_supervisord_conf     # 测试安装是否成功
echo_supervisord_conf > /etc/supervisord.conf    # 配置文件
supervisord    # 启动
# supervisor 配置文件  vim /etc/supervisord.conf
[program:pyfdfs-app]
user=root                                                                   # 启动user
directory=/opt/pyfdfs/src/server/                                           # 启动目录
command=/usr/bin/python app.py --port=900%(process_num)s --logging=error    # 启动命令
redirect_stderr=true                                                        # 重定向stderr到stdout
startretries=10                                                             # 启动失败时最大重试次数
numprocs=1                                                                  # 启动进程数量
process_name=%(program_name)s_%(process_num)s                               # 进程名
stderr_logfile=/var/log/supervisor/cloud_speedup.log                        # 日志
stdout_logfile=/var/log/supervisor/cloud_speedup.log
autostart=true                                                              # supervisor启动的时候是否随着同时启动
autorestart=true                                                            # 当程序跑出exit的时候，这个program会自动重启
```
