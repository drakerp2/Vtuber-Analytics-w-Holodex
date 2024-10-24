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
#        inputimeout
#        requests
#
#! This script is used to link parse_streams and parse_channels
#! Will try and run at even intervals (by default 1:00, 1:15, 1:30, 1:45, 2:00, ...)
#! File writes are done all at once, so forcibly ending the program mid parse *should* be safe, however it is still disadvised
#
# options:
#    -d <filename>
#        the file to write debug info too 
#        sys.stdout by default
#    -t <throwaway duration>
#        ignores streams that have been going for less than the duration (in minutes) 
#        15 by default
#    -i <check interval>
#        the interval of time (in minutes) to wait in between pulling data from the Holodex server
#        inputs that are not factors of 60 will produce unexpected behavior, but will not crash or produce errors
#        15 by default
#    -k <api key location>
#        the file adress of the api key (a blank file with the key on the first line)
#        .\..\apikeys\holodex by default



from parse_streams import parse_streams
from parse_channels import parse_channels
from datetime import datetime
from datetime import timezone
import sys

from inputimeout import inputimeout 

current_time = datetime.now(timezone.utc).replace(tzinfo=None)

debug_file = None
try: debug_file = open(sys.argv[sys.argv.index("-d")+1], 'w', encoding="utf-8")
except: debug_file = sys.stdout


# number of minutes the stream must have gone on for to be recorded
duration_throwaway = None 
try: duration_throwaway = int(sys.argv[sys.argv.index("-t")+1])
except: duration_throwaway = 15

# a value that is not a factor of 60 will produce unintended behavior
check_interval = None 
try: check_interval = int(sys.argv[sys.argv.index("-i")+1])
except: check_interval = 15

header = None
try: header = {"X-APIKEY": open(sys.argv[sys.argv.index("-k")+1], 'r').readline().rstrip('\n')}
except: header = {"X-APIKEY": open("./../apikeys/holodex", 'r').readline().rstrip('\n')}

while(True):
    current_time = datetime.now(timezone.utc).replace(tzinfo=None)

    print("time of parse:", str(current_time), file=debug_file)

    streams = parse_streams(current_time, duration_throwaway, header, debug_file)

    parse_channels(streams, current_time, header, debug_file)

    current_time = datetime.now(timezone.utc).replace(tzinfo=None)

    print("Finished at", current_time, file=debug_file)
    time_to_next_parse = check_interval - (current_time.minute % check_interval) - 1
    time_to_next_parse *= 60
    time_to_next_parse += 60 - current_time.second
    
    print("Time to next parse", time_to_next_parse, file=debug_file)

    try: 
        inputimeout(prompt = "press enter to stop", timeout = time_to_next_parse)
        break
    except: 
        continue
    