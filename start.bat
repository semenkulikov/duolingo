@echo off
color a


for /l %%x in (1, 1, 5) do (
	start activ.bat & ping -n 1 -w 5000 192.168.254.254 >nul
)
pause
exit