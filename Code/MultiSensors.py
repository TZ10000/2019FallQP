import RPi.GPIO as GPIO
import time
from threading import Thread
from multiprocessing import Process


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False) # for disable warnings in terminal

# time for sensor to settle
SENSOR_SETTLE_TIME = 0.00001

MEASURE_INTERVAL_TIME = 0.1 # time delay to measure (min 15miliseconds)                 

# max distance threshold for sensors to react (in cm)
MAX_DISTANCE_THRESHOLD = 5.0

# Speed of sound at sea level = 343 m/s or 34300 cm/s
MEASURE_REFERENCE = 17150

# list of sensors
sensors = []

# sensor1 with pin configuration
sensor1 = {'ID': 'sensor1', 'TRIG': 17, 'ECHO': 4, 'LED_PIN': 27 }
sensors.append(sensor1) # add to the list
# sensor2 with pin configuration
sensor2 = {'ID': 'sensor2', 'TRIG': 22, 'ECHO': 5, 'LED_PIN': 6 }
sensors.append(sensor2) # add to the list
# sensor3 with pin configuration
sensor3 = {'ID': 'sensor3', 'TRIG': 18, 'ECHO': 23, 'LED_PIN': 24 }
sensors.append(sensor3) # add to the list
# sensor4 with pin configuration
# sensor4 = {'ID': 'sensor4', 'TRIG': 20, 'ECHO': 16, 'LED_PIN': 21 }
#sensors.append(sensor4) # add to the list



def initPins():
    if len(sensors) > 0:
        for sensor in sensors:
            #Sensor's echo pins shoud be in
            GPIO.setup( sensor['ECHO'], GPIO.IN );

            #Sensor's trig pins should be out
            GPIO.setup( sensor['TRIG'], GPIO.OUT );

            #Sensor's out_pin
            GPIO.setup( sensor['LED_PIN'], GPIO.OUT );
            GPIO.output( sensor['LED_PIN'], GPIO.LOW ); # Turn off in the begining

# def turnOnLed(led_pin):
#     #Turn on led only if it is off for some safety mesures
#     if GPIO.input(led_pin) == GPIO.LOW:
#         GPIO.output(led_pin, GPIO.HIGH)
# 
# def turnOffLed(led_pin):
#     #Turn off led only if it is ON for some safety mesures
#     if GPIO.input(led_pin) == GPIO.HIGH:
#         GPIO.output(led_pin, GPIO.LOW)

def measure(sensor):
    print "Measurement started for " + sensor['ID'] + ", Ctrl+z to cancle the measurement";

    while True:
        GPIO.output( sensor['TRIG'], GPIO.LOW);

        time.sleep(MEASURE_INTERVAL_TIME); #DELAY

        GPIO.output(sensor['TRIG'], GPIO.HIGH);

        time.sleep(SENSOR_SETTLE_TIME);

        GPIO.output(sensor['TRIG'], GPIO.LOW);

        while GPIO.input(sensor['ECHO']) == 0:
            pulse_start = time.time();

        while GPIO.input(sensor['ECHO']) == 1:
            pulse_end = time.time();

        pulse_duration = pulse_end - pulse_start;

        distance = pulse_duration * MEASURE_REFERENCE;
        distanceRound = round(distance, 2);

        #if(distanceRound < MAX_DISTANCE_THRESHOLD):
        #    turnOnLed(sensor['LED_PIN'])
        #else:
        #    turnOffLed(sensor['LED_PIN'])

        print "Distance of sensor "+ sensor['ID'] + " : ", distanceRound, "cm";
        #return distanceRound


def main():
    initPins()

    # TODO: need change this part
    if len(sensors) > 0:
        for sensor in sensors:
            Process(target=measure, args=(sensor, )).start()

# TODO
if __name__ == '__main__':
    # set initial count
    print raw_input('please enter initial count: ');
    count = raw_input('please enter initial count: ');

    # set up initial distance
    firstDist = measure(sensor1);
    secondDist = measure(sensor2);
    thirdDist = measure(sensor3);

    while True:
        # list for trigger sequence
        triggeredListEnter = [];
        triggeredListExit = [];

        # return distance detected from each sensor
        dist1 = measure(sensor1);
        dist2 = measure(sensor2);
        dist3 = measure(sensor3);
        
        print "dist1 = " + dist1 + " dist2 = "+ dist2 + " dist3 = " + dist 3;

        # sensor1 triggered
        if dist1 < firstDist:
            (dist1 == dist3) ? triggeredListExit.append(1) : triggeredListEnter.append(1);

        if dist2 < secondDist:
            (dist2 == dist1) ? triggeredListEnter.append(2) : triggeredListExit.append(2);
            
        if dist3 < thirdDist:
            (dist3 == dist1) ? triggeredListEnter.append(3) : triggeredListExit.append(3);

        # 1->2->3 case
        if triggeredListEnter == [1, 2, 3]:
            count = count + 1;
            triggeredListEnter = [];

        # 3->2->1 case
        if triggeredListExit == [3, 2, 1]:
            count = count - 1;
            triggeredListExit = [];
