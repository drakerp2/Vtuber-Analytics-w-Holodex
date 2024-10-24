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
#        xlsxwriter
#
# todo: make threaded, this is going to start taking *really* long as the quantity of data increases
#



from process_data_dicts import Descriptors, Headers, Styles, Widths, Slice, Formulas

import os
import json

from xlsxwriter import Workbook





## cycles through ./channels and creates a .xlsx spreadsheet
def driver():
   channels = os.listdir("./channels")


   book = Workbook("testsheet.xlsx")
   Styles(book)
   
   sheet = book.add_worksheet("Analytic Data")
   
   book.add_worksheet("Tools")
   
   #book.add_worksheet("_help_org")
   for i in range(len(channels)):
      process_channel(channels[i], book, sheet, i+1)
   None

   format_analytic_head(sheet)
   
   make_tools(book)

   hide_sheets(book)
   book.close()
None


## formats and prints the header for Analytic Data
def format_analytic_head(sheet):
   for col in Descriptors.analytic_data:
      sheet.data_validation(0, col, 0, col, {
         "validate": "any",
         "input_title": Descriptors.analytic_data[col][0],
         "input_message": Descriptors.analytic_data[col][1],
      })
   None

   for col in Styles.Headers.analytic_data:
      sheet.set_column_pixels(col, col, Widths.analytic_data[col], Styles.analytic_data[col])
      sheet.write(0, col, Headers.analytic_data[col], Styles.Headers.analytic_data[col]) 
   None
None



## Takes a channel and parses it's data, writing it to the channel sheet and the Analytic Data sheet
## @param channel: the channel being parsed
## @param book: the workbook being used
## @param sheet: ! this should be the Analytic Data sheet
## @param row: the row of the Analytic Data sheet to be written too
def process_channel(channel, book, sheet, row):
   with open("./channels/%s" % channel, 'r', encoding="utf-8") as channel_file:
      data = json.load(channel_file)

      if data["Affiliation"]["Group"] is None: data["Affiliation"]["Group"] = "None"
      else: data["Affiliation"]["Group"] = data["Affiliation"]["Group"][2:] # this is a band-aid for an issue that needs to be fixed up stream
      data["English Name"] = channel

      data_slice = Slice.analytic_data(data)
      
      for col in data_slice:
         if (col == 10 or col == 14):
            sheet.write_datetime(row, col, data_slice[col], Styles.analytic_data[col])
            continue
         None

         sheet.write(row, col, data_slice[col], Styles.analytic_data[col])
      None
   
      handle_org(book, (data["Affiliation"]["Organization"], data["Affiliation"]["Group"], channel))
      process_streams(book.add_worksheet(channel[:31]), data["Streams"]) # excel doesn't like sheet names > 31 characters
None


org_helper = {}


## recurses through an org placeing it in the appropriate helper sheet
## @param book: the workbook being used
## @param next: the tuple of sub-orgs, expected to be (organization, group, channel)
## @param org: the current org being looked at, None by default
## @param sheet_name: the name of base sheet, "_help_org" by default, shouldn't be more than 11 characters, needs to be already declared in book
def handle_org(book, next, org = None, sheet_name="_help_org"):
   global org_helper

   if len(next) == 3: 
      handle_org(book, next[1:], next[0], sheet_name)
      return
   
   if org is None or org == "":
      org = "None"
   None

   org = org.replace(':', '։') # deprectate this with overhauled organization pulling

   sheet = book.get_worksheet_by_name(sheet_name)
   if sheet is None:
      sheet = book.add_worksheet(sheet_name)
      org_helper[sheet_name] = 0
   None
   
   new_sheet_name = "%s_%s" % (sheet_name, org[:9]) ## truncates so it doesn't go ever 31 char limit

   if len(next) == 0: ## this is not an org, this is just the vtuber themselves
      sheet.write(org_helper[sheet_name], 0, org)
      org_helper[sheet_name] += 1
      return
   None

   if book.get_worksheet_by_name(new_sheet_name) is None:
      book.get_worksheet_by_name(sheet_name).write(org_helper[sheet_name], 0, org)
      org_helper[sheet_name] += 1
   None

   handle_org(book, next[1:], next[0], new_sheet_name)
None



