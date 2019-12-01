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
    #print ("Measurement started for " + sensor['ID'] + ", Ctrl+z to cancel the measurement");

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
        #print('xian diao le')
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

#inclusive check if the distances is really changed
def rangeEqual(dis1, dis2, range0):
    if (abs(dis1 - dis2) >= range0):
        return True
    return False

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
    initDist = measure(sensor1);
    # seperate the door into several intervals
    # handle the situation that people going in and out at the same time
    interval =  (initDist / 5);
    print ("interval is " + str(interval))
    
    print(initDist);
    
    testLog = open('./testLog.txt', 'w')
    
    # list for trigger sequence
    triggeredList = [[], [], [], [], []];
    
    # width of person, subject to change
    objectWidth = 5;
    objectGap = 1;

    # TODO: change to an infinite loop
    while count < 15:
        print ('current count: ' + str(count))
        testLog.write('current count: ' + str(count) + '\n')
        
        print(triggeredList);


        # return distance detected from each sensor
        dist1 = measure(sensor1);
        dist2 = measure(sensor2);
        dist3 = measure(sensor3);
        
        # set the distances to be initDist if distances is larger than the initDist
        if dist1 > initDist:
            dist1 = initDist;
        if dist2 > initDist:
            dist2 = initDist;
        if dist3 > initDist:
            dist3 = initDist;
        
        # find the slot of the person
        dist1slot = int((dist1 - 1) / interval);
        #print(dist1slot);
        dist2slot = int((initDist - dist2 - objectWidth) / interval);
        #print(dist2slot);
        dist3slot = int((dist3 - 1) / interval);
        print("dist1slot: " +str(dist1slot) + " dist2slot: " + str(dist3slot) + " dist3slot: " + str(dist3slot));
        
        print ("dist1 = " + str(dist1) + " dist2 = "+ str(dist2) + " dist3 = " + str(dist3));
        testLog.write("dist1 = " + str(dist1) + " dist2 = "+ str(dist2) + " dist3 = " + str(dist3) + '\n')

         # sensor1 triggered
        if rangeEqual(dist1, initDist, 3):
            triggeredList[dist1slot].append(1);
        # sensor2 triggered
        if rangeEqual(dist2, initDist, 3):
            #first check if there alredy number in the slot
            if len(triggeredList[dist2slot]) != 0:
                triggeredList[dist2slot].append(2);
            #else we assume if there are two object and check the corresponding position
            else:
                originalSlot = int((initDist - dist2 - 2 * objectWidth - objectGap) / interval);
                if len(triggeredList[originalSlot]) != 0:
                    triggeredList[originalSlot].append(2);
                    count = count + 1;
        # sensor3 triggered
        if rangeEqual(dist3, initDist, 3):
            triggeredList[dist3slot].append(3);
                
        # delete the duplicate trigger
        # used when a person walks too slow or stands in a certain place
        for i in range(len(triggeredList)):
            j = 0;
            while j < (len(triggeredList[i]) - 1):
                print ("j: " + str(j));
                if triggeredList[i][j] == triggeredList[i][j + 1]:
                    del triggeredList[i][j];
                    j = j-1;
                j=j+1;
                    
        # count people
        for i in range(len(triggeredList)):
            #print ('i is' + str(i))
            if (triggeredList[i] == [1, 2, 3]) or (triggeredList[i] == [3, 1, 2]):
                count = count + 1;
                triggeredList[i] = [];
            if (triggeredList[i] == [3, 2, 1]) or (triggeredList[i] == [1, 3, 2]):
                count = count - 1;
                triggeredList[i] = [];
            if len(triggeredList[i]) >= 3:
                triggeredList[i] = [];
            '''
            #elif len(triggeredList[i]) != 0:
                if triggeredList[i][0] == 2:
                    triggeredList[i] = [];
                if len(triggeredList[i]) > 1:
                    if (triggeredList[i][0] == 1 and triggeredList[i][1] == 3)\
                       or (triggeredList[i][0] == 3 and triggeredList[i][1] == 1):
                        triggeredList[i] = [];
        '''
        time.sleep(1)
        
    GPIO.cleanup()
    testLog.close()
