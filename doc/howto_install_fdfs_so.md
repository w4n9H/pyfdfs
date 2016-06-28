# 编译安装 fdfs 第三方 c 库

### 1.系统环境

``` bash
系统环境：CentOS 7 ， 64位，JSON库是在64位 CentOS6.4 上编译的，在 6.5 上测试通过，其他环境未测试 (CentOS 6, 7 应无问题)
Fastdfs版本： 5.05  ，测试已通过，其他版本暂未测试
```

### 2.编译说明

+ 2.1.解压 fastdfs5.05 源码包, 复制 FastDFSClient_Python/ClientForPython 目录到 fastdfs-5.0.5/client/ 目录下

``` bash
git clone https://github.com/cosysun/FastDFSClient_Python.git
tar -zxf fastdfs-5.0.5.tar.gz
cp -r FastDFSClient_Python/ClientForPython fastdfs-5.0.5/client/
```

+ 2.2.复制json文件夹到 /usr/include/ 下

``` bash
cp -r FastDFSClient_Python/ClientForPython/json /usr/include/
```

+ 2.3.复制json文件夹得文件到 /usr/local/lib 和 /usr/local/lib64

``` bash
cp FastDFSClient_Python/ClientForPython/json/lib/* /usr/local/lib/
cp FastDFSClient_Python/ClientForPython/json/lib/* /usr/local/lib64/
# 新建文件
vim /etc/ld.so.conf.d/local.conf  
# 加入下面两句后保存
/usr/local/lib
/usr/local/lib64
# 最后执行 ldconfig 命令
ldconfig
```

+ 2.4.安装 python-decel
 
``` bash
# 系统初始化时已安装
yum install python-devel    # 否则会找不到python.h
```

+ 2.5.修改ClientForPython目录下Makefile文件

``` bash
vim FastDFSClient_Python/ClientForPython/Makefile
INC_PATH = -I. -I../../tracker -I../../storage -I../ -I ../../common -I/usr/local/include -I/usr/local/include/python2.7 -I/usr/include/fastcommon -I/usr/include/fdfsdfst
# /usr/local/include  修改为 /use/include
# /usr/local/include/python2.7  修改为 /usr/include/python2.7
# /usr/include/fastcommon 不变
# /usr/include/fdfsdfst 修改为 /usr/include/fastdfs
```

+ 2.6.编译并检查

``` bash
执行 make 编译，
然后通过 ldd 命令查看 so 库
ldd FDFSPythonClient.so 
    linux-vdso.so.1 =>  (0x00007fff0ff9f000)
    libfastcommon.so => /usr/lib64/libfastcommon.so (0x00007fc4dd291000)
    libfdfsclient.so => /usr/lib64/libfdfsclient.so (0x00007fc4dd07a000)
    libpthread.so.0 => /lib64/libpthread.so.0 (0x00007fc4dce5c000)
    libdl.so.2 => /lib64/libdl.so.2 (0x00007fc4dcc58000)
    libjsonlib.so => /usr/lib/libjsonlib.so (0x00007fc4dca15000)
    libstdc++.so.6 => /usr/lib64/libstdc++.so.6 (0x00007fc4dc70e000)
    libm.so.6 => /lib64/libm.so.6 (0x00007fc4dc48a000)
    libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00007fc4dc274000)
    libc.so.6 => /lib64/libc.so.6 (0x00007fc4dbedf000)
    /lib64/ld-linux-x86-64.so.2 (0x00007fc4dd6cc000)
# 没有出现 not found 就是编译成功了
```


### 3.安装说明

+ 3.1.安装说明

``` bash
执行上面的  2.3 步骤,然后执行 ldd 检查即可
代码 src/server/handers/jsonlib/ 目录下也有相同的 so 文件
```

### 4.在 python 中使用

``` bash
import FDFSPythonClient
o = FDFSPythonClient.fdfs_init("/etc/fdfs/client.conf", 7)
r = FDFSPythonClient.list_all_groups()
# 返回的对象为json.dumps后的数据
# list_all_groups()  监控所有group信息
# list_one_group("IP地址") 监控指定ip信息
# list_storages("组名", "IP地址")  监控某组下storages的信息，如果ip不为空则监控全部， 
```

### 5.相关资料

``` bash
github项目页面
https://github.com/cosysun/FastDFSClient_Python
说明文档
http://blog.csdn.net/lenyusun/article/details/44057139
这里的JSON库是我在CentOS下编译的，有可能在其他系统上有冲突，请下载源码重新编译，地址：
https://github.com/open-source-parsers/jsoncpp.git
```