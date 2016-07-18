'use strict';

angular.module('app')
    .run(['$rootScope', '$state', '$stateParams',
        function ($rootScope, $state, $stateParams) {
            $rootScope.$state = $state;
            $rootScope.$stateParams = $stateParams;
        }
    ])
    .config(['$stateProvider', '$urlRouterProvider',
        function ($stateProvider, $urlRouterProvider) {
            $urlRouterProvider.otherwise('/app/codis');
            $stateProvider
                .state('app', {
                    abstract: true,
                    url: '/app',
                    templateUrl: 'static/tpl/app.html'
                })
                .state('app.codis', {
                    url: '/codis',
                    templateUrl: 'static/tpl/codis.html',
                    controller: 'CodisController'
                })
                .state('app.redis', {
                    url: '/redis',
                    templateUrl: 'static/tpl/redis.html',
                    controller: 'RedisController'
                })
                .state('app.setting', {
                    url: '/setting',
                    templateUrl: 'static/tpl/setting.html',
                    controller: 'SettingController'
                })
                .state('app.about', {
                    url: '/about',
                    templateUrl: 'static/tpl/about.html',
                    controller: 'AboutController'
                })
        }
    ]);