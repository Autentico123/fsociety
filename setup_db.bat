@echo off
echo FSociety Database Setup
echo Created by Asero
echo.

echo Installing required packages...
py -m pip install -r requirements.txt
echo.

echo Setting up the database...
py -c "from app import app; from models import db; app.app_context().push(); db.create_all()"
echo.

echo Installing Click for the CLI tool...
py -m pip install click
echo.

echo Setup complete!
echo You can now run the database CLI with: py db_cli.py
echo Or start the application with: py -m flask run
echo.

pause
