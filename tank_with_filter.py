import deviceClasses

t = deviceClasses.Tank()
print t.name,t.filterLinks
while True:
    if t.status=='on':
        i=0
        count=0
        while i<len(t.filterLinks):
            if t.filterLinks[i].status=='on' and (int(t.filterLinks[i].level))<100:
                count+=1
            i+=1
        i=0
        while i<len(t.filterLinks):
            if t.filterLinks[i].status=='on' and (int(t.filterLinks[i].level))<100:
                t.socketIO.emit('sndWater', {'amount': str(10/count), 'name': str(t.filterLinks[i].name)})
                t.filterLinks[i].level+=int(10/count)
                t.filterLinks[i].filterDisDevice()
            i+=1
        t.socketIO.wait(seconds=1)
t.socketIO.wait()
