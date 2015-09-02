@ECHO OFF

SET PYTHONPATH="C:\Python27\"
SET PYPELYNEPATH=%~dp0

cd %PYPELYNEPATH%

%PYTHONPATH%python pypelyne_client.py %*