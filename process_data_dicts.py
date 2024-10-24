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
#        None
#
# This is a glorified data file to get the massive amounts of raw formatting required out of process_data.py to increase it's readability
#

from datetime import datetime

light_blue = "DCE6F1"
off_white = "F2F2F2"

class Headers:
   analytic_data = {
      0: "Channel",
      1: "English Name",
      2: "Channel ID",
      3: "Affiliation",
      4: "Total Views",
      5: "Subs",
      6: "Vids",
      7: "VA",
      8: "VAP",
      9: "ATVP",
      10: "DVP",
      11: "RA",
      12: "RAP",
      13: "ATRP",
      14: "DRP", 
   }

   channel_data = {
      0: "Stream Title",
      1: "Topics",
      2: "Notice",
      3: "Tardiness",
      4: "Start Time",
      5: "Duration",
      6: "End Time",
      7: "VA",
      8: "VP",
      9: "DVP",
      10: "RA",
      11: "RP",
      12: "Subs",
      13: "ΔSubs",
      14: "Views",
      15: "ΔViews",
      16: "Vids",
      17: "ΔVids",
      18: "#shorts", #this isn't actually used, but is left in to provide clarity, as the column is present in _Tools_help and the stream data
   }
None

class Descriptors:
   analytic_data = {
      2: [
         "YouTube Channel ID",
         "This is the unique identification code given to the youtube channel, used by YouTube API to store data\n\nnote: all Channel IDs begin with UC, the User ID is the same, but without the UC at the start",
      ], 
      5: [
         "Subscriber Count",
         "The total number of subscribers as of the end of their last stream",
      ],
      6: [
         "Video Count",
         "The total number of videos uploaded to the channel as of the end of their last stream",
      ],
      7: [
         "Viewer Average",
         "The average number of live viewers across all streams",
      ],
      8: [
         "Viewer Average Peak",
         "The average peak viewer count across all streams\n\nnote: this data point will be bias towards vtubers who get raided more often"
      ],
      9: [
         "All Time Viewer Peak",
         "The highest viewer count this vtuber has ever recoreded\n\nnote: records taken at ~15 minute intervals, so the real peak is likely to be slightly higher"
      ],
      10: [
         "Date of Viewer Peak",
         "The date and time at which the all time viewer peak was recored",
      ],
      11: [
         "Ratio Average",
         "The average ratio of live viewers to subscribers\n\nnote: this is taken based on subscribers at end of stream, so donothons could skew the numbers (though this is less of an issue with YouTube then Twitch)",
      ],
      12: [
         "Ratio Average Peak",
         "The viewer to subscriber ratio of the peak viewership averaged across all streams",
      ],
      13: [
         "All Time Ratio Peak",
         "The highest viewer to subscriber ratio ever recorded",
      ],
      14: [
         "Date of Ratio Peak",
         "The date the highest viewer to subscriber ratio was recorded\n\nnote: this will almost always be the same as DAP until this project has had time to age",
      ]
   }

   channel_data = {
      1: [
         "Stream Topics",
         "The topics the stream was catagorized under",
      ],
      2: [
         "Prior Notice",
         "How much time was there between when the stream was added to the schedule and when the stream began",
      ],
      3: [
         "Tardiness",
         "How late (or early) did the stream go live in respect to it's scheduled start time",
      ],
      4: [
         "Start Time",
         "The time and date the stream went live",
      ],
      5: [
         "Stream Duration",
         "How long the stream lasted",
      ],
      6: [
         "End Time",
         "The time and date the stream ended",
      ],
      7: [
         "Viewer Average",
         "The average number of live viewers across the stream",
      ],
      8: [
         "Viewer Peak",
         "The highest number of live viewers recorded during the stream\n\nnote: data pulled every 15 minutes, so real peak is likely to be slightly higher"
      ],
      9: [
         "Date of Viewer Peak",
         "The date and time at which the peak viewer count occured",
      ],
      10: [
         "Ratio Average",
         "The average viewer to subscriber ratio of the stream\n\nnote: based on subscriber count at end of stream",
      ],
      11: [
         "Ratio Peak",
         "The ratio of viewers to subscribers at the stream's peak viewership",
      ],
      12: [
         "Subscribers at Time of Stream",
         "The number of subscribers at the time of the stream rounded to the nearest thousandth\n\nnote: number comes rounded by the YouTube API, more accurate numbers would add significant complexity, processing time, and potentially cost",
      ],
      13: [
         "Subscribers Gained",
         "The change in the number of subscribers (given by the YouTube API) since the end of the prior stream\n\nnote: this is essentially the low end, with the high end being this+1000",
      ],
      14: [
         "Views at Time of Stream",
         "The total number of views across all videos on the channel at the time of the stream.",
      ],
      15: [
         "Views Gained",
         "The number of views across videos on the channel gained since the prior stream\n\nnote: abnormally low or negative values often indicate a video was removed or made private",
      ],
      16: [
         "Videos at Time of Stream",
         "The total number of videos uploaded to the channel at the time of the stream"
      ],
      17: [
         "Change in Video Count",
         "How many videos have been uploaded since the prior stream",
      ],
   }
