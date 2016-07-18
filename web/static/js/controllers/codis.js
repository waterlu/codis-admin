'use strict';

angular.module('app').controller('CodisController', ['$scope', '$http', '$state', function($scope, $http, $state) {
    console.log('CodisController');
    $scope.proxies = {};
    $scope.groups = {};
    $scope.slaves = {};
    $scope.search_result_keys = {};
    $scope.search_result_collection = [];

    $scope.redis_slave = "";
    $scope.redis_key = "";


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
        $scope.keys = {};
        $http.get('/api/search/' + key).success(function(data) {
            $scope.search_result_collection = data.data;
            $scope.search_result_page = data.page;
            console.log('$scope.search_result_collection=' + $scope.search_result_collection);
            console.log('$scope.search_result_page=' + $scope.search_result_page);
        }).error(function(data){
            console.log('error:' + data);
        });
    }
    
    $scope.fill = function (search_key) {
        $scope.redis_slave = search_key.addr;
        $scope.redis_key = search_key.key;
    }

    $scope.refreshProxy();
    $scope.refreshServer();

}]);