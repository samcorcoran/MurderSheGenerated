'use strict';

/* App Module */

var murderApp = angular.module('murderApp', [
  'murderServices',
  'murderFilters',
  'murderDirectives',
  'ui.router'
]);

var quotes = [
  ['“When you read the account of a murder - or, say, a fiction story based on murder - you usually begin with the murder itself. That\'s all wrong. The murder begins a long time beforehand. A murder is the culmination of a lot of different circumstances, all converging at a given moment at a given point. People are brought into it from different parts of the globe and for unforeseen reasons. The murder itself is the end of the story. It\'s Zero Hour.”', 'Agatha Christie'],
  ['“We\'ve all heard that a million monkeys banging on a million typewriters will eventually reproduce the entire works of Shakespeare. Now, thanks to the Internet, we know this is not true.”', 'Robert Wilensky'],
  ['“Ford!" he said, "there\'s an infinite number of monkeys outside who want to talk to us about this script for Hamlet they\'ve worked out.” — Douglas Adams'],
  ['“I like to write literature that reads like pulp fiction.”', 'Nike N. Chillemi'],
  ['“Ah, but my dear sir, the why must never be obvious. That is the whole point.”', 'Agatha Christie'],
  ['“The impossible could not have happened, therefore the impossible must be possible in spite of appearances.”', 'Agatha Christie'],
  ['“Instinct is a marvelous thing. It can neither be explained nor ignored.”', 'Agatha Christie'],
  ['“...and then a murder mystery will occur.”', 'Natsuki Takaya'],
  ['“Every murderer is probably somebody\'s old friend.”', 'Agatha Christie'],
  ['“A trillion chimpanzees typing for a trillion years still couldn’t create the garbage in the slush pile.”' ,'Unknown']
];

var quoteCtrl = murderApp.controller('QuoteCtrl', ['$scope', function($scope) {
  var quote = quotes[Math.floor((Math.random() * quotes.length))];
  $scope.quote = {text: quote[0], source: quote[1]};
  console.log($scope.quote.text + " ― " + $scope.quote.source);
}]);

var mysteryCtrl = murderApp.controller('MysteryCtrl', ['$scope', 'Cast', function($scope, Cast) {
  Cast.query(9).then(function(cast) {
    $scope.cast = cast.characters;
    $scope.groups = cast.groups;
  });
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
