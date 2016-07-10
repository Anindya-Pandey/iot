import deviceClasses

t = deviceClasses.Tank()
print t.name
while True:
  if (t.status == 'on'):
    i=0
    while (i < len(t.filterLinks)):
      if (t.filterLinks[i].status == 'on' and (int(t.filterLinks[i].level) < 100)):
        t.socketIO.emit('sndWaterFilter', {'amount': str(1), 'name': str(t.filterLinks[i].name), 'fromName': str(t.name)})
      i = i + 1
  t.socketIO.wait(seconds=1)
t.socketIO.wait()
