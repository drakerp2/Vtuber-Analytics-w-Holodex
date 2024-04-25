# !!! WILL CRASH IF YOU DO NOT HAVE A FOLDER NAMED "streams" AND "channels" IN THE DIRECTORY WHERE YOUR SCRIPTS ARE LOCATED !!!

Credits: 
      Holodex License: https://docs.holodex.net/#section/LICENSE
      Holodex Homepage: https://holodex.net/
      Oshi: Runie Ruse (Phase Connect) https://www.youtube.com/@RunieRuse

pip requirements:
      inputimeout
      requests

# parse.py is the only file meant to be run, parse_channels.py and parse_streams.py are drivers

# The parse.py script is used to link parse_streams and parse_channels
# Will try and run at even intervals (by default 1:00, 1:15, 1:30, 1:45, 2:00, ...)
# File writes are done all at once, so forcibly ending the program mid parse *should* be safe, however it is still disadvised

options:
   -d <filename>
       the file to write debug info too 
       sys.stdout by default
   -t <throwaway duration>
       ignores streams that have been going for less than the duration (in minutes) 
       15 by default
   -i <check interval>
       the interval of time (in minutes) to wait in between pulling data from the Holodex server
       inputs that are not factors of 60 will produce unexpected behavior, but will not crash or produce errors
       15 by default
