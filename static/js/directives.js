'use strict';

/* Directives */

var murderDirectives = angular.module('murderDirectives', []);

murderDirectives.directive('suspect', function() {
  return {
    restrict: 'E',
		scope: {
			character: "=",
			victim: "="
		},
    templateUrl: 'partials/character.html'
  };
});

murderDirectives.directive('victim', function() {
  return {
    restrict: 'E',
		scope: {
			character: "="
		},
    templateUrl: 'partials/victim.html'
  };
});

murderDirectives.directive('group', function() {
  return {
    restrict: 'E',
		scope: {
			group: "="
		},
    templateUrl: 'partials/group.html'
  };
});

murderDirectives.directive('cast', function() {

  var controller = ['$scope', function($scope) {
		$scope.$watch("cast", function(oldValue, newValue) {
			if(newValue != oldValue) {
				$scope.victim = $scope.cast[0];
				$scope.suspects = $scope.cast.slice(1);
			  }
			});
    }];

  return {
    restrict: 'A',
    templateUrl: 'partials/cast.html',
    controller: controller
  };
});

murderDirectives.directive('permalink', function() {

  var controller = ['$scope', function($scope) {
    }];

  return {
    restrict: 'A',
    templateUrl: 'partials/permalink.html',
    controller: controller
  };
});
