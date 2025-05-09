# FSociety Database Management Console
# Created by Asero
# PowerShell script for database management

function Show-Menu {
    Clear-Host
    Write-Host "`n  ███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗" -ForegroundColor Red
    Write-Host "  ██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝" -ForegroundColor Red
    Write-Host "  █████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝ " -ForegroundColor Red
    Write-Host "  ██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝  " -ForegroundColor Red
    Write-Host "  ██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║   " -ForegroundColor Red
    Write-Host "  ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝   " -ForegroundColor Red
    Write-Host "`n               DATABASE MANAGEMENT CONSOLE" -ForegroundColor Cyan
    Write-Host "`n  Created by Asero                      $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "`n  1. View Database Statistics"
    Write-Host "  2. Backup Database"
    Write-Host "  3. Restore Database"
    Write-Host "  4. Export Data to CSV"
    Write-Host "  5. Database Maintenance"
    Write-Host "  6. CLI Tools"
    Write-Host "  0. Exit"
    Write-Host "`n=================================================================" -ForegroundColor DarkGray
}

function Show-Stats {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "                   DATABASE STATISTICS" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host ""
    python db_stats.py --display --database instance/fsociety.db
    Write-Host ""
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "  1. Save statistics report"
    Write-Host "  2. Return to main menu"
    Write-Host "=================================================================" -ForegroundColor DarkGray
    
    $choice = Read-Host "Enter choice"
    
    switch ($choice) {
        "1" {
            python db_stats.py --database instance/fsociety.db --output-dir reports
            Write-Host "`nReport saved to reports directory" -ForegroundColor Green
            Read-Host "Press Enter to continue"
        }
    }
}

function Show-Backup {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "                    DATABASE BACKUP" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  1. Create a new backup"
    Write-Host "  2. List available backups"
    Write-Host "  3. Return to main menu"
    Write-Host "=================================================================" -ForegroundColor DarkGray
    
    $choice = Read-Host "Enter choice"
    
    switch ($choice) {
        "1" {
            python db_backup.py backup --source instance/fsociety.db --backup-dir backups
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Backup
        }
        "2" {
            python db_backup.py list --backup-dir backups
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Backup
        }
    }
}

function Show-Restore {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "                   DATABASE RESTORE" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host ""
    python db_backup.py list --backup-dir backups
    Write-Host ""
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "Enter the name of the backup file to restore or 'back' to return"
    Write-Host "=================================================================" -ForegroundColor DarkGray
    
    $restore_file = Read-Host "Backup file"
    
    if ($restore_file -eq "" -or $restore_file -eq "back") {
        return
    }
    
    python db_backup.py restore "backups/$restore_file" --target instance/fsociety.db
    Write-Host ""
    Read-Host "Press Enter to continue"
}

function Show-Export {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "                    DATA EXPORT" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  1. Export all tables"
    Write-Host "  2. Export recruits table"
    Write-Host "  3. Export contacts table"
    Write-Host "  4. Return to main menu"
    Write-Host "=================================================================" -ForegroundColor DarkGray
    
    $choice = Read-Host "Enter choice"
    
    switch ($choice) {
        "1" {
            python db_export.py --database instance/fsociety.db --output-dir exports
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Export
        }
        "2" {
            python db_export.py --database instance/fsociety.db --output-dir exports --table recruit
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Export
        }
        "3" {
            python db_export.py --database instance/fsociety.db --output-dir exports --table contact
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Export
        }
    }
}

function Show-Maintenance {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "                  DATABASE MAINTENANCE" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  1. Run full maintenance"
    Write-Host "  2. Check database size"
    Write-Host "  3. Optimize database (VACUUM)"
    Write-Host "  4. Purge old rejected recruits (30+ days)"
    Write-Host "  5. Return to main menu"
    Write-Host "=================================================================" -ForegroundColor DarkGray
    
    $choice = Read-Host "Enter choice"
    
    switch ($choice) {
        "1" {
            python db_maintenance.py full --database instance/fsociety.db
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Maintenance
        }
        "2" {
            python db_maintenance.py size --database instance/fsociety.db
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Maintenance
        }
        "3" {
            python db_maintenance.py vacuum --database instance/fsociety.db
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Maintenance
        }
        "4" {
            python db_maintenance.py purge --database instance/fsociety.db --table recruit --days 30 --status rejected
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Maintenance
        }
    }
}

function Show-CLI {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host "                      CLI TOOLS" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  1. Database CLI (db_cli.py)"
    Write-Host "  2. Return to main menu"
    Write-Host "=================================================================" -ForegroundColor DarkGray
    
    $choice = Read-Host "Enter choice"
    
    if ($choice -eq "1") {
        Write-Host ""
        Write-Host "Available commands:" -ForegroundColor Yellow
        Write-Host "  python db_cli.py stats"
        Write-Host "  python db_cli.py export --days 7"
        Write-Host "  python db_cli.py backup"
        Write-Host "  python db_cli.py purge --days 30"
        Write-Host "  python db_cli.py find_recruit [handle]"
        Write-Host "  python db_cli.py update_status [id] [status]"
        Write-Host ""
        
        $command = Read-Host "Enter command (or 'exit' to return)"
        
        if ($command -ne "exit") {
            Invoke-Expression $command
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-CLI
        }
    }
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Enter your choice (0-6)"
    
    switch ($choice) {
        "1" { Show-Stats }
        "2" { Show-Backup }
        "3" { Show-Restore }
        "4" { Show-Export }
        "5" { Show-Maintenance }
        "6" { Show-CLI }
        "0" { 
            Write-Host "`nExiting FSociety Database Management Console..." -ForegroundColor Red
            Write-Host ""
            exit 
        }
    }
} while ($true)
