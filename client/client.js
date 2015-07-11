Accounts.ui.config({
  passwordSignupFields: "USERNAME_ONLY"
});

Meteor.startup(function () {
    $('.alert').alert()
    Meteor.subscribe('games');
    if (demo) {
	Meteor.subscribe('users');
    } else {
	Meteor.subscribe('users', function() {
	    if (!Router.current()) { return; }
	    var params = Router.current().params.query;
	    var wid = params.workerId;
	    var user = Meteor.user();
	    if (!wid) {
		Meteor.logout();
	    }
	    if (wid && (!user || user.username != wid)) {
		if (user && user.username != wid) {
		    Meteor.logout();
		}
		var result = Meteor.users.findOne({'username': params.workerId});
		if (!result) {
		    Accounts.createUser({'username': wid, 
					 'password': wid,
					 'profile': {assignmentId: params.assignmentId}});
		    
		} else {
		    Meteor.loginWithPassword(params.workerId, params.workerId);
		}
	    }
	});
    }			
});
