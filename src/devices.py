#!/usr/bin/env python

#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
from actions import say
import os
import os.path
import RPi.GPIO as GPIO
import time
import re
import requests
#import subprocess
#import json
import urllib.request

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#gpio = (12,13,24)#GPIOS for 'var'. Add other GPIOs that you want

 
#IP Address of ESP/SOnOFFs
#replace xxx in the following IPs with your specific details for each ESP/SonOff

# ESP Device names
Device_1="Lamp" #95
Device_2="Dishwasher" #98
Device_3="Washing Machine"
Device_4="Car Charger"
Device_5="Tumble Dryer"
Device_6="No device registered"
Device_7="No device registered"
Device_8="No device registered"
Device_9="No device registered"
Device_10="No device registered"

Devices = [Device_1,
           Device_2,
           Device_3,
           Device_4,
           Device_5,
           Device_6,
           Device_7,
           Device_8,
           Device_9,
           Device_10]


ESP1_ip='192.168.1.95'
ESP2_ip='192.168.1.98'
ESP3_ip='192.168.1.101'
ESP4_ip='192.168.1.100'
ESP5_ip=''
ESP6_ip=''
ESP7_ip=''
ESP8_ip=''
ESP9_ip=''
ESP10_ip=''

ESPip = ['http://' + ESP1_ip,
         'http://' + ESP2_ip,
         'http://' + ESP3_ip,
         'http://' + ESP4_ip,      
         'http://' + ESP5_ip,
         'http://' + ESP6_ip,
         'http://' + ESP7_ip,
         'http://' + ESP8_ip,
         'http://' + ESP9_ip,
         'http://' + ESP10_ip,]

# ESP Device types
Switch = 0 #this is a standard On/Off type of switch
Momentary = 1 #this is a momentary contact Push type of switch
Device_1_Switch_Type = Switch
Device_2_Switch_Type = Momentary
Device_3_Switch_Type = Switch
Device_4_Switch_Type = Switch
Device_5_Switch_Type = Switch
Device_6_Switch_Type = Switch
Device_7_Switch_Type = Switch
Device_8_Switch_Type = Switch
Device_9_Switch_Type = Switch
Device_10_Switch_Type = Switch

Device_Switch_Type = [Device_1_Switch_Type,
                      Device_2_Switch_Type,
                      Device_3_Switch_Type,
                      Device_4_Switch_Type,
                      Device_5_Switch_Type,
                      Device_6_Switch_Type,
                      Device_7_Switch_Type,
                      Device_8_Switch_Type,
                      Device_9_Switch_Type,
                      Device_10_Switch_Type]

#ESP/SOnOff commands
ESP_Switch_cmd='/control?cmd=gpio,12,'
ESP_Momentary_cmd='/control?cmd=event,PulseOn'
on = '1' #turn ESP GPIO output ON
off = '0' #turn ESP GPIO output OFF

#ESP LED GPIOs
Device1_led = 4
Device2_led = 17
Device3_led = 27
Device4_led = 22
Device5_led = 23
Device6_led = 23
Device7_led = 23
Device8_led = 23
Device9_led = 23
Device10_led = 23

Device_led = [4,17,27,22,23,23,23,23,23,23]

GPIO.setup(Device1_led , GPIO.OUT)
GPIO.setup(Device2_led , GPIO.OUT)
GPIO.setup(Device3_led , GPIO.OUT)
GPIO.setup(Device4_led , GPIO.OUT)
GPIO.setup(Device5_led , GPIO.OUT)
GPIO.setup(Device6_led , GPIO.OUT)
GPIO.setup(Device7_led , GPIO.OUT)
GPIO.setup(Device8_led , GPIO.OUT)
GPIO.setup(Device9_led , GPIO.OUT)
GPIO.setup(Device10_led , GPIO.OUT)

#####  GPIO Section  ###################################################################

#for pin in gpio:
    #GPIO.setup(pin, GPIO.OUT)
    #GPIO.output(pin, 0)


############# Test Connectivity to Devices WiFi #################
        
def test_wifi(phrase):
    if 'device' in phrase or 'devices' in phrase or 'test' in phrase or 'text' in phrase or 'check' in phrase:
        say("Testing WiFi for all Devices")
        print("\n########## WiFi Test ###########")
        for device_number,device_name in enumerate(Devices):
            GPIO.output(Device_led[device_number],GPIO.LOW)
            if 'No device' not in device_name:
                
                if 'x' in ESPip[device_number] or "1" not in ESPip[device_number]:
                    print("IP address for " + str(Devices[device_number]) + " WiFi is missing or not Valid\n")
                    say("i p address for " + Devices[device_number] + " wifi is missing, or not valid")
                else:
                    print("IP address valid for " + str(Devices[device_number] + "\n"))

        for device_number,device_name in enumerate(Devices):
            GPIO.output(Device_led[device_number],GPIO.LOW)
            if 'No device' not in device_name:
                try:
                    r = requests.get(ESPip[device_number] + '/control?cmd=status,gpio,12')
                    GPIO.output(Device_led[device_number],GPIO.HIGH)
                    #print(r.status_code)
                    #print(r.text)
                    print("WiFi for " + str(device_name) + " ok\n")
                    say("wifi for " + device_name + " ok")
                except:  #no connection
                    GPIO.output(Device_led[device_number],GPIO.LOW)
                    print("No reply from " + str(device_name) + " WiFi\n")
                    say("no reply from " + device_name + " wifi")                   

        print("########## End of WiFi Test ###########")
        
############# Device Control Section ##########################
def device(Appliance_Name, Appliance_Number, phrase):
    global event
    if 'on' in phrase or 'home' in phrase:
        event=on
        status="On"
        send_ESP_command(Appliance_Name, Appliance_Number, status)
    elif 'off' in phrase:
        for Switch_Type_Number, Switch_Type_Name in enumerate(Device_Switch_Type,1):
            if Appliance_Number == Switch_Type_Number:
                if Switch_Type_Name == Momentary:        
                    say("sorry, OFF is not a valid command for this device type")
                else:
                    event=off
                    status="Off"
                    send_ESP_command(Appliance_Name, Appliance_Number, status)
    else:
        say("sorry, I didnt get that")

def send_ESP_command(Appliance_Name, Appliance_Number, status):
    for ESP_Number, ESP_String in enumerate(ESPip,1):
        if Appliance_Number == ESP_Number:
            for Switch_Type_Number, Switch_Type_Name in enumerate(Device_Switch_Type,1):
                if Appliance_Number == Switch_Type_Number:
                    if Switch_Type_Name == Momentary:
                        try:
                            r = requests.head(ESP_String + ESP_Momentary_cmd)
                            print("\nCommand string - " + ESP_String + ESP_Momentary_cmd)
                            print("\n***", Appliance_Name, "is now Switched On***\n")
                        except:
                            GPIO.output(17,GPIO.LOW)
                            say("unable to connect to device")
                    elif Switch_Type_Name == Switch:
                        try:
                            r = requests.head(ESP_String + ESP_Switch_cmd + event)
                            print("\nCommand string - " + ESP_String + ESP_Switch_cmd + event)
                            print("\n***", Appliance_Name, "is now", status,"***\n")
                        except:
                            GPIO.output(17,GPIO.LOW)
                            say("unable to connect to device")
                    else:
                        print("Switch Type for " + str(Appliance_Name) + "is not defined")
                        say("switch type for " + Appliance_Name + " is not defined")
                            
############# End of Device Control Section #################
