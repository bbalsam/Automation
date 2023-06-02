#================================================================
#VERSION
#================================================================
#00.00			Original basic download with tweaking and working proof of concept.
#00.01			Testing to upload data to database.
#00.02			Upload to database confirmed. Added log file for error reporting, and error bypass.
#00.03			Create key handling for SQL upload.
#================================================================

import datetime
import yfinance as yf
import pandas as pd
import pyodbc
import time

from datetime import datetime, timedelta
from pandas_datareader import data as pdr
from datetime import date



#================================================================
#Code to allow Yahoo! to recognize API call
#================================================================
yf.pdr_override()


#================================================================
#Define variables
#================================================================
#date = datetime.date.today()
year = str(datetime.now().year)
month = str(datetime.now().month)
day = str(datetime.now().day)
timestamp = time.strftime('%H%M%S')
today = date.today()

while len(month) < 2:
	month = '0' + month

while len(day) < 2:
	day = '0' + day

#===============================================
#Error log file
#===============================================

logfilelocation = r'C:\Users\brett\OneDrive\Documents\Excel\Trading\PyProject\ErrorReports\\'
print('Logfilelocation: ' + logfilelocation)

logfilename = str(year + month + day +  '_' + timestamp + '_ErrorReport.txt')
print('LogFileName: ' + logfilename)

logfile = logfilelocation + logfilename
print('LogFile: ' + logfile)

ErrorLog = '=================================================================================================\r\n' + 'JOB FAILURES:\r\n'  + '=================================================================================================\r\n'

f = open(logfile,'a+')
f.write(ErrorLog)

#===============================================
#New code configured from: https://reasonabledeviations.com/2018/02/01/stock-price-database/#database-schema
#===============================================

conn = pyodbc.connect(DRIVER='{SQL Server}',SERVER='LAPTOP-D6TKOBQR\SQLEXPRESS01',DATABASE='stock',Trusted_connection='yes')
crsr = conn.cursor()

#===============================================
#Backfill database with new securities
#===============================================
print('Backfill of new securities to database begin')

try:
	script = """SELECT
					TICKER
				FROM
					STOCK_DESCRIPTION
				LEFT JOIN
					(SELECT strTick FROM STOCKS GROUP BY strTick) s ON s.strTick = TICKER
				WHERE
					s.strTick IS NULL"""
	crsr.execute(script)
	print(crsr.execute(script))
	columns = [desc[0] for desc in crsr.description]
	data = crsr.fetchall()
	df1 = pd.DataFrame.from_records(data=data,columns=columns)
	ticker_list = []
	for x in data:
		ticker_list.append(x[0])
	print(ticker_list)
	# crsr.close()
except Exception as e:
	print('Query to pull ticker list failed')

#ticker_list = ['GBTC','ETHE']

# We can get data by our choice by giving days bracket
#start_date = datetime.datetime.strptime('2020–01–01','%Y-%m-%d')
#end_date= datetime.date(2020, 6, 26)#'2020–06–26'
#===============================================
#commented below for testing
#files=[]
#commented above for testing
#===============================================


