'use strict';

/* App Module */

var murderApp = angular.module('murderApp', [
  'murderServices',
  'murderFilters',
  'murderDirectives',
  'ui.router'
]);


var mysteryCtrl = murderApp.controller('MysteryCtrl', ['$scope', 'Cast', function($scope, Cast) {
  Cast.query(8).then(function(cast) { $scope.cast = cast });
  }]);

murderApp.config(function($stateProvider, $urlRouterProvider) {
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/mystery");
  // Now set up the states
  $stateProvider
    .state('mystery', {
      url: "/mystery",
      templateUrl: "partials/mystery.html",
      controller: 'MysteryCtrl'
    })
  });
