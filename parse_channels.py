# Author: Drake Pearson (Drakerp2)
# Version: 1.0.0
# Release: 10/24/2024
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
#! Parses through a list of Youtube stream IDs, looking for their data in .\streams
#! This data is then written too a file in .\channels named for the english name of the streamer (creating a new one as needed)
#! It pulls the current analytics of the streamer from Holodex, and creates a new stream entry
#
# todo: group data is coming in with 2 random(ish) characters on the front, this may be coming in from holodex, needs to be investigated
#

import threading
from multiprocessing.pool import ThreadPool
import json
from datetime import datetime
import os
import sys

import requests




# initializes the channel parsers, threading each channel parse seperately
def parse_channels(streams, current_time, header, debug_file=sys.stdout):
    if (len(streams) == 0): return
    global debug_lock 
    debug_lock = threading.Lock()

    thread_list = []

    global lock_dict 
    lock_dict = {}


#    thread = threading.Thread(target = append_to_channel, args=(streams[0], current_time, header, debug_file))
#    thread_list.append(thread)
#    thread.start()
        
    for filename in streams:
        thread = threading.Thread(target = append_to_channel, args=(filename, current_time, header, debug_file))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()



# driver function for the thread, 
# delegates the tasks of processing the analytic data and time data respectively using the multiprocessing library
# performs all computations before writing to any files
def append_to_channel(filename, current_time, header, debug_file):
    channelID = None
    snapshots = None
    with open("./streams/%s" % filename, 'r', encoding="utf-8") as inFile:
        channelID = inFile.readline().rstrip('\n') # YT channel ID
        snapshots = [line.rstrip('\n').split('?') for line in inFile.readlines() if len(line) > 1] # {Live viewer count}?{timestamp}
    
    if (len(channelID) < 2 or len(snapshots) == 0): # error catch
        return
    
    with debug_lock: print("pulling channel %s" % channelID, file=debug_file)

    pull = None
    try: 
        pull = requests.get("https://holodex.net/api/v2/channels/%s" % channelID, headers = header).json()
    except: 
        with debug_lock: print("!!! FAILED TO CONNECT TO HOLODEX !!!", file=debug_file)
        return
    
#    print(json.dumps(pull, indent=4, ensure_ascii=False))
   
    if(pull["english_name"] == None or pull["english_name"] == ""):
        pull["english_name"] = pull["name"]
    
