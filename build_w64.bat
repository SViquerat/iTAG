@echo off
echo building project....
c:\python271_64\python.exe build_setup_w64.py build > build_MSG.txt
echo "Remember to rename build directory and compress -> autoextract!"
pause