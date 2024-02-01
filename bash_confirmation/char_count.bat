@echo off
for /f %%A in ('powershell -Command "(Get-Content test.txt -Raw | Out-String).Length"') do set count=%%A
echo Character count: %count%
