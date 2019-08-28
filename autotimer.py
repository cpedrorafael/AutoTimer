from __future__ import print_function
# from AppKit import NSWorkspace
import time
# from Foundation import *
from os import system
from activity import *
import json
import datetime

import pywintypes
import win32gui
import win32con

import os

project_file_path = r"D:\Development\Scripts\AutoTimer"
active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = ActivityList([])
first_time = True
os.chdir(project_file_path)


def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


try:
    activeList.initialize_me()
except Exception:
    print('No json')


def isBrowser(window):
    if window == 'Google Chrome' or window == 'Brave' or window == 'Opera':
        return True
    return False


try:
    while True:

        window_code = win32gui.GetForegroundWindow()
        window_text = win32gui.GetWindowText(window_code)

        window_text_array = window_text.split(' - ')
        new_window_name = window_text_array[-1]
        program_name = window_text_array[-1]

        if isBrowser(program_name):
            new_window_name = window_text_array[-2]

        if active_window_name != new_window_name:
            print('\nCurrent: {}\n'.format(new_window_name))
            activity_name = active_window_name

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()

                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)

                if not exists:
                    activity = Activity(
                        activity_name, isBrowserFlag, [time_entry])
                    activeList.activities.append(activity)
                with open('{}\\activities\\{}-{}-{}.json'.format(os.getcwd(), datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year), 'w') as json_file:
                    json.dump(activeList.serialize(), json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name
            isBrowserFlag = isBrowser(program_name)

        time.sleep(10)
except KeyboardInterrupt:
    with open('{}\\activities\\{}-{}-{}.json'.format(os.getcwd(), datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year), 'w') as json_file:
        json.dump(activeList.serialize(), json_file,
                  indent=4, sort_keys=True)
