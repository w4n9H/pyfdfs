# PyFDFS 后端接口文档


### 1.需求信息
+ 使用 RESTful 风格的API
+ 上传,下载,删除文件,获取文件信息,获取存储集群状态
+ 支持身份认证auth (未实现)


### 2.API
+ 2.1.主要API信息

``` bash
文件上传
POST http://xxx.com/v1/upload?domain=xxxxx&filename=xxxxx&hash=false
(domain指定域空间默认test, 
filename指定文件名,不指定使用原始文件名,
hash为true计算hash,默认为false不计算
replace参数当存在domain和文件名相同的情况时是否覆盖,默认true覆盖
redis参数决定是否存储索引至redis,默认为false不存储,接口暂时不可用)
文件下载
GET http://xxx.com/v1/download/domain(域名称)/file_name(文件名)
文件删除
GET http://xxx.com/v1/delete/domain(域名称)/file_name(文件名)
文件信息
GET http://xxx.com/v1/info/domain(域名称)/file_name(文件名)
存储服务器状态
GET http://xxx.com/v1/storage
获取所有 domain
GET http://xxx.com/v1/list_domain
获取domain中的文件名
GET http://xxx.com/v1/list_file?domain=test&limit=100 (默认domain:test,默认limit:10)
新建 domain
GET http://xxx.com/v1/create_domain/domain_name(域名称)
删除 domain (该 domain 没有文件)
GET http://xxx.com/v1/delete_domain/domain_name(域名称)
#
返回信息
{"status": 0, "result": "xxxxxxx"}
status : 状态码
result : 返回具体信息,包括正确查询信息或者错误信息
```


### 使用 API (Python)

