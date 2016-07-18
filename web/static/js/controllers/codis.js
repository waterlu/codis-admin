'use strict';

angular.module('app').controller('CodisController', ['$scope', '$http', '$state', 'toaster', function($scope, $http, $state, toaster) {
    console.log('CodisController');
    $scope.proxies = {};
    $scope.groups = {};
    $scope.slaves = {};
    $scope.search_result_keys = [];
    $scope.search_result_count = 0;
    $scope.search_result_item_per_Page = 10;

    $scope.redis_slave = "";
    $scope.redis_key = "";
    $scope.redis_type = "";
    $scope.redis_value = "";


    $scope.refreshProxy = function() {
        $http.get('/api/proxy').success(function(data) {
            $scope.proxies = data;
            console.log('$scope.proxies=' + $scope.proxies);
        }).error(function(data){
            console.log('error:' + data);
        });
    }

    $scope.refreshServer = function() {
        $http.get('/api/groups').success(function(data) {
            $scope.groups = data;
            console.log('$scope.groups=' + $scope.groups);
        }).error(function(data){
            console.log('error:' + data);
        });

        $http.get('/api/redis').success(function(data) {
            $scope.slaves = data;
            console.log('$scope.slaves=' + $scope.slaves);
        }).error(function(data){
            console.log('error:' + data);
        });
    }
    
    $scope.search = function(key) {
        $http.get('/api/search/' + key).success(function(data) {
            $scope.search_result_count = data.count;
            $scope.search_result_keys = data.data;
            var errorCode = data.errorCode
            if (errorCode > 0) {
                var errorMessage = data.errorMsg;
                toaster.pop('error', "", errorMessage);
                return;
            }
            console.log('$scope.search_result_keys=' + $scope.search_result_keys);
            console.log('$scope.search_result_count=' + $scope.search_result_count);
            if ($scope.search_result_keys.length == 0) {
                toaster.pop('warning', "", "Can not find the key [" + key + "] in redis server!");
            }
        }).error(function(data){
            console.log('error:' + data);
        });
    }
    
    $scope.select = function (search_key) {
        $http.get('/api/type/' + search_key.addr + '/' + search_key.key).success(function(data) {
            $scope.redis_type = data.type;
            console.log('$scope.redis_type=' + $scope.redis_type);
        }).error(function(data){
            console.log('error:' + data);
        });

        $scope.redis_slave = search_key.addr;
        $scope.redis_key = search_key.key;
        $scope.redis_value = "";
    }

    $scope.search_value = function () {
        if ($scope.redis_type == 'string') {
            $http.get('/api/string/get/' + $scope.redis_slave + '/' + $scope.redis_key).success(function(data) {
                $scope.redis_value = data.value;
                console.log('$scope.redis_value=' + $scope.redis_value);
            }).error(function(data){
                console.log('error:' + data);
            });
        }
        else if ($scope.redis_type == 'list') {

        }
        else if ($scope.redis_type == 'set') {

        }
        else if ($scope.redis_type == 'zset') {

        }
        else{
            toaster.pop('error', "", "The type " + $scope.redis_type + " is not support!");
        }
    }

    $scope.refreshProxy();
    $scope.refreshServer();

}]);