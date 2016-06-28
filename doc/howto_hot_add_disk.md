# 1.如何热添加磁盘

### 1.1.挂载磁盘

``` bash
mkfs.xfs /dev/vdc    # 格式化磁盘
mkdir /opt/fastdfs/storage/data2    # 数据存储位置
vim /etc/fdtab
/dev/vdc   /opt/fastdfs/storage/data2 xfs  defaults        0 0
# 配置完成后，执行
mount -a    # 挂载
df -h    # 查看是否挂载成功
```

### 1.3.配置storage

``` bash
vim /etc/fdfs/storage.conf    # 修改配置文件
store_path0=/opt/fastdfs/storage/data1
store_path1=/opt/fastdfs/storage/data2
# path(disk or mount point) count, default value is 1
store_path_count=2
# 重启 storage
service fdfs_storaged stop     
service fdfs_storaged start    # 即可完成 节点热添加, 我使用 restart 似乎不行,好像要先关掉storage服务
```

### 1.3.配置mod_fastdfs.conf

``` bash
vim /etc/fdfs/mod_fastdfs.conf
store_path_count=2
store_path0=/opt/fastdfs/storage/data1
store_path1=/opt/fastdfs/storage/data2
```

### 1.4.配置nginx

``` bash
location /group1/M01 {
          alias /opt/fastdfs/storage/data2/data;
          ngx_fastdfs_module;
      }
```

### 1.5.重启nginx

``` bash
sh /opt/nginx restart
```