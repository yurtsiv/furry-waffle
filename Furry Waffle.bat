@echo off

echo Initializing Python venv

python3 -m venv env

CALL env/Scripts/activate

echo Installing dependencies

pip3 install -r requirements.txt

echo Starting Transmission daemon

"bin/transmission/transmission-daemon"

python3 src/main.py