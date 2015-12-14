'use strict';

/* Filters */

var murderFilters = angular.module('murderFilters', []);


murderFilters.filter('description', function() {
  return function(input) {
    if(typeof input === "undefined") return "";

    var desType = {
      "social": "social standing",
      "professional": "business",
      "romantic": "sexual appetites",
      "familial": "family"
    };

    var desFreq = [
      "Paid the barest of attention to ",
      "Did the bare minimum for ",
      "Self-conscious about ",
      "Obsessive regarding "
    ];

    var possessive = (input.gender == "male" ? "his " : "her ");

    function join(statements) {
      if(statements.length <= 1) return statements
      else if(statements.length == 2) return statements.join(" and ")
      else return statements.slice(0, statements.length - 1).join(", ") + " and " + statements.slice(statements.length - 1);
    }

    if(input.relationships.length == 0) {
      return "A withdrawn loner, never seen in public."
    } else {
      var types = input.relationships.reduce(function(acc, relationship) {
        relationship.types.map(function(t) {
          acc[t] ? acc[t] += 1 : acc[t] = 1;
        });
        return acc;
      }, {});

      var counts = Object.keys(types).reduce(function(acc, t) {
        acc[types[t]] ? acc[types[t]] = acc[types[t]].concat(t) : acc[types[t]] = [t]
        return acc;
      }, {});

      var descendingCounts = Object.keys(counts).sort().reverse();
      return descendingCounts.map(function(count) {
        var out = desFreq.pop();
        if(count == 2) out + "both ";
        out += join(counts[count].map(function(t) {
            return possessive + desType[t];
          })) + ".";
        return out;
      }).join(" ");
    }
  };
});

murderFilters.filter('pluralize', function() {
  return function(input, group) {
    if(group.length > 1) {
      return input + "s";
    } else {
      return input;
    }
  };
});

murderFilters.filter('role', function() {
  return function(input) {
    if(input.id == 0) {
      return "The recently deceased " + input.name + "."
    } else {
      return input.name  + " (Player " + (input.id) + ")"
    }
  };
});

murderFilters.filter('phrasing', function() {
  return function(input, pastTense, victim) {
    if(typeof pastTense === "undefined") pastTense = false;

    var out = "";
    if(input.types.indexOf("romantic") >= 0 && input.types.indexOf("familial") >= 0) {
      out += (pastTense ? (typeof victim ==="undefined" ? "Was" : "were") : "are") + " married to ";
    }
    else if(input.types.indexOf("romantic") >= 0 && input.types.indexOf("professional") >= 0) {
      out += (pastTense ? (typeof victim ==="undefined" ? "Had" : "were having") : "are having") + " an affair with a colleague, ";
    }
    else if(input.types.indexOf("romantic") >= 0 && input.types.indexOf("social") >= 0) {
      out += (pastTense ? (typeof victim ==="undefined" ? "Was" : "were" ) : "are") + " both a friend and lover of ";
    }
    else if(input.types.indexOf("social") >= 0 && input.types.indexOf("professional") >= 0) {
      out += (pastTense ? "Often went" : "often go") + " drinking with a colleague, ";
    }
    else if(input.types.indexOf("social") >= 0 && input.types.indexOf("familial") >= 0) {
      out += (pastTense ? "Shared" : "share") + " hobbies with a family member, ";
    }
    else if(input.types.indexOf("familial") >= 0 && input.types.indexOf("professional") >= 0) {
      out += (pastTense ? "Worked" : "work") + " with a family member, ";
    }
    else if(input.types.indexOf("romantic") >= 0) {
      out += (pastTense ? (typeof victim ==="undefined" ? "Was" : "were" ) : "are") + " romantically entwined with "
    }
    else if(input.types.indexOf("familial") >= 0) {
        out += (pastTense ? "Had" : "have") + " family ties with ";
    }
    else if(input.types.indexOf("social") >= 0) {
      out += (pastTense ? (typeof victim ==="undefined" ? "Was" : "were") : "are") + " often seen socially with "
    }
    else if(input.types.indexOf("professional") >= 0) {
      out += (pastTense ? (typeof victim ==="undefined" ? "Was" : "were") : "are") + " said to work closely with "
    }
    if(typeof victim !== "undefined") {
      out += " the recently deceased " + victim.name;
      out = out.slice(0,1).toLowerCase() + out.slice(1);
    }
    else {
      if(input.character.id == 0) {
        out += " the recently deceased " + input.character.name
      }
      else {
        out += input.character.name  + " (Player " + (input.character.id) + ")"
      }
    }
    return out;
  };
});
