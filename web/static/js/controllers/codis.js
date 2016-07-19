'use strict';

angular.module('app').controller('CodisController', ['$scope', '$http', '$state', 'toaster', function($scope, $http, $state, toaster) {
    console.log('CodisController');
    $scope.proxies = {};
    $scope.groups = {};
    $scope.slaves = {};

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

    $scope.refreshProxy();
    $scope.refreshServer();

}]);