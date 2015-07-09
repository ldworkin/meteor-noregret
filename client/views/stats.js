Template.stats.helpers({
    numGames: function() {
	var user = Meteor.user();
	return user && user.games && user.games.length;
    },
    totalScore: function() {
	return Meteor.user().score;
    },
});
