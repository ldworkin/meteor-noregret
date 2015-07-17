Template.game.helpers({
    gameNum: function() {
	var user = Meteor.user();
	var g = game();
	if (!user || !g || !user.games) {return;}
	var number = user.games.length;
	if (g.status != 'over') {
	    number += 1;
	}
	return number;
    },
    numGames: function() {
	return sequences.length;
    },
    done: function() {
	var u = Meteor.user();
	var length = sequences.length;
	return u && u.games && u.games.length == length;
    },
    step: function() {
	var g = game();
	var number = g.step;
	if (g.status != 'over') {	    
	    number += 1;
	}
	return number;
    },    
    totalSteps: function() {
	var g = game();
	return g && sequences[g.sequence_id].length;
    },
    showPrevious: function() {
	var g = game();
	return g && game().step > 0;   
    },
    playing: function() {
	var g = game();
	return g && g.status != 'over';
    },
    notPlaying: function() {
	var g = game();
	return g && g.status == 'over';
    },
    results: function() {
	var r = results();
	return r[r.length-1];
    },
    payoffs: function() {
	var r = results();
	var obj = {'you': 0,
		   'e1': 0,
		   'e2': 0};
	for (var i=0; i<r.length; i++) {
	    obj['you'] += r[i]['payoff'];
	    obj['e1'] += r[i]['e1'];
	    obj['e2'] += r[i]['e2'];
	}
	return obj;
    },
    instructionsOpen: function() {
	return Session.get('instructionsOpen');
    }
});

Template.game.events({
    "click .predict": function(e) {
	Meteor.call('makePrediction', parseInt(e.target.value));
    },
    "click .next": function() {
	var g = game();	
	Meteor.call('newGame', g.sequence_id + 1);
    },
    "click .continue": function() {
	Meteor.call('setState', 'submit');
    },
    "click .collapser": function() {
	var prev = Session.get('instructionsOpen');
	Session.set('instructionsOpen', !prev);
    }
});
