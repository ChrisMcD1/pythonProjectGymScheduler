Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "C:\Users\camcd\PycharmProjects\pythonProject\ScheduleScript.bat" & Chr(34), 0
Set WinScriptHost = Nothing