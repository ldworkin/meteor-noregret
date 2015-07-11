Template.wrapper.helpers({
    showStats: function() {
	var state = playerState();
	return (state == 'game' ||
		state == 'lobby');
    },
    demo: function() {
	return demo;
    }
});

Template.loggedout.helpers({
    demo: function() {
	return demo;
    }
});

Template.main.helpers({
    active: function() {
	if (Meteor.loggingIn()) {
	    return 'loading';
	}
	if (Meteor.user()) {
	    return playerState();
	}
	return 'loggedout';
    }
});