None

class Styles:
   analytic_data = None
   channel_data = None
   data_val = None

   def __init__(self, book):
      Styles.set_analytic_data(book)
      Styles.set_channel_data(book)
      Styles.set_data_val(book)
      Styles.Headers.set_analytic_data(book)
      Styles.Headers.set_channel_data(book)
   None

   def set_analytic_data(book):
      Styles.analytic_data = {
         0: book.add_format({
            "border": 1,
            "bg_color": light_blue,
            "num_format": "#,##0",
         }),
         1: book.add_format({
            "border": 1,
            "bg_color": off_white,
            "num_format": "#,##0",
         }),
         2: book.add_format({
            "border": 1,
            "bg_color": light_blue,
            "num_format": "#0.00%"
         })
      }
      Styles.analytic_data = {
         0: book.add_format({
            "border": 1,
            "left": 2,
            "bg_color": light_blue,
         }),
         1: book.add_format({
            "border": 1,
            "bg_color": off_white,
         }),
         2: book.add_format({
            "border": 1,
            "bg_color": light_blue,
         }),
         3: book.add_format({
            "border": 1,
            "bg_color": off_white,
            "align": "right",
         }),
         4: Styles.analytic_data[0],
         5: Styles.analytic_data[0],
         6: Styles.analytic_data[0],
         7: Styles.analytic_data[1],
         8: Styles.analytic_data[1],
         9: Styles.analytic_data[1],
         10: book.add_format({
            "border": 1,
            "bg_color": off_white,
            "num_format": "dd/mm/yy hh:mm",
         }),
         11: Styles.analytic_data[2],
         12: Styles.analytic_data[2],
         13: Styles.analytic_data[2],
         14: book.add_format({
            "border": 1,
            "right": 2,
            "bg_color": light_blue,
            "num_format": "dd/mm/yy hh:mm",
         }),
      }
   None

   def set_channel_data(book): 
      Styles.channel_data = {
         0: book.add_format({
            "bg_color": off_white,
            "border": 1,
            "num_format": "hh:mm:ss",
            "align": "right",
         }),
         1: book.add_format({
            "bg_color": light_blue,
            "border": 1,
            "num_format": "dd/mm/yy hh:mm",
         }),
         2: book.add_format({
            "border": 1,
            "bg_color": off_white,
            "num_format": "#,##0",
         }),
      }
      Styles.channel_data = {
         0: Styles.analytic_data[0], 
         1: Styles.analytic_data[1], 
         2: book.add_format({ 
            "bg_color": light_blue,
            "border": 1,
            "num_format": "hh:mm:ss",
            "align": "right",
         }),
         3: Styles.channel_data[0], 
         4: Styles.channel_data[1],
         5: Styles.channel_data[0], 
         6: Styles.channel_data[1], 
         7: Styles.analytic_data[7], 
         8: Styles.analytic_data[8], 
         9: Styles.analytic_data[10], 
         10: Styles.analytic_data[11],
         11: Styles.analytic_data[12],
         12: Styles.channel_data[2],
         13: Styles.channel_data[2],
         14: Styles.analytic_data[4],
         15: Styles.analytic_data[4],
         16: Styles.channel_data[2],
         17: book.add_format({
            "border": 1,
            "right": 2,
            "bg_color": off_white,
            "num_format": "#,##0",
         }),
      }
   None

   def set_data_val(book):
      Styles.data_val = {
         0: book.add_format({
            "bg_color": light_blue,
            "right": 2,
            "bottom": 1,
         }),
         1: book.add_format({
            "bg_color": light_blue,
            "right": 2,
            "top": 1,
         }),
         2: book.add_format({
            "bg_color": light_blue,
            "right": 2,
         }),
         3: book.add_format({
            "bg_color": light_blue,
            "right": 2,
            "bottom": 2,
         }),
         4: book.add_format({
            "bg_color": light_blue,
            "bottom": 2,
            "top": 2
         }),
         5: book.add_format({
            "bg_color": light_blue,
            "right": 2,
            "bottom": 2,
            "top": 2
         }),
      }
   None

   class Headers:
      analytic_data = None
      channel_data = None

      def set_analytic_data(book):
         Styles.Headers.analytic_data = {
            0: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": light_blue,
               "align": "center",
            }),
            1: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": off_white,
               "align": "center",
            }),
            2: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": light_blue,
               "align": "center",
            })
         }
         Styles.Headers.analytic_data = {
            0: book.add_format({
               "border": 1,
               "bottom": 2,
               "left": 2,
               "bg_color": light_blue,
               "align": "center",
            }),
            1: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": off_white,
               "align": "center",
            }),
            2: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": light_blue,
               "align": "center",
            }),
            3: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": off_white,
               "align": "center",
            }),
            4: Styles.Headers.analytic_data[0],
            5: Styles.Headers.analytic_data[0],
            6: Styles.Headers.analytic_data[0],
            7: Styles.Headers.analytic_data[1],
            8: Styles.Headers.analytic_data[1],
            9: Styles.Headers.analytic_data[1],
            10: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": off_white,
               "align": "center",
            }),
            11: Styles.Headers.analytic_data[2],
            12: Styles.Headers.analytic_data[2],
            13: Styles.Headers.analytic_data[2],
            14: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": light_blue,
               "align": "center",
            }),
         }   
      None

      def set_channel_data(book):
         Styles.Headers.channel_data = {
            0: book.add_format({
               "bg_color": off_white,
               "border": 1,
               "bottom": 2,
               "align": "center",
            }),
            1: book.add_format({
               "bg_color": light_blue,
               "border": 1,
               "bottom": 2,
               "align": "center",
            }),
            2: book.add_format({
               "border": 1,
               "bottom": 2,
               "bg_color": off_white,
               "align": "center",
            }),
         }
         Styles.Headers.channel_data = {
            0: Styles.Headers.analytic_data[0], 
            1: Styles.Headers.analytic_data[1], 
            2: book.add_format({ 
               "bg_color": light_blue,
               "border": 1,
               "bottom": 2,
               "align": "right",
               "align": "center",
            }),
            3: Styles.Headers.channel_data[0], 
            4: Styles.Headers.channel_data[1],
            5: Styles.Headers.channel_data[0], 
            6: Styles.Headers.channel_data[1], 
            7: Styles.Headers.analytic_data[7], 
            8: Styles.Headers.analytic_data[8], 
            9: Styles.Headers.analytic_data[10], 
            10: Styles.Headers.analytic_data[11],
            11: Styles.Headers.analytic_data[12],
            12: Styles.Headers.channel_data[2],
            13: Styles.Headers.channel_data[2],
            14: Styles.Headers.analytic_data[4],
            15: Styles.Headers.analytic_data[4],
            16: Styles.Headers.channel_data[2],
            17: book.add_format({
               "border": 1,
               "bottom": 2,
               "right": 2,
               "bg_color": off_white,
               "align": "center",
            }),
         } 
      None
   None
