'use strict';

/* Directives */

var murderDirectives = angular.module('murderDirectives', []);

murderDirectives.directive('character', function() {

	var controller = ['$scope', function ($scope) {
    }];

  return {
    restrict: 'A',
		scope: {
			character: "=",
			cast: "="
		},
    templateUrl: 'partials/character.html',
    controller: controller
  };
});

murderDirectives.directive('cast', function() {

  var controller = ['$scope', function($scope) {
    }];

  return {
    restrict: 'A',
    scope: {
      cast: "="
    },
    templateUrl: 'partials/cast.html',
    controller: controller
  };
});
