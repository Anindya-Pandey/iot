console.log('wow');
var socket;
try {
 socket = io.connect('http://localhost:3001');
 console.log(socket);
}
catch (e) {
 console.log(e);
}
socket.on('rcvWater', function (rcvWater) {
 console.log(document.getElementById('level'+rcvWater.name.toString()));
 document.getElementById('level'+rcvWater.name.toString()).value = document.getElementById('level'+rcvWater.name.toString()).value + parseInt(rcvWater.amount);
});
socket.on('drawWater', function (drawWater) {
 console.log(document.getElementById('level'+drawWater.fromName.toString()));
 document.getElementById('level'+drawWater.fromName.toString()).value = document.getElementById('level'+drawWater.fromName.toString()).value - parseInt(drawWater.amount);
});