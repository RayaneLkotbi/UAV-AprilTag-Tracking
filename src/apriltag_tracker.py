from picamera2 import Picamera2
import cv2
import time

# Note that this code is used for debugging and live feedback purposes

def countdown():
     print('Detection starts in 5 seconds...')
     for i in range(5,0,-1):
          print('Seconds left: ', i)
          time.sleep(1)
                   
camera = Picamera2()
ResX = 640
ResY = 480
CenterX = ResX/2
CenterY = ResY/2
# intentionally overshooting to force max fps for this mode when I put 1000.
configuration = camera.create_video_configuration(main={"size": (ResX, ResY), "format": "RGB888"}, controls={"FrameRate": 1000})
camera.configure(configuration)
camera.start()

time.sleep(2)

tag_dictionary = cv2.aruco.getPredefinedDictionary( cv2.aruco.DICT_APRILTAG_36h11 ) # Identifies the family of april tag that will be detected)
detector_parameters = cv2.aruco.DetectorParameters() # Default AprilTag detection parameters
detector = cv2.aruco.ArucoDetector(tag_dictionary, detector_parameters)
detected = False

#Debugging Values
SumLoop = 0
SumDelta = 0
frames = 0
detectedFrames = 0
StartTime = time.time()
PreviousTime = 0 # Controls terminal output rate for alignment error
countdown()

startTime = time.time()
while time.time() - startTime <= 20.0:
    #Resets each picture
    tag_x = 0 
    tag_y = 0

    t0 = time.perf_counter() # Delta for Detection time rate
    frame = camera.capture_array() 
    gray_frame = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY ) # Apply gray scaling
    corners, ids, rejected_candidates = detector.detectMarkers(gray_frame) # Call the detection
    t1 = time.perf_counter()
    SumDelta = SumDelta + (t1-t0)
    frames = frames + 1 # Counts frames total

    if ids is not None: # So if an ID has been found
        detectedFrames = detectedFrames + 1

        tag_corners = corners[0][0] #First tag detected, 4 corners, 2 Axis.
        for j in range(0,2,1):
             for i in range(0,4,1):
                 if j == 0:
                    tag_x = tag_x + tag_corners[i][j]
                 else:
                    tag_y = tag_y + tag_corners[i][j]
        tag_x = tag_x/4 # Changed for better readability
        tag_y = tag_y/4
        error_x = -(CenterX - tag_x)
        error_y = CenterY - tag_y
        CurrentTime = time.time()
        if CurrentTime - PreviousTime >= 0.5:
            print('Error X: ', error_x, ' | Error Y: ', error_y) # X axis
            PreviousTime = CurrentTime
                  
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)  # draw boxes + IDs on the frame
        if not detected:
            detected = True
            print('AprilTag Detected')

    elif detected:
        detected = False
        print('Stopped detecting AprilTag') 

    cv2.imshow('AprilTag Feed', frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit early
            break # break
    t2 = time.perf_counter()
    SumLoop = SumLoop + (t2-t0)

# End of while loop
EndTime = time.time()
ElapsedTime = EndTime - StartTime

print('Result of this test: ')
print('-----------------------')
print('Average Frames per second: ', frames/ElapsedTime)
print('Resolution used: ', ResX, ', ', ResY)
print('Detection Percentage: ', detectedFrames*100/frames)
print('Average Time Per Frame detection: ', SumDelta/frames)
print('Average Time per Loop: ', SumLoop/frames)
# frames essentially represent the amount of loops done

camera.stop()
camera.close()




