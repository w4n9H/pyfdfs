# MariaDB 调优

### 1.配置 MariaDB 最大连接数

``` bash
大概意思是 MySQL 能够支持的最大连接数量受限于操作系统,如果超过限制会被重置到 214
修改 /etc/my.cnf.d/server.cnf
[mysqld]
open_files_limit = 65535
max_connections = 2000
max_connect_errors = 100000
max_user_connections = 2000
修改 /usr/lib/systemd/system/mariadb.service 在最下面添加
LimitNOFILE=65535
LimitNPROC=65535
$ systemctl daemon-reload    # 重新载入
$ systemctl restart  mysqld.service  # 重启mariadb
```

### 2.配置 MariaDB Time_out

``` bash
指定一个请求的最大连接时间，如果对于mariadb是大量短连接的话可以设置为5-10s
[mysqld]
wait_timeout = 10            # 连接超时时间
interactive_timeout = 120    # 交互超时时间
```

### 3.配置 MariaDB Thread 设置

``` bash
mariadb 的线程相关配置
[mysqld]
thread_cache_size = 1000          # 设置服务器缓存的线程数量
thread_pool_max_threads = 2000    # 设置线程池的最大线程数量
thread_pool_size = 2000           # 设置线程池的大小
thread_concurrency = 128          # 线程的并发数,可以设置为服务器逻辑cpu数量 * 2
```

### 4.配置 MariaDB 的查询缓存容量

``` bash
使用查询缓存需要容忍可能发生的数据不一致的问题,对数据准确性要求较高的系统不建议开启
或者数据库内容变动比较频繁的系统也不建议开启
```

### 5.禁用 MariaDB 的 DNS 反向查询

``` bash
[mysqld]
skip-name-resolve
```

### 6.Mariadb 的 buff size 设置

``` bash
[mysqld]
key_buffer_size = 384M
sort_buffer_size = 16M
read_buffer_size = 16M
read_rnd_buffer_size = 32M
join_buffer_size = 16M
```

### 7.配置临时表容量

``` bash 
[mysqld]
tmp_table_size= 128M
```

### 8.Back log 配置

``` bash
[mysqld]
back_log = 512
在MySQL暂时停止响应新请求之前的短时间内多少个请求可以被存在堆栈中。  
如果系统在一个短时间内有很多连接，则需要增大该参数的值，该参数值指定到来的TCP/IP连接的侦听队列的大小。
不同的操作系统在这个队列大小上有它自己的限制。 
试图设定back_log高于你的操作系统的限制将是无效的
```

### 9.Mariadb innodb 配置

``` bash
[mysqld]
innodb_buffer_pool_size = 8G
```

### 6.Mariadb 状态监控

``` bash
$ yum install mysqlreport
mysqlreport --socket /data/disk01/mysql/mysql.sock --user xxxxx -password xxxxx --outfile mysql.txt
```