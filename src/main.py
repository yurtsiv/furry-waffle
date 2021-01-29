import os
from ui.index import run
from transmission_rpc import Client

def start():
    print('Connecting to Transmission daemon')
    client = Client(host='localhost', port=9091, username='transmission', password='password')
    print('Connected. Starting the UI')
    run(client)

if __name__ == '__main__':
    try:
        print('Starting Transmission daemon')
        os.system('START /B "" bin/transmission/transmission-daemon --foreground --port 9091 --logfile logs.txt &')
        start()
    except Exception as e:
        print(e)