# Author: Jared Scott
# Date: 12/10/2023
# Purpose: This script will automatically set the Reclaim Sabbath hours to 15 minutes before sunset on Friday to 15 minutes after sunset on Saturday
# Usage: Run the script and it will automatically open the Reclaim Sabbath hours page and set the hours


# Import dependencies

import requests, keyboard, pyautogui, datetime, webbrowser
from PIL import Image
from time import sleep


# Define classes

class Location(): # Object to store coordinates of a geographic location
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Time(): # Object to store a particular time of day
    def __init__(self, hour, minute, meridiem):
        self.hour = hour
        self.minute = minute
        self.meridiem = meridiem.lower()

    def __str__(self):
        #print in format hh:mmam/pm
        hh = str(self.hour) if self.hour > 9 else '0'+str(self.hour)
        mm = str(self.minute) if self.minute > 9 else '0'+str(self.minute)
        return hh+':'+mm+self.meridiem
    
    def add_time(self, minutes):
        self.minute += minutes
        if self.minute >= 60:
            self.hour += self.minute // 60
            self.minute = self.minute % 60
        if self.hour >= 12:
            self.hour = self.hour % 12
            if self.meridiem == 'am':
                self.meridiem = 'pm'
            else:
                self.meridiem = 'am'

    def subtract_time(self, minutes):
        self.minute -= minutes
        if self.minute < 0:
            self.hour -= 1
            self.minute = 60 + self.minute
        if self.hour < 0:
            self.hour = 12 + self.hour
            if self.meridiem == 'am':
                self.meridiem = 'pm'
            else:
                self.meridiem = 'am'

    def copy(self):
        return Time(self.hour, self.minute, self.meridiem)


# Define functions

this_folder = 'g:/My Drive/Personal/Reclaim/'
def locate(img, confidence=0.6): # locate an image on the screen (for use with pyautogui if visual method of locating text fields is desired in the future)
    shown = False
    while True:
        try:
            print('Looking for', img)
            # import any necessary libraries and show the image
            # if not shown:
            #     pil_img = Image.open(img)
            #     pil_img.show()
            #     shown = True
            im2 = pyautogui.screenshot(this_folder+'my_screenshot.png')
            print('Screenshot taken')
            coords = pyautogui.locateCenterOnScreen(img, confidence=confidence)
            return coords
        except: sleep(0.5)


# Define main

if __name__ == '__main__':
    # Define location
    location = Location(42.369960, -71.098460) # coordinates of my apartment in Cambridge, MA

    # Get sunset time
    r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': location.latitude, 'lng': location.longitude}).json()['results']
    sunset = Time(int(r['sunset'].split(':')[0])-5, int(r['sunset'].split(':')[1]), 'pm')

    # Open Reclaim Sabbath hours page
    url = "https://app.reclaim.ai/settings/hours?id=00eff7cd-ad47-42ec-beb9-2dc4e2d511d5"
    webbrowser.open(url, new=2)
    sleep(7)

    # Set hours

    # Define locations of Friday and Saturday hours text fields on screen (achieved through a bit of trial and error)
    fri_loc = (1800, 1300)
    sat_loc = (2000, 1400)

    # Click on Friday hours field and set to 15 minutes before sunset
    pyautogui.click(fri_loc)
    sleep(1)
    keyboard.press_and_release('ctrl+a')
    fri_time = sunset.copy()
    fri_time.subtract_time(15)
    print('Reclaim Sabbath Hours start set to:', fri_time)
    keyboard.write(str(fri_time))
    keyboard.press_and_release('enter')

    sleep(3)

    # Click on Saturday hours field and set to 15 minutes after sunset
    pyautogui.click(sat_loc)
    sleep(1)
    keyboard.press_and_release('ctrl+a')
    sat_time = sunset.copy()
    sat_time.add_time(15)
    print('Reclaim Sabbath Hours end set to:', sat_time)
    keyboard.write(str(sat_time))
    keyboard.press_and_release('enter')