None

class Widths:
   analytic_data = {
      0: 350,
      1: 160,
      2: 72,
      3: 300,
      4: 87,
      5: 70,
      6: 45,
      7: 52,
      8: 52,
      9: 52,
      10: 95,
      11: 50,
      12: 50,
      13: 56,
      14: 95
   }

   channel_data = {
      0: 550,
      1: 150,
      2: 62,
      3: 62,
      4: 95,
      5: 62,
      6: 95,
      7: 52,
      8: 52,
      9: 95,
      10: 50,
      11: 50,
      12: 70,
      13: 52,
      14: 87,
      15: 70,
      16: 45,
      17: 40
   }
None


class Slice:
   def analytic_data(data):
      return {
         0: data["Channel Name"],
         1: data["English Name"],
         2: data["Channel ID"],
         3: "%s of %s" % (data["Affiliation"]["Group"], data["Affiliation"]["Organization"]),
         4: data["Total Views"],
         5: data["Subscribers"],
         6: data["Videos"],
         7: data["Live Viewership"]["Stream Average"],
         8: data["Live Viewership"]["Average Peak"],
         9: data["Live Viewership"]["All Time Peak"],
         10: datetime.fromisoformat(data["Live Viewership"]["Date of Peak"]),
         11: data["Live Viewers/Subscribers Ratio"]["Stream Average"],
         12: data["Live Viewers/Subscribers Ratio"]["Average Peak"],
         13: data["Live Viewers/Subscribers Ratio"]["All Time Peak"],
         14: datetime.fromisoformat(data["Live Viewers/Subscribers Ratio"]["Date of Peak"]),
      }
   None
   
   def channel_data(stream):
      return {
         0: stream["Title"],
         1: stream["Topics"] if stream["Topics"] is not None and stream["Topics"] != "" and stream["Topics"] != 0 else "None",
         2: get_time(stream["Prior Notice"]),
         3: get_time(stream["Tardiness"]),
         4: datetime.fromisoformat(stream["Start"]),
         5: get_time(stream["Duration"]),
         6: datetime.fromisoformat(stream["End"]),
         7: stream["Live Viewership"]["Average"],
         8: stream["Live Viewership"]["Peak"],
         9: datetime.fromisoformat(stream["Live Viewership"]["Date of Peak"]),
         10: stream["Live Viewers/Subscribers Ratio"]["Average"],
         11: stream["Live Viewers/Subscribers Ratio"]["Peak"],
         12: stream["Subscribers"]["Current"],
         13: stream["Subscribers"]["Gained"],
         14: stream["Views"]["Current"],
         15: stream["Views"]["Gained"],
         16: stream["Videos"]["Current"],
         17: stream["Videos"]["Gained"],
         18: stream["Title"].find("#shorts") >= 0,
      }
   None
