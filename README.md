# RasPi3 with Google Assistant including Home Automation using SOnOff/ESP8266  
*******************************************************************************************************************************


*******************************************************************************************************************************
### The code used as the basis for this project is derived from the original GassistPi by shivasiddharth, his code can be found at: https://github.com/shivasiddharth/GassistPi/  
### This project includes development to support more functionality relating to IoT, controlling external devices and Home Automation.  It has been simplified where possible and developed for use only with a naked Rasberry Pi3 using just a USB microphone and amplified speaker(s) plugged into the on-board audio jack.  The code may work on earlier Raspberry Pis too, but nothing is guaranteed!
 
*******************************************************************************************************************************

# Original features of GassistPi (retained in this release):  
**1.   Headless auto start on boot.**    
**2.   Direct Voice control of GPIOs without any need for IFTTT.**   
**3.   Radio station streaming.**  
**4.   Voice control of a servo connected to RPi GPIO.**  
**5.   Safe shutdown of the RPi3 using "Shut Down" voice command.**  
**6.   Indicator lights for assistant listening and speaking events.**  
**7.   Startup audio and audio feedback for wakeword detection.**   
**8.   Pushbutton service to stop Music or Radio playback.**   
**9.   Streaming music from your Google Play Music library.**     

# New Features developed for this release:
**1.   Direct Voice control of up to 10 SOnOff wireless switches or ESP8266 / NodeMCU using simple HTTP commands across your own LAN (no need for IFTTT or editing any Arduino scripts).**  


*******************************************************************************************************************************
# Important Notes: 
**This Project has adopted the new Google Assistant SDK features released on 20th Dec 2017. Old installations of the Google Assistant SDK will not work. So kindly reformat your SD Card and start again from the begining**  

**If you dont need the new features of GassistPi3 (to control external devices with voice commands) or you're using anything other than an RPi3 then please feel free to use the original code available from https://github.com/shivasiddharth/GassistPi/**

**If you have any suggestions, additions you'd like to see, or general comments / issues then please feel free to let me know.
*******************************************************************************************************************************


**************************************************
## **1. Create a new SD card image** 
**************************************************
CLI or Raspbian Lite does not support all the features required, so please use the standard Raspbian Desktop image available from https://www.raspberrypi.org/downloads/raspbian/ to create your SD card image.


*************************************************
## **2. Clone the Project on to your Pi3**   
*************************************************
Open a terminal and enter the following:  
```
git clone https://github.com/VinceW31/GassistPi3    
```
(you may need to type this in manually if copy and paste produces an error)


*************************************************  
## **3. Update to Latest Versions**
*************************************************  
Update OS and Kernel    
```
sudo apt-get update  
sudo apt-get install raspberrypi-kernel  
```
Restart your Pi3
```
sudo reboot
```


*************************************************  
## **4. Audio Configuration**
*************************************************  

Setup audio configuration.

(This step is for a simple naked RPi3 configuration using a USB Mic and amplified Speaker(s) connected to the on-board audio jack of the RPi3.   It does not support setups consisting of the AIY-HAT or any other CUSTOM-HATs.)**
 
4.1.Enter the following commands line by line (copy and paste should work fine):
```
sudo chmod +x /home/pi/GassistPi/audio-drivers/USB-MIC-JACK/scripts/usb-mic-onboard-jack.sh  
sudo /home/pi/GassistPi/audio-drivers/USB-MIC-JACK/scripts/usb-mic-onboard-jack.sh  
```

4.2. Setup the Speaker configuration.

   Right click the speaker icon on the desktop (top right) and select Analog Audio so its ticked.

   Right click the speaker icon again and select USB Device Settings

   In the new window make sure the Sound Card option at the top of the window is on bcm2835 ALSA,

   Click on the Select Controls button at the bottom of the window.

   Click on the PCM box to enable it and then select Close.

   The speaker output should now be displayed and enabled, set Vol to max.

   Select OK to close the window. 


4.3 Setup the USB Mic configuration.

   Right click the speaker icon again and select USB Device Settings once more. 

   In the new window click on the bcm2835 ALSA option and change it to the USB PnP Sound Device option.

   Click on the Select Controls button at the bottom of the window.
   
   Enable the Mic option, leave the AGC option unchecked and then select Close.

   On the Capture Tab enable the microphone and raise input Vol to Max.

   Select OK to close the window.


4.4 Audio testing.

Test speaker output by entering the following command:
```
speaker-test -t wav  
```
You should hear Front, Left, Front, Left repeatedly. Enter Ctrl C to end the test.


