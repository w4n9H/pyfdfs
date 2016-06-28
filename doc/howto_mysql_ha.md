# Mysql 双机热备 实施方案

``` bash
1.MySQL数据库没有增量备份的机制，当数据量太大的时候备份是一个很大的问题。还好MySQL数据库提供了一种主从备份的机制，其实就是把主数据库的所有的数据同时写到备份数据库中。实现MySQL数据库的热备份。
2.要想实现双机的热备首先要了解主从数据库服务器的版本的需求。要实现热备MySQL的版本都要高于3.2，还有一个基本的原则就是作为从数据库的数据库版本可以高于主服务器数据库的版本，但是不可以低于主服务器的数据库版本。
3.MySQL的双机热备份是基于MySQL内部复制功能，建立在两台或者多台以上的服务器之间，通过它们之间的主从关系，是插入主数据库的数据同时也插入到从数据库上，这实现了动态备份当前数据库的功能。
```

### 1.Mysql 环境

``` bash
主服务器A(master)、从服务器为B(slave)
A：192.168.11.129
B：192.168.11.152
```

### 2.创建同步用户

+ 授权副服务器可以连接主服务器并可以进行更新。这是在主服务器上进行的，创建一个username和password供副服务器访问时使用。在MySQL命令行下输入

``` bash
mysql> GRANT REPLICATION SLAVE ON *.* TO backup@'192.168.11.152' IDENTIFIED BY '123456'; 
mysql> flush privileges;
```

+ 这里创建了一个帐号backup用于slave访问master来更新slave数据库。
+ 当然也可以跳过这步直接使用网站本身的root用户和密码来访问master，在这里以root用户作为例子来介绍


### 3.配置主服务器
+ 修改master上mysql的根目录下的my.ini配置文件
+ 在选项配置文件中赋予主服务器一个server-id，该id必须是1到2^23-1范围
+ 内的唯一值。主服务器和副服务器的server-id不能相同。另外，还需要配置主服务器，使之启用二进制日志，即在选项配置文件中添加log-bin启动选项。
 
``` bash
[mysqld]
# 唯一值，并不能与副服务器相同
server-id=1
# 日志文件以binary_log为前缀，如果不给log-bin赋值，日志文件将以#master-server-hostname为前缀
log-bin = mysql-fdfs
# 日志文件跳过的数据库(可选属性)
binlog-ignore-db= mysql,test,information_schema,performance_schema
# 日志文件操作的数据库(可选属性)
binlog-do-db= fdfs
```
 
+ 注意：如果主服务器的二进制日志已经启用，关闭并重新启动之前应该对以前的二进制日志进行备份。重新启动后，应使用RESET MASTER语句清空以前的日志。
+ 原因：master上对数据库cartrader的一切操作都记录在日志文件中，然后会把日志发给slave，slave接收到master传来的日志文件之后就会执行相应的操作，使slave中的数据库做和master数据库相同的操作。所以为了保持数据的一致性，必须保证日志文件没有脏数据

### 4.重启master
+ 配置好以上选项后，重启MySQL服务，新选项将生效。现在，所有对数据库中信息的更新操作将被写进日志中。

### 5. 查看master状态

``` bash
mysql> FLUSH TABLES WITH READ LOCK;    # 所有库所有表锁定只读
mysql>show master status
# 注：这里使用了锁表，目的是为了产生环境中不让进新的数据，好让从服务器定位同步位置，初次同步完成后，记得解锁。
mysql> UNLOCK TABLES;    # 解锁
```

### 6.配置slave
+ 在副服务器上的MySQL选项配置文件中添加以下参数。

``` bash
[mysqld]
server-id=2
log-bin=mysql-fdfs
replicate-do-db = fdfs
replicate-ignore-db =mysql,information_schema,performance_schema,test
```

### 7.重启slave,指定同步位置

``` bash
mysql>stop slave;          #先停步slave服务线程，这个是很重要的，如果不这样做会造成以下操作不成功。
mysql>change master to
>master_host='主机ip',master_user='replicate',master_password='123456',
>master_log_file='mysql-bin.000016',master_log_pos=490;
# 注：master_log_file,master_log_pos由主服务器（Master）查出的状态值中确定
# Mysql 5.x以上版本已经不支持在配置文件中指定主服务器相关选项
mysql>start slave;    # 开启
mysql>show slave status\G    # 以下两个值为yes成功
# Slave_IO_Running: Yes
# Slave_SQL_Running: Yes
```

### 9.注意

+ 千万记得把主库锁表操作恢复过来
+ 以上的配置方式只能实现A->B，即数据由A(master)转移到B(slave)，不能由B转移到A，这样的话对B做的任何操作就不会被同步到数据库A中。
+ 当然也可以通过把A设置成slave和master，把B设置成slave和master从而实现对A或者B的任何改动都会影响到另外一方。配置同上，在此不在论述。
