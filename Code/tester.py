from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(10)
camera.capture('image.jpg')
camera.stop_preview()
