var request = require('request');

/*************************
 * CHANGE ME
 ************************/
var host = 'http://staging-ecommerce.demo.appdynamics.com';
var numberOfActiveSessions = 5;

/**************************
 * ECOMMERCE VARIABLES
 *************************/
var pages = [
    {
        url : host + '/appdynamicspilot/UserLogin.action',
        form : {
            loginName : 'aleftik',
            password : 'aleftik'
        }
    },
    {
        url : host +  '/appdynamicspilot/ViewItems.action'
    },
    {
        url : host + '/appdynamicspilot/ViewCart!addToCart.action',
        form : {
            username : 'aleftik',
            selectedId : 1,
            selectedId : 2,
            selectedItemId:',1,2'
        }
    },
    {
        url : host +  '/appdynamicspilot/ViewCart!sendItems.action',
        form : {
            username : 'aleftik'
        }
    }
]

var users = [];
var indexOfUsers = 0;

var getPages = function() {
    var user =  users[indexOfUsers];
    pages[0].form.loginName = user.email;
    pages[0].form.password = user.password;
    pages[2].form.username = user.email;
    pages[3].form.username = user.email;
    if (indexOfUsers < (users.length -1)) {
        indexOfUsers++;
    } else {
        indexOfUsers = 0;
    }
    console.log('Username for session set to ' + user.email);
    return pages;
}


/**************************
 * DONT CHANGE
 *************************/
var _getSteps = null;

var begin = function(pagesToExecute, numberOfSessions) {
    _getSteps = pagesToExecute;
    var numberOfSessions = numberOfSessions || 1;
    for (var i = 1; i <= numberOfSessions; i++) {
        console.log('Initiating looping session :' + i);
        startSession(i);
    }
}

var startSession = function(sessionId) {
    console.log('New session start for Id ' + sessionId);
    var steps = JSON.parse(JSON.stringify(typeof(_getSteps) === 'function' ? _getSteps() : _getSteps));
    nextStep(steps, request.jar(), sessionId);
}

var nextStep = function(steps, jar, sessionId) {
    var currentPage = steps.shift();
    var options = {url : currentPage.url, jar : jar};
    var method = 'get';
    if (currentPage.form) {
        var method = 'post';
        options.form = currentPage.form;
    }
    request[method](options, function(err, resp, body) {
        if (err) console.error(err);
        console.log('SessionId' + sessionId + ' - ' + options.url + ' : ' + resp.statusCode);
        if (steps.length === 0) {
            startSession(sessionId);
        } else {
            nextStep(steps, jar, sessionId);
        }
    });
}

request(host + '/appdynamicspilot/rest/json/user/all', function(err,resp,body) {
    users = JSON.parse(body);
    begin(getPages, numberOfActiveSessions);
});