from picamera2 import Picamera2
import cv2
import time
                
camera = Picamera2()
ResX = 640
ResY = 480
# Request a high frame rate to determine the maximum achievable throughput for this camera mode
configuration = camera.create_video_configuration(main={"size": (ResX, ResY), "format": "RGB888"}, controls={"FrameRate": 1000})
camera.configure(configuration)
camera.start()

time.sleep(2)

tag_dictionary = cv2.aruco.getPredefinedDictionary( cv2.aruco.DICT_APRILTAG_36h11 ) # Identifies the family of april tag that will be detected)
detector_parameters = cv2.aruco.DetectorParameters() # Default OpenCV marker-detection parameters
detector = cv2.aruco.ArucoDetector(tag_dictionary, detector_parameters)

detected = False

#Debugging Values
frames = 0
StartTime = time.time()
while time.time() - StartTime <= 20.0: # Run benchmark for 20 seconds
    frame = camera.capture_array() 
    gray_frame = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY ) # Apply gray scaling
    corners, ids, rejected_candidates = detector.detectMarkers(gray_frame) # Call the detection
    frames = frames + 1

    if ids is not None: # So if an ID has been found
        if not detected:
            detected = True
            print('AprilTag Detected')

    elif detected:
        detected = False
        print('Stopped detecting AprilTag') 

EndTime = time.time()
print('FPS: ', frames/(EndTime-StartTime))
camera.stop()
camera.close()


# Detection-only benchmark used to measure processing throughput without live visualization overhead.
