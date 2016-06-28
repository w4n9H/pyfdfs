# 如何编译 fdfs rpm 安装包

### 1.系统环境

``` bash
系统环境：CentOS 7 ， 64位，JSON库是在64位 CentOS6.4 上编译的，在 6.5 上测试通过，其他环境未测试 (CentOS 6 应无问题)
Fastdfs版本： 5.05  ，测试已通过，其他版本暂未测试
```

### 2. libfastcommon-1.0.7-1.el7.centos.src.rpm

``` bash
rpm2cpio libfastcommon-1.0.7-1.el7.centos.src.rpm | cpio -div    # 如何解压 rpm 包
libfastcommon-1.0.7.tar.gz  libfastcommon.spec    #解压出的文件
rpmbuild -bb libfastcommon.spec    # 这样不会成功,但是会在home目录下生产 rpmbuild 的目录  
cp fdfs0302_centos7/source/libfast/libfastcommon-1.0.7.tar.gz ~/rpmbuild/SOURCE/
cp fdfs0302_centos7/source/libfast/libfastcommon.spec ~/rpmbuild/SPEC/
rpmbuild -bb ~/rpmbuild/SPECS/libfastcommon.spec    # 执行编译
# 成功后会在 rpmbuild/RPMS/x86_64/ 生成RPM包
ls ~/rpmbuild/RPMS/x86_64/
rpm -i libfastcommon-debuginfo-1.0.7-1.el7.centos.x86_64.rpm  
rpm -i libfastcommon-1.0.7-1.el7.centos.x86_64.rpm
rpm -i libfastcommon-devel-1.0.7-1.el7.centos.x86_64.rpm
```

### 3. 编译 fastdfs rpm包

``` bash
cp fdfs0302_centos7/source/fdfs5.0.5/* ~/rpmbuild/SOURCE/
cp fdfs0302_centos7/source/fdfs5.0.5/fastdfs_new.spec  ~/rpmbuild/SPEC/
rpmbuild -bb ~/rpmbuild/SPEC/fastdfs_new.spec
rpm -i fastdfs-5.0.5-7.el7.centos.x86_64.rpm
rpm -i fastdfs-tracker-5.0.5-7.el7.centos.x86_64.rpm
rpm -i fastdfs-storage-5.0.5-7.el7.centos.x86_64.rpm
rpm -i fastdfs-tool-5.0.5-7.el7.centos.x86_64.rpm
rpm -i libfdfsclient-5.0.5-7.el7.centos.x86_64.rpm
rpm -i libfdfsclient-devel-5.0.5-7.el7.centos.x86_64.rpm
rpm -i fastdfs-debuginfo-5.0.5-7.el7.centos.x86_64.rpm
```

### 4. 编译 nginx rpm包

``` bash
cp fdfs0302_centos7/source/nginx/* ~/rpmbuild/SOURCE/
cp fdfs0302_centos7/source/nginx/nginx_new.spec ~/rpmbuild/SOURCE/
rpmbuild -bb ~/rpmbuild/SPEC/nginx_new.spec
rpm -i nginx-1.7.9-3.el7.centos.x86_64.rpm
```

### 5. 安装脚本

``` bash
rpm -ivh libfast/libfastcommon-debuginfo-1.0.7-1.el7.centos.x86_64.rpm  
rpm -ivh libfast/libfastcommon-1.0.7-1.el7.centos.x86_64.rpm
rpm -ivh libfast/libfastcommon-devel-1.0.7-1.el7.centos.x86_64.rpm
rpm -ivh fdfs505rpm/fastdfs-5.0.5-7.el7.centos.x86_64.rpm
rpm -ivh fdfs505rpm/fastdfs-tracker-5.0.5-7.el7.centos.x86_64.rpm
rpm -ivh fdfs505rpm/fastdfs-storage-5.0.5-7.el7.centos.x86_64.rpm
rpm -ivh fdfs505rpm/fastdfs-tool-5.0.5-7.el7.centos.x86_64.rpm
rpm -ivh fdfs505rpm/libfdfsclient-5.0.5-7.el7.centos.x86_64.rpm
rpm -ivh fdfs505rpm/libfdfsclient-devel-5.0.5-7.el7.centos.x86_64.rpm
rpm -ivh fdfs505rpm/fastdfs-debuginfo-5.0.5-7.el7.centos.x86_64.rpm
rpm -ivh nginx179rpm/nginx-1.7.9-3.el7.centos.x86_64.rpm
```

### 6. 卸载脚本

``` bash 
rpm -e nginx-1.7.9-3.el7.centos.x86_64
rpm -e fastdfs-debuginfo-5.0.5-7.el7.centos.x86_64
rpm -e libfdfsclient-devel-5.0.5-7.el7.centos.x86_64
rpm -e libfdfsclient-5.0.5-7.el7.centos.x86_64
rpm -e fastdfs-tool-5.0.5-7.el7.centos.x86_64
rpm -e fastdfs-storage-5.0.5-7.el7.centos.x86_64
rpm -e fastdfs-tracker-5.0.5-7.el7.centos.x86_64
rpm -e fastdfs-5.0.5-7.el7.centos.x86_64
rpm -e libfastcommon-devel-1.0.7-1.el7.centos.x86_64
rpm -e libfastcommon-1.0.7-1.el7.centos.x86_64
rpm -e libfastcommon-debuginfo-1.0.7-1.el7.centos.x86_64  
```
