Week 1: (Establish connection and communication between express server (nodejs) and client python process)
 1. Created a client process in python simulating a simple device with device type (eg motor) as a property.
 2. Created an express server and connected it to mongodb.
 3. Made the client python process connect to the express server.
 4. Made the client python process send device type to the express server.
 5. Made the express server return a unique id to the client python process on receiving the device type from the client python process.
 6. Made the express server create a document for the device on mongodb.
 
Week 2: (Simulate switch on/off functionality)
 1. Modified the client python process to include a property 'status' which keeps track of whether the device is on or off.
 2. Created a web page listing all the devices currently connected to the server.
 3. Each device has a button associated with it to switch the device on/off.
 4. The device is off in the beginning.
 5. On clicking the button for a device, the device state changes from on to off and vice versa and the state change can be observed on the console running the python client process.
 
Week 3: (Complete simulation for tank and motor)
 1. 
 