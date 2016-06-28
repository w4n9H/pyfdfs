# Fastdfs 配置文件文档

### 1.Tracker 配置文件文档
 
``` python
disabled=false                             # 配置tracker.conf这个配置文件是否生效，因为在启动fastdfs服务端进程时需要指定配置文件，所以需要使次配置文件生效。false是生效，true是屏蔽。
run_by_group=fdfs                          # 进程以那个用户/用户组运行，不指定默认是当前用户
run_by_user=fdfs
bind_addr=                                 # 程序的监听地址，如果不设定则监听所有地址
port=22122                                 # tracker监听的端口
base_path=/opt/fastdfs/tracker             # 数据和日志的存放地点
connect_timeout=30                         # 链接超时设定
network_timeout=60                         # tracker在通过网络发送接收数据的超时时间
max_connections=256                        # 服务所支持的最大链接数
accept_threads=1
work_threads=4                             # 工作线程数
store_lookup=2                             # 在存储文件时选择group的策略，0:轮训策略 1:指定某一个组 2:负载均衡，选择空闲空间最大的group
store_group=group2                         # 如果上面的store_lookup选择了1，则这里需要指定一个group
store_server=0                             # 在group中的哪台storage做主storage，当一个文件上传到主storage后，就由这台机器同步文件到group内的其他storage上，0：轮训策略 1：根据ip地址排序，第一个 2:根据优先级排序，第一个
store_path=0                               # 选择文件上传到storage中的哪个(目录/挂载点),storage可以有多个存放文件的base path 0:轮训策略 2:负载均衡，选择空闲空间最大的
download_server=0                          # 选择那个storage作为主下载服务器，0:轮训策略 1:主上传storage作为主下载服务器
reserved_storage_space = 10%               # 系统预留空间, xx.xx%, 4GB, 400MB.....
log_level=info                             # 日志信息级别
allow_hosts=*                              # 允许那些机器连接tracker默认是所有机器, 10.0.1.[1-15,20], host[01-08,20-25].domain.com
sync_log_buff_interval = 10                # 设置日志信息刷新到disk的频率，默认10s
check_active_interval = 120                # 检测storage服务器的间隔时间，storage定期主动向tracker发送心跳，如果在指定的时间没收到信号，tracker认为storage故障，默认120s
thread_stack_size = 64KB                   # 线程栈的大小，最小64K
storage_ip_changed_auto_adjust = true      # storage的ip改变后服务端是否自动调整，storage进程重启时才自动调整
storage_sync_file_max_delay = 86400        # storage之间同步文件的最大延迟，默认1天
storage_sync_file_max_time = 300           # 同步一个文件所花费的最大时间
# 块存储相关设置
use_trunk_file = false                     # 是否用一个trunk文件存储多个小文件
slot_min_size = 256                        # 最小的solt大小，应该小于4KB，默认256bytes
slot_max_size = 16MB                       # 最大的solt大小，如果上传的文件小于默认值，则上传文件被放入trunk文件中
trunk_file_size = 64MB                     # trunk文件的默认大小，应该大于4M
trunk_create_file_advance = false
trunk_create_file_time_base = 02:00
trunk_create_file_interval = 86400
trunk_create_file_space_threshold = 20G
trunk_init_check_occupying = false
trunk_init_reload_from_binlog = false
trunk_compress_binlog_min_interval = 0
# 
use_storage_id = true
storage_ids_filename = storage_ids.conf
id_type_in_filename = ip
store_slave_file_use_link = false
rotate_error_log = false
error_log_rotate_time=00:00
rotate_error_log_size = 0
log_file_keep_days = 365
use_connection_pool = false    # 使用连接池
connection_pool_max_idle_time = 3600
# http 服务 , 暂不使用
http.server_port=8080
http.check_alive_interval=30
http.check_alive_type=tcp
http.check_alive_uri=/status.html
```


### 2.Storage 配置文件文档

