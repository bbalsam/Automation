'==============================================================================================
'Declare Variables
'==============================================================================================
dim accessApp
dim fromdate
dim todate
dim sleepAmt
dim WshShell
dim BtnCode
dim cmd
dim PyLoc
dim i
dim EOM1W
dim LDOTM
dim CD25PBD

'==============================================================================================
'Start Loop
'==============================================================================================
While x < 10


'==============================================================================================
'Set Variables
'==============================================================================================

Set wshShell = CreateObject("WScript.Shell")
PyLoc = """C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe""" 'UNJ1LDJBNTF2
'PyLoc = """C:\Users\balsambr\AppData\Local\Programs\Python\Python37-32\python.exe""" 'GLNVMWKSTN28

fromdate = Date
'fromdate = #08/11/2022#  'To run for a manual date, uncomment this line and set the date 1 business day prior to the date you need to have run.
'==============================================================================================
'Set Variables
'==============================================================================================
'Busday = 0
todate = DateSerial(Year(fromdate), Month(fromdate), 1)
Select Case Weekday(todate)
	Case 1,7
		Busday = 0
	Case 2,3,4,5,6
		Busday = 1
End Select


'==============================================================================================
'Dictionary of holidays:  2 fields, date, and number of days to next business day.
'==============================================================================================

Dim holidays
Set holidays = CreateObject("Scripting.Dictionary")
holidays.Add  DateSerial(2021, 1, 1),3 'New Years
holidays.Add  DateSerial(2021, 12, 24),3 'Christmas
holidays.Add  DateSerial(2021, 12, 31),3 'New Years
holidays.Add  DateSerial(2022, 1, 17),1 'MLK Jr Day
holidays.Add  DateSerial(2022, 5, 30),1 'Memorial Day
holidays.Add  DateSerial(2022, 7, 4),1 'Independence Day
holidays.Add  DateSerial(2022, 9, 5),1 'Labor Day
holidays.Add  DateSerial(2022, 11, 24),4 'Thanksgiving
holidays.Add  DateSerial(2022, 11, 25),3 'Thanksgiving (day after)
holidays.Add  DateSerial(2022, 12, 26),1 'Christmas


'==============================================================================================
'Set Business day logic
'==============================================================================================

While todate <= fromdate

	Select Case Weekday(todate)
	Case 6
		todate = DateSerial(Year(todate), Month(todate), Day(todate)+3)
	Case 7
		todate = DateSerial(Year(todate), Month(todate), Day(todate)+2)
	Case 1,2,3,4,5
		todate = DateSerial(Year(todate), Month(todate), Day(todate)+1)
	End Select
	
	Busday = Busday + 1
	
	If holidays.Item(todate) <> "" Then
		todate = DateSerial(Year(todate), Month(todate), Day(todate)+holidays.Item(todate))
	End If
	
	If DatePart("m",todate) <> DatePart("m",fromdate) Then
		Busday = 1
	End If
	
	' MsgBox("Next scheduled date is: " + CStr(todate)+vbCrLf+"Next business date is: " + CStr(Busday))
Wend


If holidays.Item(todate) <> "" Then
		todate = DateSerial(Year(todate), Month(fromdate), Day(todate)+holidays.Item(todate))
	End If

calday = datepart("d",todate)
todate = todate + TimeSerial(04,00,00)


'==============================================================================================
'Set Variables - Set sleep timer
'==============================================================================================
sleepAmt = DateDiff("s",Now,todate)

'==============================================================================================
'Notification with time delay for scheduled execution
'==============================================================================================
BtnCode = WshShell.Popup("Data scripts scheduled to run at:"+vbCrLf+Cstr(todate)+vbCrLf+vbCrLf+"To BYPASS schedule, and run IMMEDIATELY, click 'OK'"+vbCrLf+vbCrLf+"To stop and exit, click 'Cancel'", sleepAmt, "REPORT Automation", 1+64)
Select Case BtnCode
Case -1
Case 1
	Wscript.Echo "The script will now start.  Press 'OK' to continue."
Case 2
	Wscript.Echo "The program will now exit!"
    Wscript.Quit
End Select
'==============================================================================================
'Set up Access to prepare for running jobs
'==============================================================================================
' accessApp.OpenCurrentDataBase "\\corp.ocwen.com\data\laxa\prod\Common\Port\SMART\SMART.mdb"
' accessApp.visible = true
' accessApp.UserControl = true


'==============================================================================================
'Run Jobs - DAILY JOBS
'==============================================================================================
	cmd = PyLoc + " " + """C:\Users\brett\Documents\GitHub\Automation\CharlesSchwab.py"""
	wshShell.Run cmd
	WScript.Sleep(60000)
	cmd = PyLoc + " " + """C:\Users\brett\Documents\GitHub\Automation\YahooDownload_PROD_NEW_02.py"""
	wshShell.Run cmd
	WScript.Sleep(2000)


'==============================================================================================
'End Loop  - Loop is designed to run endlessly.  Click cancel on popup to exit program.
'==============================================================================================
Wend