None


_help_org_formula_helper = '=          \
_xlfn.LET(                             \
   _xlpm.sorted,                       \
   _xlfn.LET(                          \
      _xlpm.sheetname,                 \
      INDIRECT(                        \
         "\'_help_org" &                \
         {FORMULA:s} &                 \
         "\'!$A$1:$A$1000"             \
      ),                               \
      _xlfn.SORTBY(                    \
         _xlpm.sheetname,              \
         _xlfn.BYROW(                  \
            _xlpm.sheetname,           \
            _xlfn.LAMBDA(              \
               _xlpm.array,            \
               CODE(                   \
                  LEFT(_xlpm.array)    \
               )                       \
            )                          \
         )                             \
      )                                \
   ),                                  \
   _xlfn.FILTER(                       \
      _xlpm.sorted,                    \
      _xlpm.sorted<>{{0}}              \
   )                                   \
)'

# this entire class is a feable attempt at increasing the readability of excel formulas
class Formulas:
   _help_org = {
      "B1": _help_org_formula_helper.format(FORMULA= '""'),   

      "C1": _help_org_formula_helper.format(FORMULA= '"_" & LEFT(Tools!$A$2, 9)'),
         
      "D1": _help_org_formula_helper.format(FORMULA= '"_" & LEFT(Tools!$A$2, 9) & "_" & LEFT(Tools!$A$3, 9)'),   
   }

   Tools = {
# -------------------------------------------------\
      "H2": '=                                     \
         FILTER(                                   \
            INDIRECT(                              \
               "_Tools_help!$A$1:$R$" &            \
               _Tools_help!U1                      \
            ),                                     \
            INDIRECT(                              \
               "_Tools_help!$S$1:$S$" &            \
               _Tools_help!U1                      \
            )=SWITCH(                              \
               B6,                                 \
               "Exclude",{FALSE},                  \
               "Only",{TRUE},                      \
               INDIRECT(                           \
                  "_Tools_help!$S$1:$S$" &         \
                  _Tools_help!U1                   \
               )                                   \
            )                                      \
         )'
   }

   _Tools_help = {
# -------------------------------------------------\
      "A1": "=                                     \
         INDIRECT(                                 \
            \"'\" &                                \
            LEFT(Tools!A4, 31) &                   \
            \"'!$A$1:$S$\" &                       \
            U1                                     \
         )",
# -------------------------------------------------\      
      "U1": "=                                     \
         COUNT(                                    \
            INDIRECT(                              \
               \"'\" &                             \
               LEFT(Tools!A4, 31) &                \
               \"'!$Q$1:$Q$1000\"                  \
            )                                      \
         )",
# -------------------------------------------------\
      "W1": "=                                     \
         UNIQUE(                                   \
            INDIRECT(                              \
               \"$B$1:$B$\" &                      \
               U1                                  \
            )                                      \
         )",
# -------------------------------------------------\ 
      "X1:AA1": '=                                 \
         _xlfn.LET(                                \
            _xlpm.col,                             \
            _xlfn.BYROW(                           \
               W1:W1000, _xlfn.LAMBDA(             \
                  _xlpm.array,                     \
                  {FUNC:s}(                        \
                     _xlfn.FILTER(                 \
                        INDIRECT(                  \
                           \"${c:s}$1:${c:s}$\" &  \
                           U1                      \
                        ),                         \
                        INDIRECT(                  \
                           "$B$1:$B$" &            \
                           U1                      \
                        )=_xlpm.array,             \
                        0                          \
                     )                             \
                  )                                \
               )                                   \
            ),                                     \
            _xlfn.FILTER(                          \
               _xlpm.col,                          \
               _xlpm.col<>{{0}}                      \
            )                                      \
         )'
   }
None


def get_time(time_str):
   temp = time_str.split()

   if len(temp) > 1:
      time = temp[2].split(":")
      hour = int(time[0])
      hour += int(temp[0]) * 24
      time[0] = str(hour)
      time_str = ':'.join(time)
   None
   
   return time_str
None