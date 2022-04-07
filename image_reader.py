from picamera import PiCamera
 # NOTE: following code is for camera module that is not implemented yet
# Set up camera module
camera = PiCamera()
# TODO: Figure out what resolution works well
camera.resolution = (1024, 768)
camera.start_preview()

# NOTE: CV not implemented yet
img = camera.capture('image.jpg')
#see if any signs are detected in image
# if detect_signs():
#    print("Signs Detected")
# else:
#   print("Signs not detected")        