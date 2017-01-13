app.controller(
	'playController',
	function($scope, $rootScope, $timeout, $location, askService, tellService) {
		$rootScope.title = "Play | PENA";
		$scope.answers = {};
		$scope.character = {};
		$scope.limit = 10;
		$scope.context = 'loading';
		$scope.message = "I'm thinking of a question for you...";

		$scope.askPena = function(answers, limit) {
			askService.ask($scope.answers, limit)
				.then(function(response) {
					if (response.data.decision == 'CONTINUE') {
						$scope.context = 'question';
						$scope.question_name = response.data.data.next_question.name;
						$scope.question_text = response.data.data.next_question.text;
						$scope.message = $scope.question_text;
					} else if (response.data.decision == 'FOUND') {
						$scope.context = 'guess';
						$scope.message = 
							"Is it "+response.data.data.character_found+"?";
					} else if (response.data.decision == 'NOTFOUND') {
						if ($scope.limit < 20) {
							$scope.limit += 5;
							$scope.askPena($scope.answers, $scope.limit);
						} else {
							$scope.context = 'submit';
							$scope.message = "So who is it?";
						}
					} else {
						$scope.context = 'exception';
						if (response.data.data.exception) {
							$scope.message = response.data.data.exception;
						} else {
							$scope.message = 
								"Sorry, I can't understand what "
								+ "my server is telling me!";
						}
					}
				}, function(response) {
					$scope.context = 'exception';
					$scope.message = "Sorry, I can't even reach my server!";
				});
		}
		$scope.answerYes = function() {
			$scope.answers[$scope.question_name] = true;
			$scope.askPena($scope.answers, $scope.limit);
		};
		$scope.answerNo = function() {
			$scope.answers[$scope.question_name] = false;
			$scope.askPena($scope.answers, $scope.limit);
		};
		$scope.acceptAnswer = function() {
			$scope.context = 'success';
			$scope.message = "Yeiiiiiii!"
		}
		$scope.rejectAnswer = function() {
			if ($scope.limit < 20) {
				$scope.limit += 5;
				$scope.askPena($scope.answers, $scope.limit);
			} else {
				$scope.context = 'submit';
				$scope.message = "Then tell me who is it!";
			}
		}
		$scope.tellPena = function() {
			$scope.character = $scope.answers;
			$scope.character['name'] = $scope.characterName;
			tellService.tell($scope.character)
				.then(function(response) {
					if (response.data.decision == 'ACCEPTED') {
						$scope.context = 'success';
						$scope.message = "Thanks, I know someone new now!";
					} else if (response.data.decision == 'REJECTED') {
						$scope.context = 'exception';
						$scope.message = "For some reason, " 
							+ "I can't memorize your character!";
					} else {
						$scope.context = 'exception';
						if (response.data.data.exception) {
							$scope.message = response.data.data.exception;
						} else {
							$scope.message = 
								"Sorry, I don't know if my server "
								+ "understood my request or nah!";
						}
					}
				}, function(response) {
					$scope.context = 'exception';
					$scope.message = "Sorry, I can't reach my "
						+ "my distant memory to save your character!";
				});
		}

		$timeout(function() {
			$scope.askPena($scope.answers, $scope.limit);
		}, 2000);
	}
);
