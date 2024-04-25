# Author: Drake Pearson (Drakerp2)
# Version: 0.0.0
# Release: 4/24/2024
# Git: https://github.com/drakerp2/Vtuber-Analytics-w-Holodex
# License: https://github.com/drakerp2/Vtuber-Analytics-w-Holodex/blob/main/LICENSE
# Credits: 
#        Holodex License: https://docs.holodex.net/#section/LICENSE
#        Holodex Homepage: https://holodex.net/
#        Oshi: Runie Ruse (Phase Connect) https://www.youtube.com/@RunieRuse
#
# pip requirements:
#        requests
#
#! Pulls a list of every active YT stream from Holodex and appends the data to files in .\streams 
#! Returns a list of streams in .\streams that are finished
#




import threading
from datetime import datetime
from datetime import timedelta
import os
import sys

import requests


#import json #used in debugging


# initializes the stream parsers, threading each stream parse seperately
def parse_streams(current_time, duration_throwaway, header, debug_file=sys.stdout):
    global streams
    streams = os.listdir("./streams")
    global streams_lock
    streams_lock = threading.Lock()
    
    global debug_lock 
    debug_lock = threading.Lock()
    
    global valid_streams
    
    params = {
        "include": "live_info",
        "status": "live",
        "limit": 50,
        "offset": 0,
    }

    threadList = []

    for i in range(20): # debug limit ensureing loop does not continue forever if garbage data fails to get filtered (like that from many non-YT streams)
        
        params["offset"] += 50
        r = requests.get("https://holodex.net/api/v2/videos", params, headers=header)
#        json.dump(r.json(), debug_file, indent=4, ensure_ascii=False)
        
        valid_streams = False
        for stream in r.json():
            thread = threading.Thread(target=append_to_stream, args=(stream, current_time, duration_throwaway, debug_file))
            threadList.append(thread)
            thread.start()
        if (valid_streams == False): # prevents loop from running forever (or until the debug limit)
            break

    for thread in threadList:
        thread.join()
    
    print("returning", streams, file = debug_file)
    return streams


# driver function for the thread
# performs all computations before writing to any files
def append_to_stream(stream, current_time, duration_throwaway, debug_file):
#  with debug_lock: # this will force each thread to be handled one at a time for debugging
#    print(stream, file=debug_file)
   
    if (stream.get("credits") != None): #ignores streams not on youtube
#        print("tossed for credits",file=debug_file)
        return
    if (int(stream.get("live_viewers")) == 0): #ignores bad data (cannceled/late streams and such)
#        print("tossed for views",file=debug_file)
        return
    

#    json.dump(stream, debug_file, indent=4, ensure_ascii=False)

    start_actual = stream.get("start_actual")
    if (start_actual == None): start_actual = stream.get("start_scheduled") # Occurs when stream starts exactly when scheduled
    start_actual = datetime.fromisoformat(start_actual).replace(tzinfo=None)
    
    duration = current_time - start_actual
#    print(current_time, start_actual, duration, file=debug_file)

    #tosses streams that have been going for less than 15 minutes, this is to increase accuracy of live viewer counts by ensuring time for people to actually join
    #also checks for the stream in the dir in case the throwaway duration has been changed
    if (duration.total_seconds() < duration_throwaway*60 and streams.count(stream["id"]) == 0):
#        print("tossed for dur",file=debug_file)
        return
    
    global valid_streams
    valid_streams = True
    
    #opens the file associated with the stream or creates a new one
    outFile = open("./streams/%s" % stream["id"], 'a', encoding="utf-8") 
    
    try:
        with streams_lock: # thread safety
            streams.remove(stream["id"])
    except: #runs for new streams
        print(stream.get("channel").get("id"), file=outFile)  
        with debug_lock:
            print("creating", stream["id"], file=debug_file)
    
    print(stream.get("live_viewers"), current_time.isoformat(), sep='?', file=outFile)
    outFile.close()

    

