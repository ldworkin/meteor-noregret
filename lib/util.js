pid = function() {
    var u = Meteor.user();
    return u && u._id;
};

gid = function() {
    var u = Meteor.user();
    return u && u.game.game_id;
};

game = function() {
    var u = Meteor.user();
    return u && Games.findOne(u.game.game_id);
};

playerState = function() {
    var u = Meteor.user()
    return u && u.state;
};

results = function() {
    var g = game();
    var objects = [];
    var sequence = sequences[seqIds[g.sequence_id]];
    for (var i=0; i<g.step; i++) {
	var object = {'step_': i+1,
		      'e1': sequence[i][0],
		      'e2': sequence[i][1],
		      'choice': g.predictions[i] + 1,
		      'payoff': g.scores[i]};
	objects.push(object);
    }
    return objects;
};

sum = function(array) {
    var total = 0;
    for (var i=0; i<array.length; i++) {
	total += array[i];
    }
    return total;
}