``` python
disabled=false                            # 同tracker
run_by_group=fdfs                         # 同tracker
run_by_user=fdfs                          # 同tracker
bind_addr=                                # 同tracker
port=23000                                # 同tracker
base_path=/opt/fastdfs/storage            # 数据和日志的存放地点
store_path0=/opt/fastdfs/storage/data1    # 配置多个store_path路径，从0开始，如果store_path0不存在，则base_path必须存在
store_path1=/opt/fastdfs/storage/data2
store_path_count=1                        # store_path 数量,要和设置匹配
tracker_server=192.168.11.129:22122       # 设置tracker_server
group_name=group2                         # 这个storage服务器属于那个group
client_bind=true                          # 连接其他服务器时是否绑定地址，bind_addr配置时本参数才有效
connect_timeout=30                        # 同tracker
network_timeout=60                        # 同tracker
heart_beat_interval=30                    # 主动向tracker发送心跳检测的时间间隔
stat_report_interval=60                   # 主动向tracker发送磁盘使用率的时间间隔
max_connections=256                       # 服务所支持的最大链接数
buff_size = 256KB                         # 接收/发送数据的buff大小，必须大于8KB
accept_threads=1
work_threads=4                            # 工作线程数
disk_rw_separated = true                  # 磁盘IO是否读写分离
disk_reader_threads = 1                   # 混合读写时的读写线程数
disk_writer_threads = 1                   # 混合读写时的读写线程数
sync_wait_msec=50                         # 同步文件时如果binlog没有要同步的文件，则延迟多少毫秒后重新读取，0表示不延迟
sync_interval=0                           # 同步完一个文件后间隔多少毫秒同步下一个文件，0表示不休息直接同步
sync_start_time=00:00                     # 同步开始时间
sync_end_time=23:59                       # 同步结束时间
write_mark_file_freq=500                  # 同步完多少文件后写mark标记
subdir_count_per_path=256                 # subdir_count  * subdir_count个目录会在store_path下创建，采用两级存储
log_level=info                            # 日志信息级别
allow_hosts=*                             # 允许哪些机器连接tracker默认是所有机器
file_distribute_path_mode=0               # 文件在数据目录下的存放策略，0:轮训 1:随机
file_distribute_rotate_count=100          # 当问及是轮训存放时，一个目录下可存放的文件数目
fsync_after_written_bytes=0               # 写入多少字节后就开始同步，0表示不同步
sync_log_buff_interval=10                 # 刷新日志信息到disk的间隔
sync_binlog_buff_interval=10
sync_stat_file_interval=300               # 同步storage的状态信息到disk的间隔
thread_stack_size=512KB                   # 线程栈大小
upload_priority=10                        # 设置文件上传服务器的优先级，值越小越高
if_alias_prefix=
check_file_duplicate=0                    # 是否检测文件重复存在，1:检测 0:不检测
file_signature_method=hash
key_namespace=FastDFS
keep_alive=0                              # 与FastDHT建立连接的方式 0:短连接 1:长连接
use_access_log = false
rotate_access_log = false
access_log_rotate_time=00:00
rotate_error_log = false
error_log_rotate_time=00:00
rotate_access_log_size = 0
rotate_error_log_size = 0
log_file_keep_days = 365
file_sync_skip_invalid_record=false
use_connection_pool = false
connection_pool_max_idle_time = 3600
http.domain_name=
http.server_port=8888
```

### 3.mod_fastdfs.conf 配置文件文档

``` python
connect_timeout=2                          # 连接超时时间，默认值是30秒
network_timeout=30                         # 网络超时时间，默认值是30秒
base_path=/tmp
load_fdfs_parameters_from_tracker=true
storage_sync_file_max_delay = 86400
use_storage_id = true
storage_ids_filename = storage_ids.conf
tracker_server=192.168.11.129:22122        # Tracker服务器
storage_server_port=23000                  # 本机的Storage端口号，默认值为23000
group_name=group2                          # 本机Storage的组名
url_have_group_name = true                 # 访问文件的URI是否含有group名称
store_path_count=1                         # 存储路径个数
store_path0=/opt/fastdfs/storage/data1     # 存储路径
log_level=info                             # 日志级别
log_filename=/opt/www/logs/mod_fastdfs.log # 日志路径,注意权限问题
response_mode=proxy                        # 当本地不存在该文件时的响应策略，proxy则从其他Storage获取然后响应给client，redirect则将请求转移给其他storage
if_alias_prefix=
http.mime_types_filename=mime.types
http.default_content_type = application/octet-stream
flv_support = true
flv_extension = flv
group_count = 0
```