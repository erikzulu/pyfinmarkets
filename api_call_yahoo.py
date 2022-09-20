# API Program for Yahoo Finance

# IMPORT PYTHON Modules
import json, requests, os, re
from urllib import response
from datetime import datetime

# Define global variables
assets = ('')


class ANSI():				# Set the object color, style, background color
    def background(code):
        return "\33[{code}m".format(code=code)
  
    def style_text(code):
        return "\33[{code}m".format(code=code)
  
    def color_text(code):
        return "\33[{code}m".format(code=code)


def dbOpen():				# Load SQL data base engine "sqlite3"
	global c, conn
	import sqlite3,sys

    # Open database file(s)
	try:
		conn = sqlite3.connect('finmkt.db')
	except:
		print('finmkt.db file connection failed.')
	finally:
		print('SQL version: '+str(sqlite3.version_info))

	#  Set up db connection cursor
	c = conn.cursor()


def get_dttm(xdt):			# Get and return current date & time to 1,000 ms
	xdt = datetime.now()
	# .strftime("%d/%m/%Y %H:%M:%S")
	return xdt


def get_conf():						# Read the config file with list of ticker symbols
	f = ("")
	fpath = os.path.sys.path[0]
	yfile = 'ticsymbol.conf'
	fpathfile = str(fpath) + os.sep + str(yfile)

	if os.path.isfile(fpathfile) and os.access(fpathfile, os.R_OK):
		f = open(fpathfile, "rt")
	else:
		print("  Config file for ticker symbols does not exist or found.   Please create ticsybols.conf.")
		print("  Ticker symbols should be space separated.  e.g.  ^IXIC ^FTSE MMM BTC-USD")
		exit()

	assets = f.read()				# --- read the file
	assets = assets[:len(assets)-1]	# Remove the'\n' from the end of the file read, next line 
	
#	assetList = f.strip()			# --- strip space from begin and end.

#	if assetList == '':				# ---  if there is nothing, ...
	if f == '':						# ---  if there is nothing, ...
		# empty file
		print("Config file "+ yfile + "has no values.   Setting to defaults. ^GSPS ^FTSE ^N225 BTC-USD")
		f = "^GSPS ^FTSE ^N225 BTC-USD"
	else:
		assetList = assets.split(" ")				# --- Split string into 'list'
		assetList = list(dict.fromkeys(assetList))	# --- remove duplicates using 'dict' function
		assets = ",".join(assetList)				# --- Convert back to comma separated string for API call
	
	f.close()						# --- close the open file.   contents are in 'f' variable
	return assets



def apiCallYahoo(assetsList):		# Function to call API
	# This is the list of ticker symbols to retrieve data for.
#	assetList = ("^GSPC ^FTSE ^N225 GC=F KO MMM T AMZN BTC-USD ETH-USD SCHD XLE")
	assetList = assetsList
#	print(assetList)				# --- Test to see if we are getting values passed in
	ycolrst = ANSI.color_text(0)

	# Which service are we calling:  limited to less than 500 per day;  5 per minute
	API_BASEURL="https://query1.finance.yahoo.com"

	# ------ Yahoo finance v7
	API_ENDPOINTv7="/v7/finance/quote?lang=en-US&region=US"
	API_FIELDS="marketState"

	# ------ Yahoo finance v11
	API_ENDPOINTv11="/v11/finance/quoteSummary/"
	API_MODULES="defaultKeyStatistics"
#	Set endpoint to version
	API_ENDPOINT=API_ENDPOINTv7
	api_setURL = API_BASEURL+API_ENDPOINT+API_FIELDS+"&symbols="+assetList

#	Yahoo finance requires a good browser user agent ( python agent produces 403 error )
#	Call the URL API 
	jresult = requests.get(api_setURL, headers={'User-agent': 'Mozilla/5.0'})

	if (jresult.status_code != 200):	# check to make sure we get a good response
		print("The request FAILED.")
		print(response)					# --- HTTP response code
		exit

	assetValue = json.loads(jresult.text)
	respArray = assetValue["quoteResponse"]			# ["result"]
	
#	Print a output heading - in yellow
	print('\33[33m{0:<10} ' ' {1:<40} ' ' {2:>9} ' ' {3:^10} ' ' {4:>13} ' ' {5:<15}\33[0m'.format('Symbol','Name','Price','Change%','Volume','Market Type'))
	print("=" * 110)				# print "=" character x times 

# ---	get assets from array and print to show what we are getting
	for q in respArray["result"]:
		
		ysymbol = (q["symbol"])
		if "shortName" and "regularMarketPrice" in q:
			yshortName = (q["shortName"])
		else: continue				# If these to fields not found in the result, abandon and move on to next symbol
		ytypeDisp = (q["typeDisp"])
		yregMktPrice = (q["regularMarketPrice"])
		ymktChgPct = (q["regularMarketChangePercent"])
		y52wkRge = (q["fiftyTwoWeekRange"])
		ymktVol = (q["regularMarketVolume"])
		if ymktChgPct < 0:
			ycolor = ANSI.color_text(31)
		elif ymktChgPct > 0:
			ycolor = ANSI.color_text(32)
		else:
			ycolor = ANSI.color_text(0)
		print('{:<10} ' ' {:<40} ' '{:10,.2f}' ' {} {:7.2f} {} ' ' {:>15,} ' ' {:15}'.format(ysymbol, yshortName, yregMktPrice, ycolor, ymktChgPct, ycolrst, ymktVol, ytypeDisp))
	
	print("\33[35m  :Last refresh time:"+str(datetime.now())+"					|Press Ctrl+C to quit|\033[0;0m")
# END OF "def apiCallYahoo"

def main():							# Main function calling all sub functions
	assets = get_conf()				# Get symbols assests from config file
	apiCallYahoo(assets)			# Use the assests, call api, print results


# START  ===  Call function to start python script
main()


### --- END OF SCRIPT --- ###
#   Some general stuff;  remenances, testing, etc.
#	call to get time
#		xdt = ''		# global variable
#		print("# --- Start query --- # "+str(get_dttm(xdt)))
#	print(q["symbol"],q["shortName"],q["typeDisp"],q["regularMarketPrice"],q["fiftyTwoWeekRange"], q["regularMarketVolume"])
#	print(json.dumps(respArray, indent=4, separators=(". ", " = ")))		# Testing:  view query output text

#   List of yahoo modules here:   https://syncwith.com/yahoo-finance/yahoo-finance-api#9ec3ad7d4e144db2b16a3d6545bd528c