# Does not utilize book.active meaning it should be threadable
## process the stream data onto a channel sheet
## @param sheet: the channel sheet
## @param streams: the list containing all the streams
def process_streams(sheet, streams):
   for row in range(len(streams)):
      stream = streams[row]
      data_slice = Slice.channel_data(stream)
      for col in data_slice:
         if (col == 4 or col == 6 or col == 9):
            sheet.write_datetime(row, col, data_slice[col])
            continue
         None

         sheet.write(row, col, data_slice[col])
   None

   sheet.hide() #by doing this last, if an error occurs the sheet will not be hidden, allowing easier diagnosis
None
   


## Makes the tool page
## @param book: the workbook being used
## todo: this should probably get broken up into smaller pieces, data_vals should be moved to process_data_dicts and looped through
def make_tools(book):
   sheet = book.get_worksheet_by_name("_help_org")
   for cell in Formulas._help_org:
      sheet.write_dynamic_array_formula(f"{cell:s}:{cell:s}", Formulas._help_org[cell])
   None

   sheet = book.get_worksheet_by_name("Tools")

   sheet.set_column_pixels(0,1,60)
   sheet.set_column_pixels(2,2,150)
   

   sheet.merge_range("A1:C1", "Select the vtuber you want to pull data on:", Styles.data_val[0])

   sheet.merge_range("A2:C2", "", Styles.data_val[1])
   sheet.data_validation("A2:C2", {
      "validate": "list",
      "source": "=_help_org!$B$1:$B$1000",

      "input_title": "Organization",
      "input_message": "The organization or company that your vtuber belongs too",
   })
   sheet.write("A2:C2", "Phase Connect", Styles.data_val[1])

   sheet.merge_range("A3:C3", "", Styles.data_val[2])
   sheet.data_validation("A3:C3", {
      "validate": "list",
      "source": "=_help_org!$C$1:$C$1000",
      "input_title": "Group",
      "input_message": "The group within their organization your vtuber belongs too",
   })
   sheet.write("A3:C3", "Phase 03 - Euphoria", Styles.data_val[2])

   sheet.merge_range("A4:C4", "", Styles.data_val[3])
   sheet.data_validation("A4:C4", {
      "validate": "list",
      "source": "=_help_org!$D$1:$D$1000",
      "input_title": "VTuber",
      "input_message": "If your vtuber isn't in this list, they haven't had data pulled on them, you entered their company information in wrong, or the data recieved from holodex was incorrect",
   })
   sheet.write("A4:C4", "Runie Ruse", Styles.data_val[3])

   sheet.write("A6:A6", "#shorts:", Styles.data_val[4])

   sheet.data_validation("B6:B6", {
      "validate": "list",
      "source": ["Include", "Exclude", "Only"],
   })
   sheet.write("B6", "Include", Styles.data_val[5])


   
   offset_col = ord('H') - ord('A')

   for col in Descriptors.channel_data:
      colN = offset_col + col
      sheet.data_validation(0, colN, 0, colN, {
         "validate": "any",
         "input_title": Descriptors.channel_data[col][0],
         "input_message": Descriptors.channel_data[col][1],
      })
   None

   for col in range(len(Headers.channel_data)-1):
      colN = offset_col + col

      sheet.set_column_pixels(colN, colN, Widths.channel_data[col], Styles.channel_data[col])
      
      sheet.write_string(0, colN, Headers.channel_data[col],  Styles.Headers.channel_data[col])
   None

   
   sheet_help = book.add_worksheet("_Tools_help")
   sheet_help.write_formula("U1", Formulas._Tools_help["U1"])
   sheet_help.write_dynamic_array_formula("A1:A1", Formulas._Tools_help["A1"])

   sheet.write_dynamic_array_formula("H2:H2", Formulas.Tools["H2"])

   sheet_help.write_dynamic_array_formula("W1:W1", Formulas._Tools_help["W1"])

   # This makes significantly more sense in the excel_formula.txt version
   for col in range(4):
      foo = "AVERAGE" if col%2 == 0 else "MAX" # does anyone else find python ternary objectively worst to read in every way when compared to c style ternary?
      c =  chr(ord('A') + 7 + col + (0 if col<2 else 1))
      off = ord('X') - ord('A') + col
      sheet_help.write_dynamic_array_formula(0, off, 0, off, Formulas._Tools_help["X1:AA1"].format(FUNC=foo, c=c))
None   
   



def hide_sheets(book):
   for sheet in book.worksheets():
      if sheet.get_name()[0] == '_':
         sheet.hide()
None


driver()