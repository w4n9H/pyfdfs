# 1.如何热添加服务器

### 1.1.系统初始化及安装 fastdfs

``` basn
# 参照 fastdfs 安装教程, 第一步, 第二步
```

### 1.2.挂载磁盘

``` bash
mkfs.xfs /dev/vdb    # 格式化磁盘
mkdir /opt/fastdfs/storage/data1    # 数据存储位置
vim /etc/fdtab
/dev/vdb   /opt/fastdfs/storage/data1 xfs  defaults        0 0
# 配置完成后，执行
mount -a    # 挂载
df -h    # 查看是否挂载成功
```


### 1.3.配置storage

``` bash
# 参照 fastdfs 安装教程, 第四步 storage配置 , 但是暂时不启动
```

### 1.4.配置tracker

``` bash
# 参照 fastdfs 安装教程, 第三步 3.2.storage_ids.conf配置 , 增加新的节点信息
service fdfs_trackerd restart    # 重启 tracker
```

### 1.5.启动storage

``` bash
service fdfs_storaged start    # 即可完成 节点热添加
```

### 1.6.修改 pyfdfs app 配置文件

``` bash
vim /opt/afdfs/src/server/handlers/settings.py
# 修改 FDFS_DOMAIN 中的 group 信息
supervisorctl restart pyfdfs-app:*    # 重启服务
```

### 1.7.注意事项

``` bash
1. storage 是不需要 mysql配置那一步的
2. fastdfs 第三方 so 库在系统初始化时已经安装好了, 也不需要安装
3. pyfdfs app 配置那一步 确实很坑
```