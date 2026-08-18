from picamera2 import Picamera2
import time
import cv2

ResX = 640
ResY = 480

camera = Picamera2()
configuration = camera.create_video_configuration(main={"size": (ResX, ResY), "format": "RGB888"}, controls={"FrameRate": 60})
camera.configure(configuration)
camera.start()

time.sleep(3) # Gives time to turn on...

Start = time.time()
frames = 0
letterQ = False
while not letterQ:
    frame = camera.capture_array()
    frames = frames+1
    cv2.imshow('Live Feedback', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        letterQ = True
        break
End = time.time()
print('Done, FPS: ',frames/(End-Start) )
