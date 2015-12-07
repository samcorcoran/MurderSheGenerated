'use strict';

/* Filters */

var murderFilters = angular.module('murderFilters', []);

murderFilters.filter('phrasing', function() {
  return function(input) {
    var out = "";
    if(input.types.indexOf("romantic") >= 0 && input.types.indexOf("familial") >= 0) {
      out += "Incestuously involved with ";
    }
    else if(input.types.indexOf("romantic") >= 0) {
      out += "Romantically entwined with "
    }
    else if(input.types.indexOf("familial") >= 0) {
      out += "Has family ties with ";
    }
    else if(input.types.indexOf("social") >= 0) {
      out += "Often seen socially with "
    }
    else if(input.types.indexOf("professional") >= 0) {
      out += "Works together with "
    }
    out += input.character.name  + " (Player " + (input.character.id + 1) + ")"
    return out;
  };
});
