import socket
import requests

def isPortOpen(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((host, port))
        sock.shutdown(socket.SHUT_RDWR)
        return 1
    except:
        return 0
    finally:
        sock.close()

def get_request(url):
    try:
        req = requests.get(url)
        return req
    except:
        return None
