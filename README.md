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
 1. Created a python process for simulating a motor.
 2. Created a python process for simulating a tank.
 3. Modified the server to handle communication among tanks and motors and serve web pages for the user interface.
 4. We assume that all motors available are connected to all the tanks available but the user has the ability to decide which of the links can be used and can make changes to these links dynamically.
 5. Created a web page listing all the tanks and motors that are currently available.
 6. For every tank and motor there are two buttons "change link" and "switch on" (if the device is off) / "switch off" (if the device is on).
 7. Every tank has a progress bar monitoring the level of water in the tank (capacity 1000).
 8. "change link" button is used to activate or deactivate links among tanks and motors.
 9. On clicking the change link button a web page appears showing 2 lists of links "connect to" and "disconnect from".
 10. "connect to" list shows the list of tanks(for the motor whose button was pressed) or motors(for the tank whose button was pressed) that can be connected to (activate the link) the motor/tank whose "change link" button was clicked.
 11. Clicking on a tank or a motor in the "connect to" list activates the link between that tank or motor to the motor or the tank whose button was clicked.
 12. "disconnect from" list shows the list of tanks(for the motor whose button was pressed) or motors(for the tank whose button was pressed) that can be disconnected from (deactivate the link) the motor/tank whose "change link" button was clicked.
 13. Clicking on a tank or a motor in the "disconnect from" list deactivates the link between that tank or motor and the motor or the tank whose "change link" button was clicked.
 14. "switch on/off" button is used to switch the device on or off.
 15. "switch" button automatically changes to "switch on" if the device is off and changes to "switch off" if the the device is on.
 16. A motor can only feed water to a tank if both the motor and tank are on and the link between the 2 is activated ad the tank is not full.
 17. Motor supplies water at the rate of 10 units / second which gets divided equally among tanks that are not full, on and connected to the motor.
 18. Once a tank gets filled to max capacity or switched off or disconnected, motor stops sending water to it and only distributes water to tanks that are on, not full and connected to it.
    
 Week 4: (Complete simulation for tank, motor and filter)
  1. Created a python process for simulating a filter.
  2. Modified the server to handle communication among tanks and motors and filters and serve web pages for the user interface.
  3. In addition to week 3, We assume that all tanks available are connected to all the filters available but the user has the ability to decide which of the links can be used and can make changes to these links dynamically.
  4. A filter can draw water from a tank only if both the filter and tank are on and the link between the 2 is activated and the filter is not full and the tank is not empty.
  5. A filter draws water at the rate of 1 unit / second.
  6. Max capacity of filter is 100 units.
  7. Once a filter is filled to max capacity or switched off or disconnected or the tank is empty the filter stops drawing water from it.