Test Microphone input by entering the follwing commands:

To record a 5 second voice test enter the following then speak into the Mic:
```
arecord --format=S16_LE --duration=5 --rate=16000 --file-type=raw out.wav
```
Playback your recording with:
```
aplay --format=S16_LE --rate=16000 out.wav
```
You should hear your voice recording.  Adjust Volumes to suit.


**********************************************************************  
## **5. Installing Google assistant**
**********************************************************************   

5.1 Go to Google and create your Developer Project (refer to this doc for creating credentials https://developers.google.com/assistant/sdk/develop/python/config-dev-project-and-account)  

5.2 Download your Project credentials from Google (ClientSecret.json file) and transfer it to your RasPi3 /home/pi directory **DO NOT RENAME THE FILE**  

5.3 Place the .json file in/home/pi directory **DO NOT RENAME THE FILE**  

5.3 Install Google Assistant on RasPi3 by entering the following commands into a terminal window:
```
sudo chmod +x /home/pi/GassistPi/scripts/gassist-installer-pi3.sh
sudo  /home/pi/GassistPi/scripts/gassist-installer-pi3.sh 
```
This may take a long time and may appear to hang, but leave it alone for a while and it will complete.
When prompted, enter your Google Cloud console Project-Id, a name for your Assistant and the Full Name of your credentials .json file, including the json extension.**

5. Copy the google assistant authentication link shown in the terminal window on your RasPi and authorize the Project in your Google account.

6. Copy the authorization code from your browser window into the terminal window and then press enter.   

7. After successful authentication, the Google Assistant Demo test will automatically start. At the start, the volume might be low, the assistant volume is independent of the Pi volume, so increase the volume by using the "Volume Up" voice command.

8. After verifying the working of assistant, close and exit the terminal.

9. The Google Assistant service can be stopped and started manually using:


*************************************************  
## **Google Assistent AUTOSTART on RasPi BOOT**  
*************************************************  
1. Open the service files in the /home/pi/GassistPi/systemd/ directory and add your project and model ids in the indicated places and save the file.

2. Make the service installer executable  

```
sudo chmod +x /home/pi/GassistPi/scripts/service-installer.sh
```  

3. Run the service installer  

```
sudo /home/pi/GassistPi/scripts/service-installer.sh    
```  

4. Enable the services - **Pi3 and Armv7 users, enable the "gassistpi-ok-ggogle.service" and Pi Zero, Pi A and Pi 1 B+ users, enable "gassistpi-push-button.service"**          
**To stop music playback using a pushbutton connected to GPIO 23 enable stopbutton.service**  
```
sudo systemctl enable gassistpi-ok-google.service  
sudo systemctl enable gassistpi-push-button.service
sudo systemctl enable stopbutton.service  
```  

5. Start the service - **Pi3 and Armv7 users, start the "gassistpi-ok-ggogle.service" and Pi Zero, Pi A and Pi 1 B+ users, start "gassistpi-push-button.service"**          
**To stop music playback using a pushbutton connected to GPIO 23 start stopbutton.service**   
```
sudo systemctl start gassistpi-ok-google.service  
sudo systemctl start gassistpi-push-button.service
sudo systemctl start stopbutton.service  
```  

If you need to stop and re-start the service manually then perform the following steps:


*******************************************************************
## **INDICATORS for GOOGLE ASSISTANT'S LISTENING AND SPEAKING EVENTS**  
*******************************************************************
Connect LEDs with colours of your choice to GPIO05 for Listening and GPIO06 for Speaking Events.  

*******************************************************************
## **PUSHBUTTON TO STOP MUSIC/RADIO PLAYBACK**  
*******************************************************************
Connect a pushbutton between GPIO23 and Ground. Using this pushbutton, now you can stop the music or radio playback.  

*******************************************************************
## **VOICE CONTROL of GPIOs and SERVOs connected to a GPIO**
*******************************************************************
The default GPIO and shutdown trigger word is **trigger**. It should be used for controlling the GPIOs, servo and for safe shutdown of Pi.

It has been intentionally included to prevent control actions due to false positive commands.  If you wish to change the trigger word, you can replace the '**trigger**'in the main.py and assistant.py code with your desired trigger word.

The default keyword for servo motor is **servo**. For example, the command **trigger servo 90** will rotate the servo by 90 degrees.   

If you wish to change the keyword, you can replace the 'servo' in the action.py script with your desired keyword for the motor.

*******************************************************************
## **Voice Activated Shut Down of RasPi3**
*******************************************************************

For safe shutdown of the pi, simple say: **shut down**  

*******************************************************************
## **VOICE CONTROL of SOnOff wireless switch or ESP8266 devices**
*******************************************************************
Download the ESPEasy firmware from here: https://www.letscontrolit.com/wiki/index.php/ESPEasy

Follow the tutorials below and the instructions on the site to flash your ESP/SOnOff devices with the downloaded firmware, during this process make sure you record the IP address that each of your ESP/SOnOff devices is using.

This link is a tutorial on how to flash a basic ESP8266:
https://www.letscontrolit.com/wiki/index.php/Basics:_Connecting_and_flashing_the_ESP8266

The YouTube link shows how to flash a SOnOff wireless switch with the ESPEasy firmware:
https://www.youtube.com/watch?v=fN_QKOWvG1s

If you need more detailed tutorial then you can also try this link:
https://rutg3r.com/sonoff-firmware-tutorial-to-esp-easy/

After flashing and performing the initial set-up there is no need to modify any Arduino firmware code or add any special rules as the default firmware configuration you just loaded to the ESP/SOnOFF will work fine as it is.

After flashing your ESP/SOnOff then add the new IP addresses (that you recorded above) for each of the devices in the actions.py file under the "IP Address of ESP/SOnOff" section

Add a Unique user friendly Name / Description for each of your appliances to be controlled into the main.py file (e.g. lamp, dish washer, coffee machine etc.) under the "Appliance Names" section.

Add a similar or the same Name / Description for each of the ESP/SOnOff device switches into the action.py file under the "ESP Device Name" section.

The  type of Switching action you want for each device switch must be correctly entered in the action.py file, under the "ESP Device Type" section.  You must identify the switch type for each device, the only valid options are ”Switch” (standard On/Off switch) or “Momentary” (like a Push switch).

************************************************
## **Music Streaming from Google Music**  
************************************************
The music streaming from Google Music uses [Gmusicapi](https://unofficial-google-music-api.readthedocs.io/en/latest/).

Enter your Google userid and password in the gmusic.py file in the line **"logged_in = api.login('YOUR_GMAIL_ID', 'YOUR_GMAIL_PASSWORD', Mobileclient.FROM_MAC_ADDRESS)"**. If you are using a two-step authentication or two-factor authentication, generate and use an app specific password.

### Getting app specific password:
Refer to this page on google help - https://support.google.com/accounts/answer/185833?hl=en

### What you can do:
Play all your songs in loop using the syntax: **"Hey Google, Play all the songs from Google Music"**

Play songs added to the user created playlist (does not include: most played playlist, thumsup playlist, etc) using the syntax: **"Hey Google, Play songs from the first playlist in Google Music"**
Playlists are sorted by date created, if you have multiple playlists, use a similar syntax replacing first with second, third etc. Also you need to make suitable changes in the main.py (It has been commented in the script to help)

Play songs by a particular artist using the syntax: **"Hey Google, Play songs by artist YOUR_ARTIST_NAME from Google Music"**

Play songs from particular album using the syntax: **"Hey Google, Play songs from album YOUR_ALBUM_NAME from Google Music"**

### What you cannot do at the moment: (some features may be added later):
Change tracks
Shuffle tracks
Repeat tracks

**Due to the Pi Zero's limitations, and computationally intensive nature of the Google Music streaming feature, this action has not been enabled for Pi Zero.**  

************************************************
## **Radio Station Streaming**  
************************************************
You must define your required Radio stations and their respective http links in actions.py 
Default keyword for streaming radio is **Radio** or **tune into**. 
For example, **tune into Radio 2**     

Useful links for obtaining radio streaming links:   
http://www.radiosure.com/stations/  

http://www.live-radio.net/worldwide.shtml  

http://worldradiomap.com/map/  

************************************************  
## **FOR NEOPIXEL INDICATOR**
************************************************  
1. Change the Pin numbers in the given sketch according to your board and upload it.  

2. Follow the circuit diagram given.  

************************************************  
## **LIST OF GPIOs USED**  
************************************************  
| GPIO Number (BCM) | Purpose                                        |
|-------------------|------------------------------------------------|
|    
| 05 and 06         | Google assistant listening and responding      |  
| 22                | Pushbutton trigger for gRPC API.               |  
| 12,13,24          | Voice control of devices connected to GPIO     |  
| 27                | Voice control of servo                         |  

