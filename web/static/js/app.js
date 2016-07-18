'use strict';

var myApp = angular.module('app', ['ui.router', 'smart-table', 'toaster', 'ngAnimate']);

myApp.controller('AppCtrl', ['$scope', '$http', '$state', function($scope, $http, $state) {
    console.log('AppCtrl');

    $scope.app = {
        name:"Codis Admin",
        version:"0.0.1"
    }
}]);