Template.instructions.helpers({
});

Template.instructions.events({
    "click .game": function () {
	Meteor.call('newGame', 0);
    },
});
