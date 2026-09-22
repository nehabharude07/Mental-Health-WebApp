@echo off
REM Windows par app chalane ke liye - double click karein
call env1\Scripts\activate.bat
python train_model.py
python app.py
pause
