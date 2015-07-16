Template.stats.helpers({
    thisScore: function() {
	var g = game();
	return sum(g.scores);
    },
    thisBonus: function() {
	var g = game();
	var amt = sum(g.scores) * 0.005;
	return amt.toFixed(2);
    },

    totalScore: function() {
	return Meteor.user().score;
    },
    totalBonus: function() {
	var amt = Meteor.user().score * 0.005;
	return amt.toFixed(2);
    }
});
