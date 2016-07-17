'use strict';

angular.module('app').controller('RedisController', ['$scope', '$http', '$state', function($scope, $http, $state) {

    console.log('RedisController');

    $scope.results = [];
    $scope.db = 0;
    $scope.type = "string";
    $scope.key = "test:str:get";

    $scope.search = function() {
        $scope.results = [];
        var uri = '/search/' + $scope.db + "/" + $scope.key + "/" + $scope.type;
//        alert(uri)
        $http.get(uri).success(function(data) {
            $scope.results = data;
        }).error(function(data){
            console.log('error:' + data);
        });
    }

}]);