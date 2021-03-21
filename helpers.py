import socket
import requests

async def isPortOpen(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        await sock.connect((host, port))
        sock.shutdown(socket.SHUT_RDWR)
        return 1
    except:
        return 0
    finally:
        sock.close()

def get_request(url):
    try:
        req = requests.get(url, timeout=3)
        return req
    except:
        return None
