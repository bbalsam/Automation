#================================================================
#VERSION
#================================================================
#00.00			Orig test of theory
#00.01			Fix for deltaOwned 'New', and '>' replacement and added additional error logging
#00.02			Fix for long strings
#00.03			Fix for force date logic
#================================================================

#===============================================
# importing the libraries
#===============================================
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import pandas as pd
import time
import pyodbc

from datetime import datetime, timedelta
from pandas_datareader import data as pdr
from datetime import date



#===============================================
# Variables
#===============================================
page = 5
rowcount = 1000
url="""http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=0&fdr=&td=0&tdr=&fdlyl=&fdlyh=3&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt="""+str(rowcount)+"""&page="""+str(page)

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, 'lxml')
#print(soup.prettify()) # print the parsed data of html

#print(soup.td())

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
#ODBC connection code: https://reasonabledeviations.com/2018/02/01/stock-price-database/#database-schema
#===============================================
conn = pyodbc.connect(DRIVER='{SQL Server}',SERVER='LAPTOP-D6TKOBQR\SQLEXPRESS',DATABASE='stockdb',Trusted_connection='yes')
crsr = conn.cursor()


#===============================================
# BeautifulSoup variables
#===============================================

insider_table = soup.find('table', attrs={'class': 'tinytable'})

#===============================================
#Code pulls headers, not necessary once table created
#===============================================
# insider_table_data = insider_table.thead.find_all('tr')

# Get all the headings of Lists
# headings = []
# for tr in insider_table_data[0].find_all('th'):
	# remove any newlines and extra spaces from left and right
	# print(str(tr.text))
	# print(tr.text.replace('\xa0','_'))
	# headings.append(tr.text.replace('\xa0','_')) #text..replace('\n', ' ').strip.b
	# print(tr)

# print(headings)
#===============================================
#Code pulls Insider trading data
#===============================================

insider_table_data = insider_table.tbody.find_all('tr')

# Get all the headings of Lists

tdata = []
i=0
p=1
print(rowcount)
f.write('Row count: ' + str(rowcount) + '\r\n')
while p <= page:
	url="""http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=0&fdr=&td=0&tdr=&fdlyl=&fdlyh=3&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt="""+str(rowcount)+"""&page="""+str(p)
	html_content = requests.get(url).text
	soup = BeautifulSoup(html_content, 'lxml')
	insider_table = soup.find('table', attrs={'class': 'tinytable'})
	insider_table_data = insider_table.tbody.find_all('tr')
	while i <= rowcount-1: #one less than cnt in webpage html 'url'
		tdata = []
		for tr in insider_table_data[i].find_all('td'):
			# remove any newlines and extra spaces from left and right
			#print(str(tr.text))
			tdata.append(tr.text.replace('\xa0','_').replace('$','').replace('%','').replace(',','').replace('+','')) #text..replace('\n', ' ').strip.b
		tdata = tdata[:13]
		createid = tdata[1]
		tdata[0] = tdata[0][:8]
		tdata[3] = tdata[3].replace(' ','')[:8]
		tdata[4] = tdata[4][:64]
		tdata[5] = str(tdata[5][:64])
		tdata[6] = tdata[6][:64]
		tdata[7] = tdata[7][:64]
		tdata[11] = tdata[11].replace('New','-1').replace('>','1000')	
		idname = str(tdata[5][:64]).replace(chr(32),'_').replace(chr(33),'').replace(chr(34),'').replace(chr(35),'').replace(chr(36),'').replace(chr(37),'').replace(chr(38),'').replace(chr(39),'').replace(chr(40),'').replace(chr(41),'').replace(chr(42),'').replace(chr(43),'').replace(chr(44),'').replace(chr(45),'').replace(chr(46),'').replace(chr(47),'').replace(chr(91),'').replace(chr(92),'').replace(chr(93),'').replace(chr(94),'').replace(chr(95),'').replace(chr(96),'').upper()		
		id = (createid[:4]+createid[5:7]+createid[8:10]+'_'+createid[11:13]+createid[14:16]+createid[17:19]+'_'+str(tdata[3])+'_'+str(idname))
		tdata.insert(0,id[:64])
		print(tdata[:14])
		#f.write(str(tdata[:14]) + '\r\n')
		try:
			print('start db')
			#f.write('start db' + '\r\n')
			crsr.execute(
			"""
			insert into InsiderPurchases VALUES(
								?
								,?
								,CAST(? as DATETIME)
								,CAST(? as DATE)
								,?
								,?
								,?
								,?
								,?
								,CAST(? as DECIMAL(12,2))
								,CAST(? as DECIMAL(12,2))
								,CAST(? as DECIMAL(12,2))
								,CAST(? as DECIMAL(12,2))
								,CAST(? as DECIMAL(12,2)))
			""",tdata[:14])
			conn.commit()
			print('Page: '+str(p)+' Row: '+str(i)+' WAS SUCCESSFUL - end db')
			#f.write('Page: '+str(p)+' Row: '+str(i)+' WAS SUCCESSFUL - end db' + '\r\n')
		except Exception as e:
				print('Page: '+str(p)+' Row: '+str(i)+' FAILED - end db')
				f.write('start db' + '\r\n')
				f.write(str(tdata[:14]) + '\r\n')
				f.write('Page: '+str(p)+' Row: '+str(i)+' FAILED - end db' + '\r\n' + str(e) + '\r\n')
				i=rowcount
				p=page
		i=i+1
	p = p+1
	i=0
	
#exit()
#===============================================
# OpenInsider download completed
#
# Begin Yahoo download
#===============================================





