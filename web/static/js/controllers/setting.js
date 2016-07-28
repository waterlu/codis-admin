'use strict';

angular.module('app').controller('SettingController', ['$scope', '$http', '$state', function($scope, $http, $state) {

    console.log('SettingController');

    $scope.zk_addr = "";
    $scope.product_name = "";
    $scope.max_count = 0;
    $scope.use_proxy_ip = false;
    $scope.servers = 0;
    $scope.readonly = true;
    $scope.zk_addr_bak = "";
    $scope.product_name_bak = "";
    $scope.max_count_bak = 0;
    $scope.use_proxy_ip_bak = false;

    $scope.refreshSetting = function() {
        $http.get('/api/setting').success(function(data) {
            data = data.data
            $scope.zk_addr = data.zk_addr;
            $scope.product_name = data.product_name;
            $scope.max_count = data.max_count;
            $scope.use_proxy_ip = data.use_proxy_ip;
            console.log('$scope.zk_addr=' + $scope.zk_addr);
            console.log('$scope.product_name=' + $scope.product_name);
            console.log('$scope.max_count=' + $scope.max_count);
            console.log('$scope.use_proxy_ip=' + $scope.use_proxy_ip);
        }).error(function(data){
            console.log('error:' + data);
        });
    }

    $scope.refreshStatus = function() {
        $http.get('/api/status').success(function(data) {
            $scope.servers = data.data;
            console.log('$scope.servers=' + $scope.servers);
        }).error(function(data){
            console.log('error:' + data);
        });
    }

    $scope.editSetting = function () {
        $scope.readonly = false;
        $scope.zk_addr_bak = $scope.zk_addr
        $scope.product_name_bak = $scope.product_name
        $scope.max_count_bak = $scope.max_count
        $scope.use_proxy_ip_bak = $scope.use_proxy_ip
    }

    $scope.cancelSetting = function () {
        $scope.readonly = true;
        $scope.zk_addr = $scope.zk_addr_bak
        $scope.product_name = $scope.product_name_bak
        $scope.max_count = $scope.max_count_bak
        $scope.use_proxy_ip = $scope.use_proxy_ip_bak
    }

    $scope.saveSetting = function () {
        $scope.readonly = true;
        $http({method: "POST",
            url: "/api/setting",
            data: {
                "zk_addr": $scope.zk_addr,
                "product_name": $scope.product_name,
                "max_count": $scope.max_count,
                "use_proxy_ip": $scope.use_proxy_ip
            }
        }).success(function(data) {
            data = data.data
            $scope.zk_addr = data.zk_addr;
            $scope.product_name = data.product_name;
            $scope.max_count = data.max_count;
            $scope.use_proxy_ip = data.use_proxy_ip;
            $scope.servers = data.servers;
        }).error(function(data){
            console.log('error:' + data);
        });
    }

    $scope.refreshSetting();
    $scope.refreshStatus();

}]);