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
    
#filter device element like tank device element
class FilterDeviceElement(DeviceElement):
  def __init__(self,name,status,level):
    DeviceElement.__init__(self,name,status)
    self.level=level
  def filterDisDevice(self):
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
    self.socketIO.on('cnct', self.cnct)
    self.socketIO.on('discnct', self.discnct)
    self.socketIO.on('switch',self.switch)
    self.socketIO.on('rcvWater',self.rcvWater)
    self.socketIO.on('drawWater',self.drawWater)
    
  def drawWater(self,*drawWater):
    i = 0
    while i<len(self.tankLinks):
      if drawWater[0]['fromName']==self.tankLinks[i].name:
        print "DrawWater : TankLinks"
        self.tankLinks[i].level-=int(drawWater[0]['amount'])
        self.tankLinks[i].tankDisDevice()
      i=i+1   
  
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
    print "Switch TankLinks"
    while (i < len(self.tankLinks)):
      self.tankLinks[i].disDevice()
      i = i + 1     
  
  def discnct(self,*rec):
    if (rec[0]['name'] == self.name):
      i = 0
      while (i < len(self.tankLinks)):
        if (self.tankLinks[i].name == rec[0]['fromName']):
          break
        i = i + 1
      del(self.tankLinks[i])
      i = 0
      print "Discnct TankLinks"
      while (i < len(self.tankLinks)):
        self.tankLinks[i].tankDisDevice()
        i = i + 1   
  
  def cnct(self,*rec):
    if (rec[0]['fromName'] == self.name):
      self.tankLinks.append(TankDeviceElement(rec[0]['toName'],rec[0]['status'],rec[0]['level']))
      i = 0
      print "Cnct TankLinks"
      while (i < len(self.tankLinks)):
        self.tankLinks[i].tankDisDevice()
        i = i + 1

  def rcvWater(self, *rcvWater):
    i = 0
    print "RcvWater TankLinks"
    while i<len(self.tankLinks):
      if rcvWater[0]['name']==self.tankLinks[i].name:
        self.tankLinks[i].level+=int(rcvWater[0]['amount'])
        self.tankLinks[i].tankDisDevice()
      i=i+1

class Tank(Device):
  def __init__(self):
    self.motorLinks = []
    #filter links
    self.filterLinks=[]
    self.level = 0
    Device.__init__(self,'tank')
    self.socketIO.on('cnct', self.cnct)
    self.socketIO.on('discnct', self.discnct)
    self.socketIO.on('switch',self.switch)
    self.socketIO.on('rcvWater',self.rcvWater)
    self.socketIO.on('drawWater',self.drawWater)
    
  def drawWater(self,*drawWater):
    if drawWater[0]['fromName']==self.name:
        self.level=self.level-int(drawWater[0]['amount'])
    sys.stdout.write("DrawWater "+str(self.level)+"\n")
                                  
  def rcvWater(self, *rcvWater):
    if (rcvWater[0]['name'] == self.name):
      self.level = self.level + int(rcvWater[0]['amount'])
      sys.stdout.write('\nRcvWaterLevel:'+str(self.level))
    i=0
    while i<len(self.filterLinks):
      if rcvWater[0]['name']==self.filterLinks[i].name:
        self.filterLinks[i].level+=int(rcvWater[0]['amount'])
        sys.stdout.write('\n'+rcvWater[0]['name']+'Level:'+str(self.filterLinks[i].level))
      i=i+1
  
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
    i=0
    while i<len(self.filterLinks):
      if name[0]['name']==self.filterLinks[i].name:
        if self.filterLinks[i].status=='on':
          self.filterLinks[i].status='off'
        else:
          self.filterLinks[i].status='on'
      i=i+1
    i=0
    print "*filter links are displayed below"
    while i<len(self.filterLinks):
      self.filterLinks[i].filterDisDevice()
      i=i+1
  
  def discnct(self,*rec):
    if (rec[0]['name'] == self.name):
      if rec[0]['fromType']=='motor':
        i = 0
        while (i < len(self.motorLinks)):
          if (self.motorLinks[i].name == rec[0]['fromName']):
            break
          i = i + 1
        del(self.motorLinks[i])
        i = 0
        while (i < len(self.motorLinks)):
          self.motorLinks[i].disDevice()
          i = i + 1
      elif rec[0]['fromType']=='filter':
        i=0
        while i<len(self.filterLinks):
          if self.filterLinks[i].name==rec[0]['fromName']:
            break
          i=i+1
        del(self.filterLinks[i])
        i=0
        while i<len(filterLinks):
          self.filterLinks[i].filterDisDevice()
          i=i+1
          
  def cnct(self,*rec):
    if (rec[0]['fromName'] == self.name):
      if rec[0]['toType']=='motor':
        self.motorLinks.append(DeviceElement(rec[0]['toName'],rec[0]['status']))#here 'motorName' needs to be change to deviceName
        i = 0
        while (i < len(self.motorLinks)):
          self.motorLinks[i].disDevice()
          i = i + 1
      elif rec[0]['toType']=='filter':
        self.filterLinks.append(FilterDeviceElement(rec[0]['toName'],rec[0]['status'],rec[0]['level']))
        i = 0
        while (i < len(self.filterLinks)):
          self.filterLinks[i].filterDisDevice()
          i = i + 1
        
