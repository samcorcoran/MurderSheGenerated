'use strict';

/* Services */

var murderServices = angular.module('murderServices', ['ngResource']);

murderServices.factory('Cast', ['$http', function($http) {
	var initialized = false;
	var cast = [];

	function castingCall(players) {
		console.log("Casting call!");
		cast = $http.get('/cast/' + players).then(function(httpResponse) {
	    if(httpResponse == null) return null;
			console.log("Cast assembled.");
      initialized = true;
	    return httpResponse.data;
	  }).catch(function(err) {
	    console.error(err);
	  });
		return cast;
	}

  let f = {};

  f.query = function(players) { return (initialized && cast.length == players ? cast : castingCall(players)) };

  return f;
}]);
