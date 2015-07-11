Template.stats.helpers({
    numGames: function() {
	var user = Meteor.user();
	return user && user.games && user.games.length;
    },
    totalScore: function() {
	return Meteor.user().score;
    },
    totalBonus: function() {
	var amt = Meteor.user().score * 0.005;
	return amt.toFixed(2);
    }
});