def getData(ticker):
	#print(ticker)cd
	try:
		data = pdr.get_data_yahoo(ticker, start=today-timedelta(18000 ), end=today) #18000 in range
		#===============================================
		#commented below for testing
			#dataname= ticker+'_'+str(today)
			#files.append(dataname)
			#SaveData(data, dataname)
		#commented above for testing
		#===============================================
		# Create a data folder in your current dir.
		#===============================================
		#commented below for testing
		# def SaveData(df, filename):
			# df.to_csv('.\SANDPDownload\\'+filename+'.csv')
		#commented above for testing
		#===============================================
		#This loop will iterate over ticker list, will pass one ticker to get data, and save that data as file.
		#print(data)
		#===============================================
		#New code configured from: https://reasonabledeviations.com/2018/02/01/stock-price-database/#database-schema
		#===============================================
		for row in data.itertuples():
			values = list(row)
			#print(values)
			values.append(ticker)
			newval = str(values[0])
			newval = newval.replace(' 00:00:00','')
			newval = newval.replace('-','')
			newval = (values[7] + '_' + newval)
			values.append(newval)
			try:
				crsr.execute("""INSERT INTO dbo.STOCKS (dtDate,decOpen,decHigh,decLow,decClose,decAdjClose,intVol,strTick,ID)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
				tuple(values))
				conn.commit()
			except Exception as e:
				try: 
					miscerr = miscerr + 'error: ' + str(newval) + str(e) + '\r\n'
				except:
					miscerr = 'error: ' + str(newval) + str(e) + '\r\n'
		#===============================================
	except Exception as e:
		ErrorLog = """'""" + str(ticker) + """'""" + ','
		f.write(ErrorLog)
		print(str(e))

for tik in ticker_list:
	timestamp = time.strftime('%H%M%S')
	print(tik + ' started at ' + str(timestamp))
	getData(tik)
	timestamp = time.strftime('%H%M%S')
	print(tik + ' completed at ' + str(timestamp))
	
print('Backfill of new securities to database complete')
ErrorLog = '\r\n'  + '================================================================================================='

#===============================================
#Add most recent data to the database for all active securities
#===============================================
print('Add most recent data to database begin')
try:
	script = """SELECT
					TICKER
				FROM
					STOCK_DESCRIPTION"""
	crsr.execute(script)
	print(crsr.execute(script))
	columns = [desc[0] for desc in crsr.description]
	data = crsr.fetchall()
	df1 = pd.DataFrame.from_records(data=data,columns=columns)
	ticker_list = ['^GSPC']
	for x in data:
		ticker_list.append(x[0])
	print(ticker_list)
	crsr.close()
except Exception as e:
	print('Query to pull ticker list failed')

#ticker_list = ['GBTC','ETHE']

# We can get data by our choice by giving days bracket
#start_date = datetime.datetime.strptime('2020–01–01','%Y-%m-%d')
#end_date= datetime.date(2020, 6, 26)#'2020–06–26'
#===============================================
#commented below for testing
#files=[]
#commented above for testing
#===============================================


def getData(ticker):
	#print(ticker)cd
	try:
		data = pdr.get_data_yahoo(ticker, start=today-timedelta(21 ), end=today) #18000 in range
		#===============================================
		#commented below for testing
			#dataname= ticker+'_'+str(today)
			#files.append(dataname)
			#SaveData(data, dataname)
		#commented above for testing
		#===============================================
		# Create a data folder in your current dir.
		#===============================================
		#commented below for testing
		# def SaveData(df, filename):
			# df.to_csv('.\SANDPDownload\\'+filename+'.csv')
		#commented above for testing
		#===============================================
		#This loop will iterate over ticker list, will pass one ticker to get data, and save that data as file.
		#print(data)
		#===============================================
		#New code configured from: https://reasonabledeviations.com/2018/02/01/stock-price-database/#database-schema
		#===============================================
		for row in data.itertuples():
			values = list(row)
			#print(values)
			values.append(ticker)
			newval = str(values[0])
			newval = newval.replace(' 00:00:00','')
			newval = newval.replace('-','')
			newval = (values[7] + '_' + newval)
			values.append(newval)
			try:
				crsr.execute("""INSERT INTO dbo.STOCKS (dtDate,decOpen,decHigh,decLow,decClose,decAdjClose,intVol,strTick,ID)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
				tuple(values))
				conn.commit()
			except Exception as e:
				try: 
					miscerr = miscerr + 'error: ' + str(newval) + str(e) + '\r\n'
				except:
					miscerr = 'error: ' + str(newval) + str(e) + '\r\n'
		#===============================================
	except Exception as e:
		ErrorLog = """'""" + str(ticker) + """'""" + ','
		f.write(ErrorLog)
		print(str(e))

for tik in ticker_list:
	timestamp = time.strftime('%H%M%S')
	print(tik + ' started at ' + str(timestamp))
	getData(tik)
	timestamp = time.strftime('%H%M%S')
	print(tik + ' completed at ' + str(timestamp))
	
print('Add most recent data to database complete')
ErrorLog = '\r\n'  + '================================================================================================='

f.write(ErrorLog)
try:
	f.write(miscerr)
except:
	print('No misc errors')
f.close()
print("""Job's done""")