class Filter(Device):
  def __init__(self):
    self.tankLinks=[]
    self.level=0
    Device.__init__(self,'filter')
    self.socketIO.on('cnct',self.cnct)
    self.socketIO.on('discnct',self.discnct)
    self.socketIO.on('switch',self.switch)
    self.socketIO.on('rcvWater',self.rcvWater)
    self.socketIO.on('drawWater',self.drawWater)
  
  def cnct(self,*rec):
    if (rec[0]['fromName']==self.name):
      self.tankLinks.append(TankDeviceElement(rec[0]['toName'],rec[0]['status'],rec[0]['level']))
      i=0
      while (i<len(self.tankLinks)):
        self.tankLinks[i].tankDisDevice()
        i=i+1

  def discnct(self,*rec):
    if (rec[0]['name']==self.name):
      i=0
      while(i<len(self.tankLinks)):
        if (self.tankLinks[i].name==rec[0]['fromName']):
          break
        i=i+1
      del(self.tankLinks[i])
      i=0
      while (i<len(self.tankLinks)):
        self.tankLinks[i].tankDisDevice()
        i=i+1
  
  def switch(self,*name):
    sys.stdout.write('signal'+name[0]['name']+'\n')
    if name[0]['name']==self.name:
      if self.status=='off':
        self.status='on'
      else:
        self.status='off'
      print self.status
    i=0
    while i<len(self.tankLinks):
      sys.stdout.write(name[0]['name']+' '+self.tankLinks[i].name+'\n')
      if name[0]['name']==self.tankLinks[i].name:
        if self.tankLinks[i].status=='off':
          self.tankLinks[i].status='on'
        else:
          self.tankLinks[i].status='off'
      i=i+1
    i=0
    while i<len(self.tankLinks):
      self.tankLinks[i].disDevice()
      i=i+1
  
  def rcvWater(self,*rcvWater):
    if rcvWater[0]['name']==self.name:
      self.level=self.level+int(rcvWater[0]['amount'])
      sys.stdout.write('\nLevel:'+str(self.level))
    i=0
    while i<len(self.tankLinks):
      if rcvWater[0]['name']==self.tankLinks[i].name:
        self.tankLinks[i].level+=int(rcvWater[0]['amount'])
        sys.stdout.write(rcvWater[0]['name']+'\ Level:'+str(self.tankLinks[i].level))
      i=i+1

      
  def drawWater(self,*drawWater):
    i=0
    while i<len(self.tankLinks):
      if drawWater[0]['fromName']==self.tankLinks[i].name:
        self.tankLinks[i].level-=int(drawWater[0]['amount'])
        sys.stdout.write(drawWater[0]['fromName']+'\ Level:'+str(self.tankLinks[i].level))
      i=i+1
