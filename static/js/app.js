'use strict';

/* App Module */

var murderApp = angular.module('murderApp', [
  'murderServices',
  'murderFilters',
  'murderDirectives'
]);

var quotes = [
  ['“We\'ve all heard that a million monkeys banging on a million typewriters will eventually reproduce the entire works of Shakespeare. Now, thanks to the Internet, we know this is not true.”', 'Robert Wilensky'],
  ['“Ford!" he said, "there\'s an infinite number of monkeys outside who want to talk to us about this script for Hamlet they\'ve worked out.”', 'Douglas Adams'],
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
}]);

var mysteryCtrl = murderApp.controller('MysteryCtrl', ['$scope', '$location', 'Mystery', function($scope, $location, Mystery) {
  $scope.title = "";
  $scope.secret = false;

  function load() {
    var num_players =  $location.search().players || 8;
    Mystery.query(num_players).then(function(mystery) {
      $scope.cast = mystery.cast.characters;
      $scope.groups = mystery.cast.groups;
      $scope.murderer = mystery.cast.murderer;
      $scope.title = mystery.title;
      $scope.scene = mystery.scene;
      $scope.location = mystery.location;
      $scope.investigator = mystery.cast.investigator
      $scope.starter = mystery.cast.characters[0].relationships[Math.floor(Math.random() * mystery.cast.characters[0].relationships.length)];
    });
  };

  $scope.$watch(function () {
    return $location.hash
  }, function (players) {
    load();
  });
}]);
