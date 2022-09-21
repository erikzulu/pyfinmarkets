# pyfinmarkets
Terminal Financial Markets 

Python file >>  api_call_yahoo.py  <<  This is the main file that can run by itself with python 3.x, also need the confic file.
( make sure this is executable via:   "chmod +x api_call_yahoo.py" )

The python script code will call a config file (ticsymbol.conf).   You can edit this file to add or remove ticker symbols as desired.

The bash script (linux / mac ) included, can be used to run continously and refresh every 150 seconds.  
  NOTE:  Do not lower the '150' seconds too low, you may get blocked from calling the Yahoo Finance API.

