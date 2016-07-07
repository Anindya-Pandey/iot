from socketIO_client import SocketIO, LoggingNamespace
import json
import sys

class DeviceElement:
  def __init__(self,name,status):
    self.name = name
    self.status = status
  def disDevice(self):
    print self.name,self.status
  
class TankDeviceElement(DeviceElement):
  def __init__(self,name,status,level):
    DeviceElement.__init__(self,name,status)
    self.level = level
  def tankDisDevice(self):
    DeviceElement.disDevice(self)
    print self.level
 
class Device:
  def __init__(self,name):
    self.status = "off"
    self.socketIO = SocketIO('localhost',3001)
    self.socketIO.emit('sendName',{'sendName':name})
    self.name = ''
    self.socketIO.on('recName',self.setName)
    self.socketIO.wait(seconds=1)
  def setName(self,*recName):
    print recName
    self.name = recName[0]['name']
    print self.name

class Motor(Device):
  def __init__(self):
    self.tankLinks = []
    Device.__init__(self,'motor')
    self.socketIO.on('cnct', self.cnctTank)
    self.socketIO.on('discnct', self.discnctTank)
    self.socketIO.on('switch',self.switch)
  def switch(self,*name):
    sys.stdout.write('signal'+name[0]['name']+'\n')
    if (name[0]['name'] == self.name):
      if (self.status == 'off'):
        self.status = 'on'
      else:
        self.status = 'off'
      print self.status
    i = 0
    while (i < len(self.tankLinks)):
      sys.stdout.write(name[0]['name']+' '+self.tankLinks[i].name+'\n')
      if (name[0]['name'] == self.tankLinks[i].name):
        if (self.tankLinks[i].status == 'off'):
          self.tankLinks[i].status = 'on'
        else:
          self.tankLinks[i].status = 'off'
      i = i + 1
    i = 0
    while (i < len(self.tankLinks)):
      self.tankLinks[i].disDevice()
      i = i + 1     
  def discnctTank(self,*recTank):
    if (recTank[0]['name'] == self.name):
      i = 0
      while (i < len(self.tankLinks)):
        if (self.tankLinks[i].name == recTank[0]['tankName']):
          break
        i = i + 1
    del(self.tankLinks[i])
    i = 0
    while (i < len(self.tankLinks)):
      self.tankLinks[i].tankDisDevice()
      i = i + 1   
  def cnctTank(self,*recTank):
    if (recTank[0]['name'] == self.name):
      self.tankLinks.append(TankDeviceElement(recTank[0]['tankName'],recTank[0]['status'],recTank[0]['level']))
      i = 0
      while (i < len(self.tankLinks)):
        self.tankLinks[i].tankDisDevice()
        i = i + 1

class Tank(Device):
  def __init__(self):
    self.motorLinks = []
    self.level = 0
    Device.__init__(self,'tank')
    self.socketIO.on('cnct', self.cnctMotor)
    self.socketIO.on('discnct', self.discnctMotor)
    self.socketIO.on('switch',self.switch)
    self.socketIO.on('rcvWater',self.rcvWater)
  def rcvWater(self, *rcvWater):
    if (rcvWater[0]['name'] == self.name):
      self.level = self.level + int(rcvWater[0]['amount'])
      sys.stdout.write('\nLevel:'+str(self.level))
  def switch(self,*name):
    if (name[0]['name'] == self.name):
      if (self.status == 'off'):
        self.status = 'on'
      else:
        self.status = 'off'
      print self.status
    i = 0
    while (i < len(self.motorLinks)):
      if (name[0]['name'] == self.motorLinks[i].name):
        if (self.motorLinks[i].status == 'off'):
          self.motorLinks[i].status = 'on'
        else:
          self.motorLinks[i].status = 'off'
      i = i + 1
    i = 0
    while (i < len(self.motorLinks)):
      self.motorLinks[i].disDevice()
      i = i + 1     
  def discnctMotor(self,*recMotor):
    if (recMotor[0]['name'] == self.name):
      i = 0
      while (i < len(self.motorLinks)):
        if (self.motorLinks[i].name == recMotor[0]['motorName']):
          break
        i = i + 1
      del(self.motorLinks[i])
      i = 0
      while (i < len(self.motorLinks)):
        self.motorLinks[i].disDevice()
        i = i + 1   
  def cnctMotor(self,*recMotor):
    if (recMotor[0]['name'] == self.name):
      self.motorLinks.append(DeviceElement(recMotor[0]['motorName'],recMotor[0]['status']))
      i = 0
      while (i < len(self.motorLinks)):
        self.motorLinks[i].disDevice()
        i = i + 1

