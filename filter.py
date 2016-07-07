import deviceClasses

f=deviceClasses.Filter()
print '*',f.name
#seems stuck here and not printing anythin cos nothing is set in app.js to
#return the name for a filter class or filterLink.  just a guess!!
f.socketIO.wait()
