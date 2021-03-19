import re
import bs4
import whois
import requests
from helpers import *
from datetime import date, datetime
from urllib import parse
from bs4 import BeautifulSoup


def check_having_IP_Address(url):
    print('checking for IP address')
    result = re.search('(?<=\/\/)(([0-9]+x?[A-z0-9]+)\.?)+', url)
    if result:
        return 1
    else:
        return -1

def check_URL_Length(url):
    print('checking url length')
    length = len(url)
    
    if length < 54:
        return -1
    elif length >= 54 and length <= 75:
        return 0
    else:
        return 1

def check_Shortening_Service(url):
    url_shortening_services = ['7.ly', 'adf.ly', 'admy.link', 'al.ly', 'bc.v', 'bit.do', 'doiop.com', 'fur.ly', 'fave.co', 'is.gd', 'lnked.in', 'lynk.my', 'mcaf.ee', 'ouo.io', 'ow.ly', 'ph.dog', 'qr.net', 's.id', 'shrinkee.com', 'shrinkurl.in', 'sptfy.com', 'thinfi.com', 'tiny.cc', 'tinyurl.com', 'tny.im', 'flic.kr', 'v.gd', 'y2u.be', 'zi.ma', 'zzb.bz', 'adfoc.us', 'bit.ly', 'cur.lv', 'git.io', 'goo.gl', 'hec.su', 'sh.st', 'tldrify.com', 'tr.im']

    print('checking for shortening service')
    for name in url_shortening_services:
        if name in url:
            return 1
    return -1

def check_having_At_symbol(url):
    print('checking for @ in url')
    if '@' in url:
        return 1
    else:
        return -1

def check_double_slash_redirecting(url):
    print('checking for // redirect')
    ds_count = url.count('//')
    if ds_count > 1:
        return 1
    else:
        return -1

def check_Prefix_Suffix(url):
    print('checking for prefix/ suffix')
    result = (re.search('^(.*:)\/\/([A-Za-z0-9\-\.]+)(:[0-9]+)?(.*)$', url))
    res = ''
    if result:
        res = result.group(2)
    if '-' in res:
        return 1
    else:
        return -1

def check_having_Sub_Domain(url):
    print('checking for subdomain')
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

def check_SSLfinal_State(url): # TODO
    print('checking for SSL state')
    return 0

def check_Domain_registration_length(url):
    print('checking for domain registration length')
    try:
        w = whois.whois(url)
        expires = w.expiration_date
        if isinstance(expires, list):
            expires = expires[0]
        today = datetime.today()
        delta = expires - today
        if delta.days <= 365:
            return 1
        else:
            return -1
    except:
        return -2

def check_Favicon(url): # TODO
    print('checking favicon')
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
    print('checking for open ports')
    ports = [21, 22, 23, 445, 1433, 1521, 3306, 3389]
    ports_open = []
    try:
        host = whois.whois(url).domain_name
        for port in ports:
            ports_open.append(isPortOpen(host, port))
        
        if 1 in ports_open:
            ret = 1
        else:
            ret = -1
    except:
        ret = -2

    return ret

def check_HTTPS_token(url):
    print('checking for http/s in domain')
    result = (re.search('^(.*:)\/\/([A-Za-z0-9\-\.]+)(:[0-9]+)?(.*)$', url))
    res = ''
    if result:
        res = result.group(2)
    
    if 'https' in res:
        return 1
    else:
        return 0

def check_Request_URL(url, res):
    print('checking for external urls')
    hostname = parse.urlparse(url).hostname
    html = res.text
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    link_count = len(links)
    mal_link_sum = 0
    if link_count > 0:
        for link in links:
            link = link[0]
            link_hostname = parse.urlparse(link).hostname
            if link_hostname != hostname:
                mal_link_sum += 1
        percentage = mal_link_sum * 100 / link_count
        if percentage < 22:
            return -1
        elif percentage >= 22 and percentage <= 61:
            return 0
        else:
            return 1
    else:
        return -1

def check_URL_of_Anchor(url, res):
    print('checking anchor tags')
    hostname = parse.urlparse(url).hostname
    html = res.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    a_tags_count = len(a_tags)
    mal_tags_sum = 0
    if a_tags_count > 0:
        for tag in a_tags:
            link = tag.get('href')
            if link:
                if link.startswith('http'):
                    link_hostname = parse.urlparse(link).hostname
                    if link_hostname != hostname:
                        mal_tags_sum += 1
                elif link.startswith('#') or link.startswith('#content') or link.startswith('#skip') or link.startswith('JavaScript ::void(0)'):
                        mal_tags_sum += 1
                else:
                    continue
    else:
        return -1

    percentage = mal_tags_sum * 100 / a_tags_count
    if percentage < 31:
        return -1
    elif percentage >= 31 and percentage <= 67:
        return 0
    else:
        return 1

def check_Links_in_tags(url, res):
    print('checking links in tags')
    hostname = parse.urlparse(url).hostname
    html = res.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    meta_tags = soup.find_all('meta') # content
    script_tags = soup.find_all('script') # src
    link_tags = soup.find_all('link') # href

    tags_count = len(meta_tags) + len(meta_tags) + len(link_tags)
    mal_tags_sum = 0
    if tags_count > 0:
        for tag_type in (meta_tags, script_tags, link_tags):
            for tag in tag_type:
                link1 = tag.get('href')
                link2 = tag.get('src')
                link3 = tag.get('content')

                for link in (link1, link2, link3):
                    if link and link.startswith('http'):
                        link_hostname = parse.urlparse(link1)
                        if link_hostname != hostname:
                            mal_tags_sum += 1
        
        percentage = mal_tags_sum * 100 / tags_count
        if percentage < 17:
            return -1
        elif percentage >= 17 and percentage <= 81:
            return 0
        else:
            return 1
    else:
        return -1

def check_SFH(url):
    return 0

def check_Submitting_to_email(url):
    return 0

def check_Abnormal_URL(url):
    return 0

def check_Redirect(res):
    print('checking for redirects')
    redirects = len(res.history)
    if redirects <= 1:
        return 1
    elif redirects >= 2 and redirects < 4:
        return 0
    else:
        return -1

def check_on_mouseover(url, res):
    print('checking for status bar change onMouseover')
    html = res.text
    if 'onmouseover="window.status=' in html:
        return 1
    else:
        return -1

def check_RightClick(url, res):
    print('checking for right click prevention')
    html = res.text
    print(html)
    if 'event.button==2' in html:
        print('yes')
        return 1
    else:
        print('no')
        return -1

def check_popUpWindow(url):
    return 0

def check_Iframe(url, res):
    print('checking for iframes with external content')
    hostname = parse.urlparse(url).hostname
    html = res.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    iframes = soup.findAll('iframe')
    malicious_iframes_found = 0
    for iframe in iframes:
        link = iframe.get('src')
        if link and link.startswith('http'):
            link_hostname = parse.urlparse(link)
            if link_hostname != hostname:
                malicious_iframes_found = 1
    
    if malicious_iframes_found == 1:
        return 1
    else:
        return -1

def check_age_of_domain(url):
    print('checking for domain age\n')
    try:
        w = whois.whois(url)
        created = w.creation_date
        if isinstance(created, list):
            created = created[0]
        today = datetime.today()
        delta = today - created
        months = delta.days / 30
        if months <= 6:
            return 1
        else:
            return -1
    except:
        return -2

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

check_RightClick('http://www.google.com')