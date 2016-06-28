# PyFDFS
### 基于Python + Fastdfs + Nginx + Mysql 的分布式文件存储平台

### 需求：
```
+ 1.文件原样存储，非块存储
+ 2.环境快速搭建,存储集群快速扩容
+ 3.配套工具齐全
```

``` python
API接口: Python
# 快速开发，便于维护，第三方库丰富
底层存储: FastDFS
# 速度优势，文件原样存储
# 搭建难度较大，配套工具不全，没有索引存储，
下载提供: Nginx
# 负载均衡
# 提供下载文件功能
索引存储: Mysql
# 存储索引以及相关信息
# 轻量级,搭建方便
```

### 如何使用

+ 1. 安装配置 fdfs  [详情](https://coding.net/u/Mango/p/pyfdfs/git/blob/master/doc/howto_install_fastdfs.md)
+ 2. 安装 MySQL (优化教程尚缺) [详情](https://coding.net/u/Mango/p/pyfdfs/git/blob/master/doc/howto_install_mysql.md)
+ 3. 安装 fdfs 第三方 c库 [参考第三步安装即可](https://coding.net/u/Mango/p/pyfdfs/git/blob/master/doc/howto_install_fdfs_so.md)
+ 4. 安装 pyfdfs [详情](https://coding.net/u/Mango/p/pyfdfs/git/blob/master/doc/howto_use_pyfdfs.md)


### 版本更新:

+ 1.0 稳定版

``` bash
1.接口趋于稳定(暂时不会有大的调整)
2.进行性能测试以及压力测试
```

+ 0.5 测试版

``` bash
1. 首页展示使用了tornado模板,废弃了使用纯html
2. 文档更新,热添加节点和磁盘
```

+ 0.4 测试版

``` bash
1. 系统环境变更为 CentOS 7
```

+ 0.3 测试版

``` bash
1. 数据库结构调整
2. 增加系统初始化脚本,shell
3. 上传接口分为 upload(不计算hash) , upload_test(计算hash)
4. 文件上传临时存储目录可定制
```

+ 0.2 测试版

``` bash
1. 增加了删除接口
2. 增加了上传测试工具以及域空间删除工具
```

+ 0.1 测试版

``` bash
1. 基本功能,上传, 下载, 查询, 集群状态展示接口
2. 集群状态展示页面
```