#    with debug_lock: print("appending %s" % pull["english_name"], file=debug_file)

    # replaces invalid windows file characters with lookalikes
    pull["english_name"] = pull["english_name"].replace('/', '⧸')
    pull["english_name"] = pull["english_name"].replace('\u005c', '⧹')
    pull["english_name"] = pull["english_name"].replace(':', '׃')
    pull["english_name"] = pull["english_name"].replace('*', '٭')
    pull["english_name"] = pull["english_name"].replace('"', "''")
    pull["english_name"] = pull["english_name"].replace('|', '｜')
    pull["english_name"] = pull["english_name"].replace('<', '˂')
    pull["english_name"] = pull["english_name"].replace('>', '˃')
    pull["english_name"] = pull["english_name"].replace('?', '？')

    if lock_dict.get(pull["english_name"]) == None: # uses a dict to keep track of thread locks for each channel, preventing errors from attempting to read a channel already being written/read
        lock_dict[pull["english_name"]] = threading.Lock()
    
    print("Opening", pull["english_name"], file=debug_file)

    info = ThreadPool(processes=1)
    with lock_dict[pull["english_name"]]:
        outFile = open("./channels/%s" % pull["english_name"], 'a+', encoding="utf-8")
        outFile.seek(0)
        if (outFile.read(1) == '{'):
            outFile.seek(0)
            info = info.apply_async(load_json, (outFile,))
        else:
            print("Initializing", pull["english_name"])
            info = info.apply_async(initialize_channel, (pull,))
            
        with debug_lock: print("pulling stream", filename, file=debug_file)
        
        try: 
            stream = requests.get("https://holodex.net/api/v2/videos/%s" % filename, headers = header).json()
            if stream.get("message") == ("Video id %s not found" % filename):
                print(filename, "deleted by", pull["english_name"])
                os.remove("./streams/%s" % filename)
                return
        except: 
            with debug_lock: print("!!! FAILED TO CONNECT TO HOLODEX !!!", file=debug_file)
            return
        
        time_data = ThreadPool(processes=1)
        time_data = time_data.apply_async(get_time_data, (stream, current_time, debug_file,))
        
    #    with debug_lock:
    #        print(json.dumps(pull, indent=4, ensure_ascii=False), file=debug_file)
    #        print(json.dumps(stream, indent=4, ensure_ascii=False), file=debug_file)

        # performs basic checks to make sure Holodex API did not send any bad data
        if (pull["subscriber_count"] == None): pull["subscriber_count"] = 0
        if (pull["view_count"] == None): pull["view_count"] = 0
        if (pull["video_count"] == None): pull["video_count"] = 0
        
        info = calculate_analytics(info, snapshots, pull, debug_file)
        time_data = time_data.get()
        
        stream_data = {
            "Title": stream["title"],
            "Topics": stream.get("topic_id"),
            "Start": time_data["start"],
            "Duration": time_data["duration"],
            "End": time_data["end"],
            "Tardiness": time_data["tardiness"],
            "Prior Notice": time_data["notice"],
            "Live Viewership": {
                "Average": info["sys_append"]["stream_avg_views"],
                "Peak": info["sys_append"]["stream_peak_views"],
                "Date of Peak": info["sys_append"]["date_of_peak"],
            },
            "Live Viewers/Subscribers Ratio": {
                "Average": info["sys_append"]["stream_avg_sub_view_ratio"],
                "Peak": info["sys_append"]["stream_peak_sub_view_ratio"],
            },
            "Subscribers": {
                "Current": info["Subscribers"],
                "Gained": info["sys_append"]["delta_subs"],
            },
            "Views": {
                "Current": info["Total Views"],
                "Gained": info["sys_append"]["delta_views"],
            },
            "Videos": {
                "Current": info["Videos"],
                "Gained": info["sys_append"]["delta_videos"],
            }
        }
        del info["sys_append"]
        info["Streams"].append(stream_data)
        with open("./channels/%s" % pull["english_name"], 'w', encoding="utf-8") as outFile:  
            print("Performing physical write on", pull["english_name"], file=debug_file)
            json.dump(info, outFile, indent=4, ensure_ascii=False)
        os.remove("./streams/%s" % filename)



def load_json(outFile):
    ret = None
    try:
        ret = json.load(outFile)
    except json.JSONDecodeError:
        pos = outFile.tell()
        outFile.seek(pos-1)
        
        print("!!!!!!" + str(pos) + " !!! " + str(outFile.read(5)) + " !!!!!!")
    return ret



# processes the analytics of the channel provided by Holodex channels API
def calculate_analytics(info, snapshots, pull, debug_file):
    sys_append = {
        "stream_avg_views": 0,
        "stream_peak_views": 0,
        "date_of_peak": None,
        "stream_avg_sub_view_ratio": 0,
        "stream_peak_sub_view_ratio": 0,
        "delta_subs": 0,
        "delta_videos": 0,
        "delta_views": 0,
    }
    
    for snapshot in snapshots:
        if (len(snapshot) == 1): continue #avoids crashes due to double writes (can happen given other errors)
        viewers = int(snapshot[0])
        sys_append["stream_avg_views"] += viewers
        if (sys_append["stream_peak_views"] < viewers):
            sys_append["stream_peak_views"] = viewers
            sys_append["date_of_peak"] = snapshot[1]
    sys_append["stream_avg_views"] = float(sys_append["stream_avg_views"])/float(len(snapshots))
    
    # utilizes divide by 0 error to ignore streams with no subscriber_count present
    try: sys_append["stream_avg_sub_view_ratio"] = sys_append["stream_avg_views"]/int(pull["subscriber_count"])
    except: None
    try: sys_append["stream_peak_sub_view_ratio"] = float(sys_append["stream_peak_views"])/int(pull["subscriber_count"])
    except: None
    
    info = info.get()
    stream_count = len(info["Streams"])
    
    info["Live Viewership"]["Stream Average"] = int(add_to_average(stream_count, info["Live Viewership"]["Stream Average"], sys_append["stream_avg_views"]))
    info["Live Viewership"]["Average Peak"] = int(add_to_average(stream_count, info["Live Viewership"]["Average Peak"], sys_append["stream_peak_views"]))

    if (sys_append["stream_peak_views"] > info["Live Viewership"]["All Time Peak"]): 
        info["Live Viewership"]["All Time Peak"] = sys_append["stream_peak_views"]
        info["Live Viewership"]["Date of Peak"] = sys_append["date_of_peak"]
    
    info["Live Viewers/Subscribers Ratio"]["Stream Average"] = add_to_average(stream_count, info["Live Viewers/Subscribers Ratio"]["Stream Average"], sys_append["stream_avg_sub_view_ratio"])
    info["Live Viewers/Subscribers Ratio"]["Average Peak"] = add_to_average(stream_count, info["Live Viewers/Subscribers Ratio"]["Average Peak"], sys_append["stream_peak_sub_view_ratio"])

    if (sys_append["stream_peak_sub_view_ratio"] > info["Live Viewers/Subscribers Ratio"]["All Time Peak"]):
        info["Live Viewers/Subscribers Ratio"]["All Time Peak"] = sys_append["stream_peak_sub_view_ratio"]
        info["Live Viewers/Subscribers Ratio"]["Date of Peak"] = sys_append["date_of_peak"]
        info["Live Viewers/Subscribers Ratio"]["Subscribers at Peak"] = pull["subscriber_count"]
    
    
    
    sys_append["delta_subs"] = int(pull["subscriber_count"]) - int(info["Subscribers"])
    info["Subscribers"] = pull["subscriber_count"]
    
    sys_append["delta_views"] = int(pull["view_count"]) - int(info["Total Views"])
    info["Total Views"] = pull["view_count"]
    
    sys_append["delta_videos"] = int(pull["video_count"]) - int(info["Videos"])
    info["Videos"] = pull["video_count"]
    
    info["sys_append"] = sys_append
    
    return info

