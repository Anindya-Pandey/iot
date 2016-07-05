"use strict"
class Device {
 constructor(name) {
  this.name = name;
  this.status = "off";
 }
}

class Motor extends Device {
 constructor(name) {
  super(name);
  this.type = 'motor';
  console.log(this.name);
  this.tankLinks = [];
  this.jsonRep = JSON.parse('{"name":"'+this.name+'","status":"'+this.status+'","type":"'+this.type+'","tankLinks":['+this.getTankLinks()+']}');
  console.log(this.jsonRep);
 }
 changeJsonRep() {
  this.jsonRep = JSON.parse('{"name":"'+this.name+'","status":"'+this.status+'","type":"'+this.type+'","tankLinks":['+this.getTankLinks()+']}');
 }
 getTankLinks() {
  var tankLinkString = '';
  var i = 0;
  while (i<this.tankLinks.length) {
   if (i==0) {
    tankLinkString = tankLinkString + '"'+this.tankLinks[i]+'"';
   }
   else {
    tankLinkString = tankLinkString + ',"' + this.tankLinks[i]+'"';
   }
   i=i+1;
  }
  return tankLinkString;
 }
}

class Tank extends Device {
 constructor(name) {
  super(name);
  this.level = 0;
  this.type = 'tank';
  console.log(this.name);
  this.motorLinks = [];
  this.jsonRep = JSON.parse('{"name":"'+this.name+'","level":"'+this.level+'","status":"'+this.status+'","type":"'+this.type+'","motorLinks":['+this.getMotorLinks()+']}');
  console.log(this.jsonRep);
 }
 changeJsonRep() {
  this.jsonRep = JSON.parse('{"name":"'+this.name+'","level":"'+this.level+'","status":"'+this.status+'","type":"'+this.type+'","motorLinks":['+this.getMotorLinks()+']}');
 }

 getMotorLinks() {
  var motorLinkString = '';
  var i = 0;
  while (i<this.motorLinks.length) {
   if (i==0) {
    motorLinkString = motorLinkString + '"'+this.motorLinks[i]+'"';
   }
   else {
    motorLinkString = motorLinkString + ',"' + this.motorLinks[i]+'"';
   }
   i=i+1;
  }
  return motorLinkString;
 }
}

module.exports.Motor = Motor;
module.exports.Tank = Tank;