@echo off
:: FSociety Database Management Utility
:: Created by Asero
:: This script provides a menu-driven interface to manage the FSociety database

:menu
cls
echo.
echo  ███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗
echo  ██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
echo  █████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝ 
echo  ██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝  
echo  ██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║   
echo  ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝   
echo.
echo               DATABASE MANAGEMENT CONSOLE
echo.
echo  Created by Asero                      %date% %time%
echo =================================================================
echo.
echo  1. View Database Statistics
echo  2. Backup Database
echo  3. Restore Database
echo  4. Export Data to CSV
echo  5. Database Maintenance
echo  6. CLI Tools
echo  0. Exit
echo.
echo =================================================================

set /p choice=Enter your choice (0-6): 

if "%choice%"=="1" goto stats
if "%choice%"=="2" goto backup
if "%choice%"=="3" goto restore
if "%choice%"=="4" goto export
if "%choice%"=="5" goto maintenance
if "%choice%"=="6" goto cli
if "%choice%"=="0" goto exit
goto menu

:stats
cls
echo =================================================================
echo                   DATABASE STATISTICS
echo =================================================================
echo.
py db_stats.py --display --database instance/fsociety.db
echo.
echo =================================================================
echo  1. Save statistics report
echo  2. Return to main menu
echo =================================================================

set /p stats_choice=Enter choice: 

if "%stats_choice%"=="1" (
    py db_stats.py --database instance/fsociety.db --output-dir reports
    echo.
    echo Report saved to reports directory
    pause
)
goto menu

:backup
cls
echo =================================================================
echo                    DATABASE BACKUP
echo =================================================================
echo.
echo  1. Create a new backup
echo  2. List available backups
echo  3. Return to main menu
echo =================================================================

set /p backup_choice=Enter choice: 

if "%backup_choice%"=="1" (
    py db_backup.py backup --source instance/fsociety.db --backup-dir backups
    echo.
    pause
    goto backup
)
if "%backup_choice%"=="2" (
    py db_backup.py list --backup-dir backups
    echo.
    pause
    goto backup
)
goto menu

:restore
cls
echo =================================================================
echo                   DATABASE RESTORE
echo =================================================================
echo.
py db_backup.py list --backup-dir backups
echo.
echo =================================================================
echo Enter the name of the backup file to restore or 'back' to return
echo =================================================================

set /p restore_file=Backup file: 

if "%restore_file%"=="back" goto menu
if "%restore_file%"=="" goto restore

py db_backup.py restore backups/%restore_file% --target instance/fsociety.db
echo.
pause
goto menu

:export
cls
echo =================================================================
echo                    DATA EXPORT
echo =================================================================
echo.
echo  1. Export all tables
echo  2. Export recruits table
echo  3. Export contacts table
echo  4. Return to main menu
echo =================================================================

set /p export_choice=Enter choice: 

if "%export_choice%"=="1" (
    py db_export.py --database instance/fsociety.db --output-dir exports
    echo.
    pause
    goto export
)
if "%export_choice%"=="2" (
    py db_export.py --database instance/fsociety.db --output-dir exports --table recruit
    echo.
    pause
    goto export
)
if "%export_choice%"=="3" (
    py db_export.py --database instance/fsociety.db --output-dir exports --table contact
    echo.
    pause
    goto export
)
goto menu

:maintenance
cls
echo =================================================================
echo                  DATABASE MAINTENANCE
echo =================================================================
echo.
echo  1. Run full maintenance
echo  2. Check database size
echo  3. Optimize database (VACUUM)
echo  4. Purge old rejected recruits (30+ days)
echo  5. Return to main menu
echo =================================================================

set /p maint_choice=Enter choice: 

if "%maint_choice%"=="1" (
    py db_maintenance.py full --database instance/fsociety.db
    echo.
    pause
    goto maintenance
)
if "%maint_choice%"=="2" (
    py db_maintenance.py size --database instance/fsociety.db
    echo.
    pause
    goto maintenance
)
if "%maint_choice%"=="3" (
    py db_maintenance.py vacuum --database instance/fsociety.db
    echo.
    pause
    goto maintenance
)
if "%maint_choice%"=="4" (
    py db_maintenance.py purge --database instance/fsociety.db --table recruit --days 30 --status rejected
    echo.
    pause
    goto maintenance
)
goto menu

:cli
cls
echo =================================================================
echo                      CLI TOOLS
echo =================================================================
echo.
echo  1. Database CLI (db_cli.py)
echo  2. Return to main menu
echo =================================================================

set /p cli_choice=Enter choice: 

if "%cli_choice%"=="1" (
    echo.
    echo Available commands:
    echo   py db_cli.py stats
    echo   py db_cli.py export --days 7
    echo   py db_cli.py backup
    echo   py db_cli.py purge --days 30
    echo   py db_cli.py find_recruit [handle]
    echo   py db_cli.py update_status [id] [status]
    echo.
    cmd /k
)
goto menu

:exit
echo.
echo Exiting FSociety Database Management Console...
echo.
exit /b 0
