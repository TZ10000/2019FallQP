import RPi.GPIO as GPIO
import time
import sys
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
sensor1 = {'ID': 'sensor1', 'TRIG': 23, 'ECHO': 24}
sensors.append(sensor1) # add to the list
# sensor2 with pin configuration
sensor2 = {'ID': 'sensor2', 'TRIG': 22, 'ECHO': 10}
sensors.append(sensor2) # add to the list
# sensor3 with pin configuration
sensor3 = {'ID': 'sensor3', 'TRIG': 25, 'ECHO': 8}
sensors.append(sensor3) # add to the list
# sensor4 with pin configuration
# sensor4 = {'ID': 'sensor4', 'TRIG': 20, 'ECHO': 16, 'LED_PIN': 21 }
#sensors.append(sensor4) # add to the list



def initPins():
    print('initial pin')
    if len(sensors) > 0:
        for sensor in sensors:
            #Sensor's echo pins shoud be in
            GPIO.setup( sensor['ECHO'], GPIO.IN );

            #Sensor's trig pins should be out
            GPIO.setup( sensor['TRIG'], GPIO.OUT );

            #Sensor's out_pin
            #GPIO.setup( sensor['LED_PIN'], GPIO.OUT );
            #GPIO.output( sensor['LED_PIN'], GPIO.LOW ); # Turn off in the begining

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
    #print ("Measurement started for " + sensor['ID'] + ", Ctrl+z to cancle the measurement");

    #while True:
    #GPIO.output( sensor['TRIG'], GPIO.LOW);

    #time.sleep(MEASURE_INTERVAL_TIME); #DELAY
    #print('2')
    GPIO.output(sensor['TRIG'], GPIO.HIGH);

    time.sleep(SENSOR_SETTLE_TIME);

    GPIO.output(sensor['TRIG'], GPIO.LOW);
    
    # manually set starttime
    pulse_start = time.time()
    pulse_end = time.time()
    
    #print('get there1')

    while GPIO.input(sensor['ECHO']) == 0:
        #print('get there2')
        pulse_start = time.time();

    while GPIO.input(sensor['ECHO']) == 1:
        #print('get there3')
        pulse_end = time.time();

    pulse_duration = pulse_end - pulse_start;
    #print('get there4')

    distance = pulse_duration * MEASURE_REFERENCE;
    distanceRound = round(distance, 2);

        #if(distanceRound < MAX_DISTANCE_THRESHOLD):
        #    turnOnLed(sensor['LED_PIN'])
        #else:
        #    turnOffLed(sensor['LED_PIN'])

    print ("Distance of sensor "+ sensor['ID'] + " : ", distanceRound, "cm");
    return distanceRound


def main():
    initPins()

    # TODO: need change this part
    #if len(sensors) > 0:
     #   for sensor in sensors:
     #      Process(target=measure, args=(sensor, )).start()
    #print('1')
    for sensor in sensors:
        print(measure(sensor))

# TODO

if __name__ == '__main__':
    main()

    # set initial count
    cnt = input('please enter initial count: ');
    count = int(cnt)
    #count = raw_input('please enter initial count: ');

    # set up initial distance
    firstDist = measure(sensor1);
    secondDist = measure(sensor2);
    thirdDist = measure(sensor3);
    
    testLog = open('./testLog.txt', 'w')
    
    # list for trigger sequence
    triggeredList = [0, 0, 0];
    triggeredListEnter = [0, 0, 0];
    triggeredListExit = [0, 0, 0];

    while count < 15:
        print ('current count: ' + str(count))
        testLog.write('current count: ' + str(count) + '\n')
        
        print(triggeredList)

        # return distance detected from each sensor
        dist1 = measure(sensor1);
        dist2 = measure(sensor2);
        dist3 = measure(sensor3);
        
        print ("dist1 = " + str(dist1) + " dist2 = "+ str(dist2) + " dist3 = " + str(dist3));
        testLog.write("dist1 = " + str(dist1) + " dist2 = "+ str(dist2) + " dist3 = " + str(dist3) + '\n')

        # sensor1 triggered
        if dist1 < firstDist:
            triggeredList[0] = 1;

        if dist2 < firstDist:
            triggeredList[1] = 2;
            
        if dist3 < firstDist:
            triggeredList[2] = 3;

        # 1->2->3 case
        if triggeredList == [1, 2, 3]:
            count = count + 1;
            triggeredList = [0, 0, 0];

        # 3->2->1 case
        if triggeredList == [3, 2, 1]:
            #count = count - 1;
            triggeredList = [0, 0, 0];
            
        
        time.sleep(1)
    GPIO.cleanup()
    testLog.close()
