# pyfinmarkets
Terminal Financial Markets 

Python file >>  api_call_yahoo.py  <<  This is the main file that can run by itself with python 3.x, with the required config file.  The python script will call the config file (ticsymbol.conf).   You can edit this file to add or remove ticker symbols as desired.

The setup:
Create a new directory e.g. pyfinmarkets.  Download the files into a new directory.
Open and edit the ticsymbol.conf file, remove and add ticker symbols to this file.  ( symbols should be space separated )

How to run:
( make the .py file and .sh files are executable:   "chmod +x api_call_yahoo.py" )

Open a terminal window.  Type in at the command prompt:  python3 ./api_call_yahoo.py  
This will run the python script once.  If you would like to run it with a refresh rate of 150 seconds, run the bash script.  This uses the 'watch' package ( you may need to install it ) and will run the api_call_yahoo.py script every 150 seconds.

 NOTE:  Do not lower the '150' seconds too low, you may get blocked from calling the Yahoo Finance API.

