# 安装Mysql

### 1.系统环境

``` bash
操作系统: CentOS 7
系统配置: 4核16G20G
```

### 2.卸载原有Mysql

``` bash
rpm -qa | grep mysql    # 查看已经安装的mysql版本
rpm -e mysql-xx.xx.xx.xx    # 卸载已经安装的mysql --nodeps 强力删除模式
```

### 3.安装mysql

``` bash
# 系统初始化时已经安装
# yum install mysql-server mysql mysql-devel -y
# 截止 2016-01-25  YUM 默认的 Mysql 版本为 5.1.73 (确实老了点,也可以尝试自行编译)
# centos 7
yum install mariadb mariadb-server -y
```

### 4.启动Mysql

``` bash
# 安装成功后会多一个mysqld的服务
service mysqld start    # 启动mysql
service mysqld stop    # 关闭mysql
service mysqld restart    # 重启mysql
chkconfig mysqld on    # 开机启动
# centos 7
systemctl start mariadb ==> 启动mariadb
systemctl enable mariadb ==> 开机自启动
```

### 5.基本配置

``` bash
mysqladmin -u root password 'test'    # 为root账户设置密码
/etc/my.cnf    # mysql 配置文件
/var/lib/mysql    # mysql数据库的数据库文件存放位置
```


### 6.基本使用

``` bash
mysql -u root -ptest    # 登录
show databases;
create database fdfs;
```

### 7.设置外网访问

```bash
mysql -u root -ptest>use mysql;
#mysql>update user set host='%' where user='root';
mysql>GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'IDENTIFIED BY '123456' WITH GRANT OPTION;
#mysql>select host, user from user;
mysql>flush privileges;
```

### 8.Python安装Mysql库

```bash
# 初始化中已经安装
pip install peewee pymysql
```

# 9.创建数据表

``` bash
mysql -h ip -u root -ptest
create database fdfs;    # 创建数据库
python afdfs/src/server/handler/mysql_create.py    # 完成建表
# 优化
# 1.建立 file_name 索引
# 2.file_name 和 domain_name 做了复合主键,防止出现相同名称和域的数据,去除了 id 这个主键
# 3.对字段均做了max长度处理
```

# 10.中文存储配置

``` bash
# 可插入中文
vim /etc/my.cnf.d/server.cnf
[mysqld]
character-set-server=utf8
# 查询中文,以及显示中文
```