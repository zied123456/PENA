app.config(function($routeProvider, $locationProvider) {
    $routeProvider
        .when('/play', {
            templateUrl: 'app/play/playView.html',
            controller: 'playController'
        })
	    .otherwise({
	    	templateUrl: 'app/common/notfoundView.html'
	    });
});
