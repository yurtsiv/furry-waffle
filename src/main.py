from ui.index import run
from transmission_rpc import Client

if __name__ == '__main__':
    try:
        client = Client(host='localhost', port=9091, username='transmission', password='password')
        run(client)
    except Exception as e:
        print(e)