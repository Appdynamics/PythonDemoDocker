var request = require('request');
var winston = require('winston');

/**************************
 * VARIABLES
 **************************/

var host = process.env.PYTHON_HOST;
var debugConsole = process.env.DEBUG_CONSOLE || false;
var consoleLevel = process.env.CONSOLE_LOG_LEVEL || 'info';
var logFilePath = process.env.LOG_PATH || ((process.cwd().indexOf('src') !== -1) ? '../logs/' : 'logs/');
var logFileLevel =  process.env.LOG_LEVEL || 'info';
var logFileName = host.replace('http://','') + '-' + process.pid + '-' + Date.now() + '.log';

/**************************
 * CHANGE ME
 *************************/
var pages = [
    {url : host + ':5000/'},
    {url : host +  ':5000/viewCatalog'},
    {url : host + ':5000/addToCart'},
    {url : host +  ':5000/checkout'},
    {url : host + ':5000/viewCart'},
    {url : host + ':5000/viewCart-removeItem'},
    {url : host + ':1080/'},
    {url : host + ':1080/signUp'}
];
var numberOfActiveSessions = 2;

/*************************
 * LOGGING
 *************************/
var logger = new winston.Logger({
    transports : [
        new (winston.transports.File)({
            name : 'file',
            filename : logFilePath + logFileName,
            level : logFileLevel
        })  ,
        new (winston.transports.Console)({
            name : 'console',
            level : consoleLevel
        })
    ]
});
if (!debugConsole) {
    logger.remove('console');
}

logger.log('info', 'Load script start', {
    host : host,
    debugConsole : debugConsole,
    consoleLevel : consoleLevel,
    logFilePath : logFilePath,
    logFileLevel :  logFileLevel,
    logFileName : logFileName
});
setTimeout(function() {
    logger.log('info','Heartbeat');
}, 10000);

/**************************
 * DONT CHANGE
 *************************/

var _getSteps = null;

var begin = function(pagesToExecute, numberOfSessions) {
    _getSteps = pagesToExecute;
    var numberOfSessions = numberOfSessions || 1;
    for (var i = 1; i <= numberOfSessions; i++) {
        logger.info('Initiating looping session :' + i);
        startSession(i);
    }
}

var startSession = function(sessionId) {
    logger.info('New session start for Id ' + sessionId);
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
        if (err) {
            logger.error(err);
        } else {
            logger.info('SessionId' + sessionId + ' - ' + options.url + ' : ' + resp.statusCode);
        }
        if (steps.length === 0) {
            startSession(sessionId);
        } else {
            nextStep(steps, jar, sessionId);
        }
    });
}
begin(pages, numberOfActiveSessions);