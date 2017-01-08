app.service('tellService', function($http) {
	this.tell = function (character) {
		var promise = $http.post(
			"api/v1/pena/tell",
			character
		).then(function(response) {
			return response;
		});

		return promise;
	}
});
