'use strict';

angular.module('app').controller('RedisController', ['$scope', '$http', '$state', 'toaster', function ($scope, $http, $state, toaster) {
    console.log('RedisController');

    $scope.search_result_keys = [];
    $scope.search_result_count = 0;
    $scope.search_result_item_per_Page = 10;

    $scope.redis_slave = "";
    $scope.redis_key = "";
    $scope.redis_type = "";
    $scope.redis_value = "";
    $scope.redis_start = 0;
    $scope.redis_stop = -1;
    $scope.redis_count = 1;

    $scope.row_status = [];
    for (var i = 0; i < $scope.search_result_item_per_Page; i++) {
        $scope.row_status[i] = true;
    }

    $scope.resetRowStatus = function (index) {
        for (var i = 0; i < $scope.row_status.length; i++) {
            $scope.row_status[i] = true;
        }
    }

    $scope.search = function (key) {
        $http.get('/api/search/' + key).success(function (data) {
            $scope.resetRowStatus();
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
        }).error(function (data) {
            console.log('error:' + data);
        });
    }

    $scope.select = function (index, search_key) {
        if (!$scope.row_status[index]) {
            $scope.row_status[index] = !$scope.row_status[index]
        } else {
            $http.get('/api/type/' + search_key.addr + '/' + search_key.key).success(function (data) {
                $scope.redis_slave = search_key.addr;
                $scope.redis_key = search_key.key;
                $scope.redis_value = "";
                $scope.redis_type = data.type;
                console.log('$scope.redis_type=' + $scope.redis_type);
                if ($scope.redis_type == 'zset') {
                    $scope.redis_start = 0;
                    $scope.redis_stop = -1;
                }
                else if ($scope.redis_type == 'set') {
                    $scope.redis_count = 1;
                }
                $scope.resetRowStatus(index);
                $scope.row_status[index] = !$scope.row_status[index]
            }).error(function (data) {
                console.log('error:' + data);
                toaster.pop('error', "", data);
            });
        }
    }

    $scope.string_get = function () {
        $http.get('/api/string/get/' + $scope.redis_slave + '/' + $scope.redis_key).success(function (data) {
            $scope.redis_value = data.value;
            console.log('$scope.redis_value=' + $scope.redis_value);
            if ($scope.redis_value.length == 0) {
                toaster.pop('info', "", "The value is empty.");
            }
        }).error(function (data) {
            console.log('error:' + data);
        });
    }

    $scope.zset_zrange = function () {
        $http.get('/api/zset/zrange/' + $scope.redis_slave + '/' + $scope.redis_key + '/' + $scope.redis_start + '/'
            + $scope.redis_stop).success(function (data) {
            $scope.redis_value = data.value;
            console.log('$scope.redis_value=' + $scope.redis_value);
        }).error(function (data) {
            console.log('error:' + data);
            toaster.pop('error', "", data);
        });
    }

    $scope.zset_zcard = function () {
        $http.get('/api/zset/zcard/' + $scope.redis_slave + '/' + $scope.redis_key).success(function (data) {
            $scope.redis_value = data.value;
            console.log('$scope.redis_value=' + $scope.redis_value);
        }).error(function (data) {
            console.log('error:' + data);
            toaster.pop('error', "", data);
        });
    }

    $scope.set_srandmember = function () {
        $http.get('/api/set/srandmember/' + $scope.redis_slave + '/' + $scope.redis_key + '/' + $scope.redis_count)
            .success(function (data) {
            $scope.redis_value = data.value;
            console.log('$scope.redis_value=' + $scope.redis_value);
        }).error(function (data) {
            console.log('error:' + data);
            toaster.pop('error', "", data);
        });
    }

    $scope.set_smembers = function () {
        $http.get('/api/set/smembers/' + $scope.redis_slave + '/' + $scope.redis_key)
            .success(function (data) {
            $scope.redis_value = data.value;
            console.log('$scope.redis_value=' + $scope.redis_value);
        }).error(function (data) {
            console.log('error:' + data);
            toaster.pop('error', "", data);
        });
    }

    $scope.set_scard = function (count) {
        $http.get('/api/set/scard/' + $scope.redis_slave + '/' + $scope.redis_key).success(function (data) {
            $scope.redis_value = data.value;
            console.log('$scope.redis_value=' + $scope.redis_value);
        }).error(function (data) {
            console.log('error:' + data);
            toaster.pop('error', "", data);
        });
    }

}]);