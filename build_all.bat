@echo off
echo building project....
c:\python27\python.exe build_setup_w32.py build > build_MSG32.txt
c:\python27_x64\python.exe build_setup_w64.py build > build_MSG64.txt
echo "Remember to rename build directory and compress -> autoextract!"
pause