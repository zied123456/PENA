app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'app/home/homeView.html',
            controller: 'homeController'
        })
        .when('/play', {
            templateUrl: 'app/play/playView.html',
            controller: 'playController'
        })
        .when('/about', {
            templateUrl: 'app/about/aboutView.html',
            controller: 'aboutController'
        })
        .otherwise({
            templateUrl: 'app/notfound/notfoundView.html',
            controller: 'notfoundController'
        });
});
