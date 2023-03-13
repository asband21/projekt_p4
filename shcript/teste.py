
# Connect to the drone
tello = Tello()
tello.connect()

# Send the takeoff command
tello.takeoff()

# Retrieve the battery level
battery = tello.get_battery()
print("Battery level:", battery)

# Land the drone
tello.land()

# Disconnect from the drone
tello.end()
