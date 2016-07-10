import deviceClasses

m = deviceClasses.Motor()
print m.name
while True:
  if (m.status == 'on'):
    i=0
    count = 0
    while (i < len(m.tankLinks)):
      if (m.tankLinks[i].status == 'on' and (int(m.tankLinks[i].level) < 1000)):
        count = count + 1
      i = i + 1
    i=0
    while (i < len(m.tankLinks)):
      if (m.tankLinks[i].status == 'on' and (int(m.tankLinks[i].level) < 1000)):
        m.socketIO.emit('sndWater', {'amount': str(10/count), 'name': str(m.tankLinks[i].name)})
      i = i + 1
  m.socketIO.wait(seconds=1)
m.socketIO.wait()
