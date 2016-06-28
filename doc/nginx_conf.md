### Nginx 配置文件
+ tracker nginx 配置文件

``` bash
user  www www;
worker_processes  16;
error_log  /opt/www/logs/error.log  error;
pid        /opt/www/logs/nginx.pid;
worker_rlimit_nofile 5120;
events {
  use epoll;
  worker_connections  5120;
}
http {
  include       mime.types;
  default_type  application/octet-stream;
  sendfile        on;
  tcp_nopush     on;
  keepalive_timeout  20;
  tcp_nodelay on;
  proxy_next_upstream error;
  upstream pyfdfs {
    server 192.168.13.192:8000 max_fails=1 fail_timeout=600s;
    server 192.168.13.192:8001 max_fails=1 fail_timeout=600s;
    server 192.168.13.192:8002 max_fails=1 fail_timeout=600s;
    server 192.168.13.192:8003 max_fails=1 fail_timeout=600s;
    server 192.168.13.192:8004 max_fails=1 fail_timeout=600s;
    server 192.168.13.193:8000 max_fails=1 fail_timeout=600s;
    server 192.168.13.193:8001 max_fails=1 fail_timeout=600s;
    server 192.168.13.193:8002 max_fails=1 fail_timeout=600s;
    server 192.168.13.193:8003 max_fails=1 fail_timeout=600s;
    server 192.168.13.193:8004 max_fails=1 fail_timeout=600s;
    keepalive 16;
  }
  server {
      listen       80;
      server_name  tracker01.afdfs.antiy;
      location / {
          proxy_pass_header Server;
          proxy_set_header Host $http_host;
          proxy_redirect off;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Scheme $scheme;
          proxy_pass http://pyfdfs;
          client_max_body_size 1000m;
      }
  }
}
```