@echo off
setlocal
cd /d "%~dp0"
set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%PY%" (
  "%PY%" "%~dp0ekspor_html.py"
) else (
  py -3 "%~dp0ekspor_html.py"
)
if errorlevel 1 (
  echo.
  echo Ekspor gagal. Baca pesan di atas. Jangan unggah paket yang belum selesai.
) else (
  echo.
  echo Selesai. Unggah ZIP SATRIA-DomaiNesia-Siap-Upload.zip yang baru ke hosting.
)
pause