# helper function for calulate_analytics to compute the new average based on the old one
# A(n+1) = [ n*A(n) + x ] / [ n + 1 ]
def add_to_average(current_count, current_average, new_value):
    return (float(current_average)*float(current_count) + float(new_value)) / float(current_count+1)

# processes the time data provided by Holodex videos API
def get_time_data(stream, current_time, debug_file):
    start_actual = stream.get("start_actual")
    start_scheduled = stream.get("start_scheduled")
    published_at = stream.get("published_at")
    end_actual = stream.get("end_actual")
    
    if (start_actual == None): start_actual = stream.get("start_scheduled") # Occurs when stream starts exactly when scheduled
    if (start_scheduled == None): start_scheduled = start_actual # Weird fringe case, maybe streams that are scheduled without a start time?
    if (published_at == None): published_at = start_scheduled # Occurs for guerilla streams
    if (end_actual == None): end_actual = current_time # I don't think this is possible, but prevents errors just in case
    else: end_actual = datetime.fromisoformat(str(end_actual)).replace(tzinfo=None)
    try:
        start_actual = datetime.fromisoformat(start_actual).replace(tzinfo=None)
    except: 
        print(start_actual)
    start_scheduled = datetime.fromisoformat(str(start_scheduled)).replace(tzinfo=None)
    published_at = datetime.fromisoformat(str(published_at)).replace(tzinfo=None)
    
    #propperly formats early streams
    tardiness = start_actual - start_scheduled 
    if (tardiness.total_seconds() < 0):
        tardiness = "-%s" % str(abs(tardiness))
    else:
        tardiness = str(tardiness)
    
    return {
        "start": start_actual.isoformat(),
        "end": end_actual.isoformat(),
        "notice": str(start_actual - published_at),
        "tardiness": tardiness,
        "duration": str(end_actual - start_actual),
    }
    
    

# creates the channel template for new channels
def initialize_channel(pull):
    ret = {
        "Channel Name": pull["name"],
        "Channel ID": pull["id"],
        "Type": pull["type"],
        "Affiliation": {
            "Organization": pull.get("org"),
            "Group": pull.get("suborg")
        },
        "Total Views": pull["view_count"],
        "Subscribers": pull["subscriber_count"],
        "Videos": pull["video_count"],
        "Live Viewership": {
            "Stream Average": 0,
            "Average Peak": 0,
            "All Time Peak": 0,
            "Date of Peak": None
        },
        "Live Viewers/Subscribers Ratio": { 
            "Stream Average": 0,
            "Average Peak": 0,
            "All Time Peak": 0,
            "Subscribers at Peak": 0,
            "Date of Peak": None
        },
        "Streams": []
    }
    return ret
    
