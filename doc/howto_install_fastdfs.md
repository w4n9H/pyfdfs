# 快速部署FastDFS

###　系统环境
``` bash
操作系统：CentOS 7
配置: ４核8G20G (基于openstack)
FastDFS 相关版本:fastdfs-5.05 fastdfs-nginx-module-v1.16 libfastcommon-v1.0.7
```

### 1.系统准备
+ 1.1.获取 pyfdfs

``` bash
git clone https://git.coding.net/Mango/pyfdfs.git
or
wget https://coding.net/u/Mango/p/pyfdfs/git/archive/master
```
+ 1.2.初始化系统

``` bash
yum update -y
sh pyfdfs/package/init_system.sh
# 初始化系统
```

### 2.安装FastDFS
+ 2.1.下载一键安装包(项目package目录中),unzip解压

``` bash
unzip -q package/fdfs0302_centos7.zip    # 解压基于centos6编译的fdfs安装包
cd package/fdfs0302_centos7
fdfs_install.sh    # 安装脚本
fdfs_uninstall.sh    # 卸载脚本
# 如果编译rpm包的教程在文档中会有的
```

+ 2.2.安装fdfs

``` bash
sh fdfs_install.sh    # 安装 fdfs
```

### 3.tracker配置启动
+ 3.1.tracker配置 (/etc/fdfs/tracker.conf)

``` bash
port=22122    # tracker 端口号
base_path=/opt/fastdfs/tracker    # 日志目录
reserved_storage_space = 10%    # storage 保留空间 10%
run_by_group=fdfs    # 运行group
run_by_user=fdfs    # 运行用户
use_storage_id = true    # 使用server ID作为storage server标识
storage_ids_filename = storage_ids.conf     # <id> <group_name> <ip_or_hostname>
id_type_in_filename = id    # 文件名反解析中包含server ID,以前是ip
```

+ 3.2.storage_ids.conf 配置 (/etc/fdfs/storage_ids.conf)
``` bash
# <id>  <group_name>  <ip_or_hostname>
 100001   group1  192.168.xx.xx
```

+ 3.3.client.conf 配置 (/etc/fdfs/client.conf)
``` bash
base_path=/opt/fastdfs/tracker
tracker_server=192.168.xxx.xxx:22122    # 客户端工具配置文件
```

+ 3.4.启动tracker
``` bash
service fdfs_trackerd start
```

### 4.storage配置启动
+ 4.1.storage.conf配置 (/etc/fdfs/storage.conf)
``` bash
group_name=group1    # 设置存储服务器group名称
port=23000    # 设置存储服务器端口号
base_path=/opt/fastdfs/storage    # 日志目录
store_path0=/opt/fastdfs/storage    # 设置存储服务器data数据存储目录
tracker_server=xxx.xxx.xxx.xxx:22122    # 指定tracker的ip及端口号
run_by_group= -> fdfs    # 运行group
run_by_user= -> fdfs    # 运行用户
```

+ 4.2.client.conf 配置 (/etc/fdfs/client.conf)
``` bash
base_path=/opt/fastdfs/storage
tracker_server=192.168.xxx.xxx:22122    # 客户端工具配置文件
```

+ 4.2.启动storage
``` bash
service fdfs_storaged start 
```

### 5.在storage启动nginx
+ 5.1.nginx配置 (/usr/local/nginx/conf/nginx.conf)
``` bash
location /group1/M00 {
          alias /opt/fastdfs/storage/data;
          ngx_fastdfs_module;
      }
# 如果在 storage 目录下挂载了硬盘目录　data1,配置应该为 alias /opt/fastdfs/storage/data1/data
```

+ 5.2.配置mod_fastdfs.conf,nginx的fdfs模块配置文件
``` bash
base_path=/tmp
load_fdfs_parameters_from_tracker=true
tracker_server=xxx.xxx.xxx.xx:22122    # 设置tracker的地址及端口
storage_server_port=23000    # 存储服务器端口
group_name=group1    # 这台存储服务器所属group
url_have_group_name = true    # 通过url下载文件是是否需要带上group名
store_path_count=1    # 存储路径数量
store_path0=/opt/fastdfs/storage    # 存储路径
log_filename=/opt/www/logs/mod_fastdfs.log    # 日志路径,要放在一个nginx有权限的目录
# 下面两条是需要添加的
http.mime_types_filename=mime.types
http.default_content_type = application/octet-stream
```

+ 5.3.启动nginx
``` bash
service nginx start
```

### 6.简单测试
``` bash
fdfs_monitor /etc/fdfs/client.conf    # 查看存储服务器状态
fdfs_upload_file /etc/fdfs/client.conf xxxx.txt    # 上传文件
group1/M00/00/00/oYYBAFagj52AeJ4-AAAAgOp8ixk565.txt    # 上传文件的返回信息
http://xxx.xxx.xxx.xxx/group1/M00/00/00/oYYBAFagj52AeJ4-AAAAgOp8ixk565.txt    # 在存储服务器访问文件
```
