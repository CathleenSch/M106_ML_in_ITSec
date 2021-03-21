import socket
import requests

# einen Port ueberpruefen und 1 zurueckgeben, wenn er offen ist
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

# einen HTTP-Request absetzen und das Result-Objekt zurückgeben
def get_request(url):
    try:
        res = requests.get(url, timeout=3)
        return res
    except:
        return None

