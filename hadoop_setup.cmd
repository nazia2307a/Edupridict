@echo off
title Hadoop Demo Setup - EduPredict
color 0A
echo.
echo ========================================
echo    🎓 EduPredict - Hadoop DEMO Setup
echo ========================================
echo.

REM Create Hadoop demo folders
echo [1/3] Creating Hadoop demo structure...
mkdir hadoop >nul 2>&1
mkdir data >nul 2>&1
mkdir data\edupredict >nul 2>&1

REM Create core-site.xml (HDFS Demo Config)
echo [2/3] Configuring HDFS (Demo Mode)...
(
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<?xml-stylesheet type="text/xsl" href="configuration.xsl"?^>
echo ^<configuration^>
echo    ^<property^>
echo        ^<name^>fs.defaultFS^</name^>
echo        ^<value^>file:///C:/EduPredict/data^</value^>
echo    ^</property^>
echo ^</configuration^>
) > hadoop\core-site.xml

REM Create hdfs-site.xml
(
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<?xml-stylesheet type="text/xsl" href="configuration.xsl"?^>
echo ^<configuration^>
echo    ^<property^>
echo        ^<name^>dfs.replication^</name^>
echo        ^<value^>1^</value^>
echo    ^</property^>
echo ^</configuration^>
) > hadoop\hdfs-site.xml

REM Create sample data link
echo [3/3] Linking demo data to HDFS...
mklink /D data\edupredict\students.csv "%CD%\data\students.csv" >nul 2>&1

echo.
echo ✅ Hadoop DEMO Setup Complete!
echo 📁 HDFS Path: file:///C:/EduPredict/data/
echo ⚡ PySpark will use LOCAL mode (No real Hadoop needed)
echo.
echo Press any key to continue...
pause >nul