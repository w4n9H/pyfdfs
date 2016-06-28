/**
 * Created by wangyazhe on 16/2/3.
 */
var app = angular.module('fdfs_status', []);
app.controller('userCtrl', function($scope, $http) {
    $scope.fdfs = {
        'group_count': 'Unkonwn',
        'storage_count': 'Unkonwn',
        'active_storage': 'Unknown',
        'total_mb': 'Unkonwn',
        'used_mb': 'Unkonwn',
        'free_mb': 'Unkonwn'
    };
    $scope.groups = [
        {
            'group_name': 'Unkonwn',
            'server_count': 'Unkonwn',
            'active_count': 'Unkonwn',
            'total_mb': 'Unkonwn',
            'used_mb': 'Unkonwn',
            'free_mb': 'Unkonwn'
        }
    ];
    $scope.servers = [
        {
            'ip_addr': 'Unkonwn',
            'group': 'Unkonwn',
            'version': 'Unkonwn',
            'up_time': 'Unkonwn',
            'status': 'Unkonwn',
            'store_path_count': 'Unkonwn',
            'total_mb': 'Unkonwn',
            'used_mb': 'Unkonwn',
            'free_mb': 'Unkonwn'
        }
    ];
    $scope.storage_update = function() {
        $http.get('http://192.168.11.129:8080/v1/storage'
        ).success(function (response) {
                $scope.fdfs = response.result.all_info;
                $scope.groups = response.result.all_group;
                $scope.servers = response.result.group_detail;
        }).error(function () {
                alert('发送失败')
        });
    };
});
