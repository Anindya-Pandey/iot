var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var deviceClasses = require('./deviceClasses');
var motorArray = [];
var gsocket;
var tankArray = [];
var deviceArray = [];

function inDeviceArray() {
 var i = 0;
 deviceArray = [];
 while ( i < motorArray.length ) {
  deviceArray.push(JSON.stringify(motorArray[i].jsonRep));
  i=i+1;
 }
 i=0;
 while ( i < tankArray.length ) {
  deviceArray.push(JSON.stringify(tankArray[i].jsonRep));
  i=i+1;
 }
}

function deviceArrayJson() {
 var i = 0;
 var deviceArrayString = '';
 while (i < deviceArray.length) {
  if (i==0) {
   deviceArrayString = deviceArrayString +deviceArray[i];
  }
  else {
   deviceArrayString = deviceArrayString + ',' + deviceArray[i];
  }
  i=i+1;
 }
 console.log(deviceArrayString);
 return deviceArrayString;
}

var routes = require('./app_api/routes/index');
var users = require('./app_api/routes/users');

var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/view', function (req, res, next) {
 res.render('view',JSON.parse('{"devices":['+deviceArrayJson()+']}'));
});

app.get('/changeLink/:deviceName', function (req, res, next) {
 res.render('changeLink',JSON.parse('{"name":"'+req.params.deviceName+'","devices":['+deviceArrayJson()+']}'));
});

app.get('/connect/:deviceName/:deviceType/:toName', function (req, res, next) {
 var i = 0;
 var name = req.params.deviceName;
 var toName = req.params.toName;
 if ( req.params.deviceType == 'motor' ) {
  var motor = motorArray[parseInt(name[name.length-1])];
  if (motor.tankLinks.indexOf(toName) <= -1) {
   var tank = tankArray[parseInt(toName[toName.length-1])];
   io.sockets.emit('cnct',{'name': name, 'tankName': toName, 'status': tank.status, 'level': tank.level});
   io.sockets.emit('cnct',{'name': toName, 'motorName': name, 'status': motor.status});
   motor.tankLinks.push(toName);
   motor.changeJsonRep();
   tank.motorLinks.push(name);
   tank.changeJsonRep();
  }
 }
 else {
  var motor = motorArray[parseInt(toName[toName.length-1])];
  var tank = tankArray[parseInt(name[name.length-1])];
  if (tank.motorLinks.indexOf(toName) <= -1) {
   io.sockets.emit('cnct',{'name': toName, 'tankName': name, 'status': tank.status, 'level': tank.level});
   io.sockets.emit('cnct',{'name': name, 'motorName': toName, 'status': motor.status});
   motor.tankLinks.push(name);
   motor.changeJsonRep();
   tank.motorLinks.push(toName);
   tank.changeJsonRep();
  }
 }
 inDeviceArray();
 deviceArrayJson();
 //console.log(deviceArrayJson());
 res.render('changeLink',JSON.parse('{"name":"'+req.params.deviceName+'","devices":['+deviceArrayJson()+']}'));
});

app.get('/disconnect/:deviceName/:deviceType/:fromName', function (req, res, next) {
 var i = 0;
 var name = req.params.deviceName;
 var fromName = req.params.fromName;
 if ( req.params.deviceType == 'motor' ) {
  var motor = motorArray[parseInt(name[name.length-1])];
  var index = motor.tankLinks.indexOf(fromName);
  if (index > -1) {
   io.sockets.emit('discnct',{'name': name, 'tankName': fromName})
   io.sockets.emit('discnct',{'name': fromName, 'motorName': name})
   var tank = tankArray[parseInt(fromName[fromName.length-1])];
   var index1 = tank.motorLinks.indexOf(name);
   motor.tankLinks.splice(index,1);
   motor.changeJsonRep();
   tank.motorLinks.splice(index1,1);
   tank.changeJsonRep();
  }
 }
 else {
  var motor = motorArray[parseInt(fromName[fromName.length-1])];
  var index = motor.tankLinks.indexOf(name);
  var tank = tankArray[parseInt(name[name.length-1])];
  var index1 = tank.motorLinks.indexOf(fromName);
  if (index1 > -1) {
   io.sockets.emit('discnct',{'name': name, 'motorName': fromName})
   io.sockets.emit('discnct',{'name': fromName, 'tankName': name})
   motor.tankLinks.splice(index,1);
   motor.changeJsonRep();
   tank.motorLinks.splice(index1,1);
   tank.changeJsonRep();
  }
 }
 inDeviceArray();
 deviceArrayJson();
 //console.log(deviceArrayJson());
 res.render('changeLink',JSON.parse('{"name":"'+req.params.deviceName+'","devices":['+deviceArrayJson()+']}'));
});

app.get('/switch/:deviceName/:deviceType', function (req, res, next) {
 var name = req.params.deviceName;
 var type = req.params.deviceType;
 io.sockets.emit('switch', {'name':name});
 if (type == 'motor') {
  var motor = motorArray[parseInt(name[name.length-1])];
  if (motor.status == 'on') {
   motor.status = 'off';
  }
  else {
   motor.status = 'on';
  }
  motor.changeJsonRep();
 }
 else {
  var tank = tankArray[parseInt(name[name.length-1])];
  if (tank.status == 'on') {
   tank.status = 'off';
  }
  else {
   tank.status = 'on';
  }
  tank.changeJsonRep();
 }
 inDeviceArray();
 res.redirect('http://localhost:3000/view');
});
  

io.on('connection', function (socket) {
 console.log('A user has connected');
 socket.on('disconnect', function () {
  console.log('User has disconnected');
 });
 socket.on('message', function(message) {
  //console.log('Received:'+JSON.stringify(message));
  //console.log(message.type);
 });
 socket.on('sndWater', function(sndWater) {
  var name = sndWater.name;
  var tank = tankArray[parseInt(name[name.length-1])];
  if (tank.level < 1000) {
   io.sockets.emit('rcvWater', {'amount': sndWater.amount.toString(), 'name': sndWater.name.toString()});
   tank.level = parseInt(tank.level) + parseInt(sndWater.amount);
   console.log(sndWater.amount);
   console.log(tank.level);
   tank.changeJsonRep();
   inDeviceArray();
  }
 });
 socket.on('sendName', function(sendName) {
  //console.log('Received:'+JSON.stringify(sendName));
  if(sendName.sendName == "motor") {
   socket.emit('recName',{'name': 'motor'+motorArray.length.toString()});
   var motor = new deviceClasses.Motor('motor'+motorArray.length.toString())
   motorArray[motorArray.length] = motor;
   deviceArray[deviceArray.length] = JSON.stringify(motor.jsonRep);
   //console.log(deviceArray);
   //deviceArrayJson();
  }
  if(sendName.sendName == "tank") {
   socket.emit('recName',{'name': 'tank'+tankArray.length.toString()});
   var tank = new deviceClasses.Tank('tank'+tankArray.length.toString())
   tankArray[tankArray.length] = tank;
   deviceArray[deviceArray.length] = JSON.stringify(tank.jsonRep);
   //console.log(deviceArray);
   //console.log(deviceArrayJson());
  }
 });
});

http.listen(3001, function() {
 console.log('listening on *3000');
});

// view engine setup
app.set('views', path.join(__dirname, './app_api/views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);
app.use('/users', users);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
