app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'app/home/homeView.html'
        })
        .when('/play', {
            templateUrl: 'app/play/playView.html',
            controller: 'playController'
        })
        .when('/about', {
            templateUrl: 'app/about/aboutView.html'
        })
	    .otherwise({
	    	templateUrl: 'app/common/notfoundView.html'
	    });
});
