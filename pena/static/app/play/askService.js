app.service('askService', function($http) {
	this.ask = function (answers, limit) {
		var promise = $http.post(
			"api/v1/pena/ask?limit="+limit,
			answers
		).then(function(response) {
			return response;
		});

		return promise;
	}
});