#================================================================
#Code to allow Yahoo! to recognize API call
#================================================================
yf.pdr_override()



#===============================================
#New code configured from: https://reasonabledeviations.com/2018/02/01/stock-price-database/#database-schema
#===============================================

conn = pyodbc.connect(DRIVER='{SQL Server}',SERVER='LAPTOP-D6TKOBQR\SQLEXPRESS',DATABASE='stockdb',Trusted_connection='yes')
crsr = conn.cursor()

#================================================================
#Code to create list from SQL query
#================================================================


SQL = """
		declare	@forcedate		as	datetime
		set		@forcedate		=	/*CASE
										WHEN CAST(getdate() AS DATE)=(SELECT CAST(MAX(Filing_Date) AS DATE) FROM InsiderPurchases)
										THEN (SELECT LAG(CAST(Filing_Date AS DATE),1) OVER (ORDER BY Filing_Date ASC) FROM InsiderPurchases WHERE Filing_Date = (SELECT MAX(Filing_Date) FROM InsiderPurchases))
										ELSE (SELECT CAST(MAX(Filing_Date) AS DATE) FROM InsiderPurchases)
									END*/--
									(SELECT CAST(max(Filing_Date) AS DATE) FROM InsiderPurchases) --getdate()--
									--(SELECT @forcedate,dtdate,PrevDate FROM (SELECT *,LAG(dtdate,1) OVER (ORDER BY dtdate ASC) as PrevDate FROM TradingDates) td where CAST(@forcedate as date) = td.dtdate)

		declare	@tradedatestart	as	datetime
		declare	@tradedateend	as	datetime

		set		@tradedatestart	=	@forcedate
									--(SELECT dateadd(hh,0,CAST(PrevDate as datetime)) FROM (SELECT *,LAG(dtdate,1) OVER (ORDER BY dtdate ASC) as PrevDate FROM TradingDates) td where CAST(@forcedate as date) = td.dtdate)
		set		@tradedateend	=	DATEADD(DD,1,@forcedate)
									--(SELECT dateadd(hh,0,CAST(dtdate as datetime)) FROM (SELECT *,LAG(dtdate,1) OVER (ORDER BY dtdate ASC) as PrevDate FROM TradingDates) td where CAST(@forcedate as date) = td.dtdate)


		/**/select Ticker--,sum([Value]) as SumVal,Max(Filing_Date) as MaxFDate
		from InsiderPurchases
		where 
			Ticker NOT IN ('..')
			AND Filing_Date	between @tradedatestart and @tradedateend
							--between DATEADD(HOUR,7,CAST(CAST(GETDATE() as DATE) as DATETIME)) and DATEADD(HOUR,7,DATEADD(DAY,1,CAST(CAST(GETDATE() as DATE) as DATETIME)))  /*select DATEADD(HOUR,7,CAST(CAST(GETDATE() as DATE) as DATETIME)),DATEADD(HOUR,7,DATEADD(DAY,1,CAST(CAST(GETDATE() as DATE) as DATETIME)))*/
							--between DATEADD(HOUR,7,DATEADD(DAY,-1,CAST(CAST(GETDATE() as DATE) as DATETIME))) and DATEADD(HOUR,7,CAST(CAST(GETDATE() as DATE) as DATETIME)) /*select DATEADD(HOUR,7,DATEADD(DAY,-1,CAST(CAST(GETDATE() as DATE) as DATETIME))),DATEADD(HOUR,7,CAST(CAST(GETDATE() as DATE) as DATETIME))*/
							/*MONDAY*/--between DATEADD(HOUR,7,DATEADD(DAY,-3,CAST(CAST(GETDATE() as DATE) as DATETIME))) and DATEADD(HOUR,7,CAST(CAST(GETDATE() as DATE) as DATETIME)) /*select DATEADD(HOUR,7,DATEADD(DAY,-1,CAST(CAST(GETDATE() as DATE) as DATETIME))),DATEADD(HOUR,7,CAST(CAST(GETDATE() as DATE) as DATETIME))*/
		GROUP BY Ticker
		ORDER BY Ticker
		"""

crsr.execute(SQL)

result = crsr.fetchall() #result = (1,2,3,) or  result =((1,3),(4,5),)

final_result = []
for i in result:
	#print(str(i).replace('(','').replace(', )',''))
	final_result.append(str(i).replace('(','').replace(', )','').replace("""'""",''))

print(final_result)
f.write('List to download from Yahoo finance: ' + str(final_result) + '\r\n')

ticker_list = final_result

# We can get data by our choice by giving days bracket
#start_date = datetime.datetime.strptime('2020–01–01','%Y-%m-%d')
#end_date= datetime.date(2020, 6, 26)#'2020–06–26'
#===============================================
#commented below for testing
#files=[]
#commented above for testing
#===============================================


def getData(ticker):
	#print(ticker)
	try:
		data = pdr.get_data_yahoo(ticker, start=today-timedelta(10), end=today) #18000 in range
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
			values.append(ticker)
			newval = str(values[0])
			newval = newval.replace(' 00:00:00','')
			newval = newval.replace('-','')
			newval = (values[7] + '_' + newval)
			values.append(newval)
			try:
				crsr.execute("""INSERT INTO InsiderStocks (dtDate,decOpen,decHigh,decLow,decClose,decAdjClose,intVol,strTick,ID)
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
	

ErrorLog = '\r\n'  + '================================================================================================='

f.write(ErrorLog)
try:
	f.write(miscerr)
except:
	print('No misc errors')
f.close()
print("""Job's done""")

