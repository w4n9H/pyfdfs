#!/usr/bin/env bash
# init sysytems
yum install rpm-build vim wget git screen zip unzip gcc glibc-devel libtool openssl openssl-devel pcre-devel pcre ntp gcc gcc-c++ -y
# yum install mysql-server mysql mysql-devel -y
yum install mariadb mariadb-server mariadb-devel -y
yum install python-devel python-setuptools -y

# start ntpds
chkconfig ntpd on
service ntpd start
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# set selinux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

# close iptabless
service iptables stop
chkconfig iptables off

# install fdfs so
cp /opt/afdfs/src/server/handlers/jsonlib/* /usr/local/lib/
cp /opt/afdfs/src/server/handlers/jsonlib/* /usr/local/lib64/
touch /etc/ld.so.conf.d/local.conf
echo '/usr/local/lib' >> /etc/ld.so.conf.d/local.conf
echo '/usr/local/lib64' >> /etc/ld.so.conf.d/local.conf
ldconfig

# install python libs
easy_install pip
pip install tornado==4.3 peewee==2.8.0 supervisor pymysql
# tornado == 4.3
# peewee == 2.8.0


