from ui.index import run
from transmission_rpc import Client

client = Client(host='localhost', port=9091, username='transmission', password='password')

if __name__ == '__main__':
    run(client)