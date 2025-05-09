@echo off
:: FSociety Database Scheduled Backup
:: Created by Asero
:: This batch file can be scheduled to run regularly for automatic backups

echo FSociety Database Backup - %date% %time%
echo.

:: Change to the script directory
cd /d %~dp0

:: Create automatic backup and rotate old backups
py db_backup.py auto --max 10

echo.
echo Backup completed at %time%
