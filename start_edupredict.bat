@echo off
echo ========================================
echo    EduPredict - AI Education Analytics
echo ========================================
echo.

echo [1/5] Installing dependencies...
pip install -r requirements.txt > nul 2>&1

echo [2/5] Setting up Hadoop (Single Node)...
call hadoop_setup.cmd > nul 2>&1

echo [3/5] Generating sample education data...
python data_generator.py > nul 2>&1

echo [4/5] Starting EduPredict Dashboard...
echo.
echo ========================================
echo Dashboard running at: http://localhost:5000
echo ========================================
python edupredict_app.py

pause