@echo off
cd /d "C:\Library_Management\library_Mgt_BBHC"
call venv\Scripts\activate.bat
python app.py >> log.txt 2>&1
