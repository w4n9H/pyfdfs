/**
* ajax 上传文件
*/
function query_info() {
    var domain_name = $("#input_domain_name").val();
    var file_name = $("#input_file_name").val();
    var url = '/v1/info/' + domain_name + '/' + file_name;
    $.ajax({
        url : url,
        type : 'GET',
        success : function(responseStr) {
            if (responseStr.status == 0){
                alert('成功');
                var html = "";
                html += "<tr><td>" + responseStr.result.file_name + "</td>";
                html += "<td>" + responseStr.result.file_md5 + "</td>";
                html += "<td>" + responseStr.result.file_crc32 + "</td>";
                html += "<td>" + responseStr.result.file_size + "</td>";
                html += "<td>" + responseStr.result.domain_name + "</td>";
                html += "<td><a href='/v1/download/" + domain_name + '/' + file_name + "'>下载</a></td></tr>";
                $("#fdfs_query_file").html(html);
            }
            else{
                alert("失败：" + JSON.stringify(responseStr));
            }
        },
        error : function(responseStr) {
            alert("失败:" + JSON.stringify(responseStr));    //将    json对象    转成    json字符串。
        }
    });
}
function query_info_op(domain_name, file_name) {
    var url = '/v1/info/' + domain_name + '/' + file_name;
    $.ajax({
        url : url,
        type : 'GET',
        success : function(responseStr) {
            if (responseStr.status == 0){
                alert('成功');
                var html = "";
                html += "<tr><td>" + responseStr.result.file_name + "</td>";
                html += "<td>" + responseStr.result.file_md5 + "</td>";
                html += "<td>" + responseStr.result.file_crc32 + "</td>";
                html += "<td>" + responseStr.result.file_size + "</td>";
                html += "<td>" + responseStr.result.domain_name + "</td>";
                html += "<td><a href='/v1/download/" + domain_name + '/' + file_name + "'>下载</a></td></tr>";
                $("#fdfs_query_file").html(html);
            }
            else{
                alert("失败：" + JSON.stringify(responseStr));
            }
        },
        error : function(responseStr) {
            alert("失败:" + JSON.stringify(responseStr));    //将    json对象    转成    json字符串。
        }
    });
}
function uploadByForm() {
    var formData = new FormData($("#myForm")[0]);    //用form 表单直接 构造formData 对象; 就不需要下面的append 方法来为表单进行赋值了。
    var url = "/v1/upload?domain=test&hash=true";
    $.ajax({
        url : url,
        type : 'POST',
        data : formData,
        /**
         * 必须false才会避开jQuery对 formdata 的默认处理
         * XMLHttpRequest会对 formdata 进行正确的处理
         */
        processData : false,
        /**
         *必须false才会自动加上正确的Content-Type
         */
        contentType : false,
        /**
         *上传文件不需要缓存
         */
        cache: false,
        success : function(responseStr) {
            if (responseStr.status == 0){
                query_info_op('test', responseStr.result)
            }
            else{
                alert("失败：" + JSON.stringify(responseStr));
            }
        },
        error : function(responseStr) {
            alert("失败:" + JSON.stringify(responseStr));    //将    json对象    转成    json字符串。
        }
    });
}


