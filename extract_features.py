import re
import whois
import requests
from datetime import date, datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

url_shortening_services = ['7.ly', 'adf.ly', 'admy.link', 'al.ly', 'bc.v', 'bit.do', 'doiop.com', 'fur.ly', 'fave.co', 'is.gd', 'lnked.in', 'lynk.my', 'mcaf.ee', 'ouo.io', 'ow.ly', 'ph.dog', 'qr.net', 's.id', 'shrinkee.com', 'shrinkurl.in', 'sptfy.com', 'thinfi.com', 'tiny.cc', 'tinyurl.com', 'tny.im', 'flic.kr', 'v.gd', 'y2u.be', 'zi.ma', 'zzb.bz', 'adfoc.us', 'bit.ly', 'cur.lv', 'git.io', 'goo.gl', 'hec.su', 'sh.st', 'tldrify.com', 'tr.im']

def check_having_IP_Address(url):
    result = re.search('(?<=\/\/)(([0-9]+x?[A-z0-9]+)\.?)+', url)
    if result:
        return 1
    else:
        return -1

def check_URL_Length(url):
    length = len(url)
    
    if length < 54:
        return -1
    elif length >= 54 and length <= 75:
        return 0
    else:
        return 1

def check_Shortening_Service(url):
    for name in url_shortening_services:
        if name in url:
            return 1
    return -1

def check_having_At_symbol(url):
    if '@' in url:
        return 1
    else:
        return -1

def check_double_slash_redirecting(url):
    ds_count = url.count('//')
    if ds_count > 1:
        return 1
    else:
        return -1

def check_Prefix_Suffix(url):
    result = (re.search('^(.*:)\/\/([A-Za-z0-9\-\.]+)(:[0-9]+)?(.*)$', url))
    res = ''
    if result:
        res = result.group(2)
    if '-' in res:
        return 1
    else:
        return -1

def check_having_Sub_Domain(url):
    result = (re.search('^(.*:)\/\/([A-Za-z0-9\-\.]+)(:[0-9]+)?(.*)$', url))
    res = ''
    if result:
        res = result.group(2)
    
    if 'www.' in res:
        res = res[4:]
    
    dot_count = res.count('.')
    if dot_count == 1:
        return -1
    elif dot_count == 2:
        return 0
    else:
        return 1

def check_SSLfinal_State(url):
    return 0

def check_Domain_registration_length(url):
    w = whois.whois(url)
    expires = w.expiration_date
    if isinstance(expires, list):
        expires = expires[0]
    today = datetime.today()
    delta = expires - today
    print(delta)
    if delta.days <= 365:
        return 1
    else:
        return -1

def check_Favicon(url):
    """
    domain = 'http://' + urlparse(url).netloc
    page = requests.get(domain)
    soup = BeautifulSoup(page.text, features="lxml")
    icon_link = soup.find("link", rel="shortcut icon")
    if icon_link is None:
        icon_link = soup.find("link", rel="icon")
    if icon_link is None:
        return domain + '/favicon.ico'
    icon = icon_link["href"]
    print(icon)
    """
    return 0

def check_port(url):
    return 0

def check_HTTPS_token(url):
    result = (re.search('^(.*:)\/\/([A-Za-z0-9\-\.]+)(:[0-9]+)?(.*)$', url))
    res = ''
    if result:
        res = result.group(2)
    
    if 'https' in res:
        return 1
    else:
        return 0

def check_Request_URL(url):
    return 0

def check_URL_of_Anchor(url):
    return 0

def check_Links_in_tags(url):
    return 0

def check_SFH(url):
    return 0

def check_Submitting_to_email(url):
    return 0

def check_Abnormal_URL(url):
    return 0

def check_Redirect(url):
    return 0

def check_on_mouseover(url):
    return 0

def check_RightClick(url):
    return 0

def check_popUpWindow(url):
    return 0

def check_Iframe(url):
    return 0

def check_age_of_domain(url):
    return 0

def check_DNSRecord(url):
    return 0

def check_web_traffic(url):
    return 0

def check_Page_Rank(url):
    return 0

def check_Google_Index(url):
    return 0

def check_Links_pointing_to_page(url):
    return 0

def check_Statistical_report(url):
    return 0


