from djitellopy import Tello
import cv2

width = 120
height = 240
startCounter = 0

te = Tello()
te.connect()
te.for_back_velocity = 0
te.left_right_velocity = 0
te.up_down_velocity = 0
te.yaw_velocity = 0
te.speed = 0

print(te.get_battery())

te.streamoff()
te.streamon()

while True:
    frame_read = te.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))

    if startCounter == 0:
        te.takeoff()
        te.move_left(20)
        te.rotate_clockwise(90)
        startcounter = 1

    cv2.imshow("Sut", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        te.land()
        break
