Games = new Meteor.Collection('games');

Meteor.methods({
    newGame: function(sid) {
	var game_id = Games.insert({start: new Date(),
				    player: Meteor.userId(),
				    status: 'playing',
				    sequence_id: sid,
				    step: 0,
				    predictions: [],
				    scores: [],
				    timestamps: []});
	Meteor.users.update({_id: Meteor.userId()},
			    {$set: {state: 'game',
				    'game.game_id': game_id}});
    },
    makePrediction: function(expert) {
	var g = game();
	var step = g.step;
	var sequence = sequences[seqIds[g.sequence_id]];
	var obj = {};
	var payoff = sequence[step][expert];
	obj['predictions'] = expert;
	obj['scores'] = payoff;
	obj['timestamps'] = new Date();
	Games.update({_id: g._id},
		     {$inc: {step: 1},
		      $push: obj});
	Meteor.users.update({_id: pid()},
			    {$inc: {score: payoff}});
	if (step == sequence.length - 1) {
	    Games.update({_id: g._id},
			 {$set: {status: 'over'}});
	    Meteor.users.update({_id: pid()},
				{$push: {games: gid()}});	    
	}
    },
    completeHIT: function() {
	Meteor.users.update({_id: pid()},
			    {$set: {submitted: true}});
    },
    setState: function(state) {
	Meteor.users.update({_id: pid()},
			    {$set: {state: state}});

    },
});
