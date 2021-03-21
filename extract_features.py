import re
import bs4
import asyncio
from helpers import *
from datetime import date, datetime
from urllib import parse
from bs4 import BeautifulSoup


def check_having_IP_Address(url):
    print('checking for IP address')
    # Regulaerer Ausdruck fuer IP-Adresse als Zahlen oder Hexcode
    result = re.search('(?<=\/\/)(([0-9]+x?[A-z0-9]+)\.?)+', url)
    if result:
        return 1
    else:
        return -1

def check_URL_Length(url):
    print('checking url length')
    # Laenge der URL pruefen
    length = len(url)
    if length < 54:
        return -1
    elif length >= 54 and length <= 75:
        return 0
    else:
        return 1

def check_Shortening_Service(url):
    # Liste von haeufig genutzten URL-Verkuerzungsservices
    url_shortening_services = ['7.ly', 'adf.ly', 'admy.link', 'al.ly', 'bc.v', 'bit.do', 'doiop.com', 'fur.ly', 'fave.co', 'is.gd', 'lnked.in', 'lynk.my', 'mcaf.ee', 'ouo.io', 'ow.ly', 'ph.dog', 'qr.net', 's.id', 'shrinkee.com', 'shrinkurl.in', 'sptfy.com', 'thinfi.com', 'tiny.cc', 'tinyurl.com', 'tny.im', 'flic.kr', 'v.gd', 'y2u.be', 'zi.ma', 'zzb.bz', 'adfoc.us', 'bit.ly', 'cur.lv', 'git.io', 'goo.gl', 'hec.su', 'sh.st', 'tldrify.com', 'tr.im']

    print('checking for shortening service')
    # pruefen, ob Verkuerzungsservice-Domain in URL vorkommt
    for name in url_shortening_services:
        if name in url:
            return 1
    return -1

def check_having_At_symbol(url):
    print('checking for @ in url')
    # URL auf @ pruefen
    if '@' in url:
        return 1
    else:
        return -1

def check_double_slash_redirecting(url):
    print('checking for // redirect')
    # pruefen, ob mehr als einmal '//' in URL enthalten ist (also ueber http:// hinaus)
    ds_count = url.count('//')
    if ds_count > 1:
        return 1
    else:
        return -1

def check_Prefix_Suffix(url):
    print('checking for prefix/ suffix')
    # URL parsen und pruefen, ob '-' enthalten ist 
    hostname = parse.urlparse(url).hostname
    if '-' in hostname:
        return 1
    else:
        return -1

def check_having_Sub_Domain(url):
    print('checking for subdomain')
    # URL parsen
    hostname = parse.urlparse(url).hostname
    if 'www.' in hostname:
        hostname = hostname[4:]
    
    # Punkte in Domain zaehlen
    dot_count = hostname.count('.')
    if dot_count == 1:
        return -1
    elif dot_count == 2:
        return 0
    else:
        return 1

def check_SSLfinal_State(url):
    print('checking for SSL state')
    return 0

def check_Domain_registration_length(w):
    print('checking for domain registration length')
    try:
        expires = w.expiration_date
        # erstes Ergebnis aus der Liste von Ablaufdaten nehmen
        if isinstance(expires, list):
            expires = expires[0]
        
        # berechnen, in wie vielen Tagen die Domain auslaeuft
        today = datetime.today()
        delta = expires - today
        if delta.days <= 365:
            return 1
        else:
            return -1
    except:
        print('skipping')
        return 'skip'

def check_Favicon(url, res):
    print('checking favicon')
    # Domainnamen aus URL parsen
    hostname = parse.urlparse(url).hostname
    # HTML verarbeiten
    html = res.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    icon_link = None
    # typische Namen fuer Favicon in HTML
    icon_names = ['shortcut icon', 'icon', 'Icon']
    i = 0
    # pruefen, ob einer dieser Namen im HTML zu finden ist
    while icon_link == None and i < 3:
        icon_link = soup.find('link', rel=icon_names[i])
        i += 1
    
    if icon_link == None:
        return -1
    else:
        try:
            # Link parsen und mit Domain vergleichen
            icon = icon_link['href']
            icon_hostname = parse.urlparse(icon).hostname
            if icon_hostname == hostname:
                return -1
            else:
                return 1
        except:
            print('skipping')
            return 'skip'

async def check_port(url):
    print('checking for open ports')
    # Liste zu ueberpruefender Ports
    ports = [21, 22, 23, 445, 1433, 1521, 3306, 3389]
    try:
        # Anfragen fuer alle Ports gleichzeitig asynchron schicken (an ausgelagerte Funktion in helpers.py)
        host = parse.urlparse(url).hostname
        open_ports = await asyncio.gather(*(isPortOpen(host, port) for port in ports))        
        if 1 in open_ports:
            ret = 1
        else:
            ret = -1
    except:
        ret = -2

    return ret

def check_HTTPS_token(url):
    print('checking for http/s in domain')
    # URL parsen und pruefen, ob http(s) in Domain vorkommt
    hostname = parse.urlparse(url).hostname
    if 'https' in hostname or 'http' in hostname:
        return 1
    else:
        return 0

def check_Request_URL(url, res):
    print('checking for external urls')
    hostname = parse.urlparse(url).hostname
    # HTML verarbeiten
    html = res.text
    # alle Links in HTML finden
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    link_count = len(links)
    mal_link_sum = 0
    # jeden Link auf Domain ueberpruefen und prozentualen Anteil der externen Domains berechnen
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
    # HTML verarbeiten
    html = res.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # alle Anchortags finden ('<a>)
    a_tags = soup.find_all('a')
    a_tags_count = len(a_tags)
    mal_tags_sum = 0
    # fuer jeden Tag pruefen, ob Link oder anderer bestimmter String enthalten ist, dann Domain pruefen
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

    # prozentualen Anteil verdaechtiger Tags berechnen
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
    # HTML verarbeiten
    html = res.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # alle relevanten Tags finden
    meta_tags = soup.find_all('meta')
    script_tags = soup.find_all('script')
    link_tags = soup.find_all('link')

    tags_count = len(meta_tags) + len(meta_tags) + len(link_tags)
    mal_tags_sum = 0
    
    # ueber gefundene Tags iterieren und auf Attribute ueberpruefen, die URLs enthalten koennen
    # dann Domain pruefen
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
        
        # prozentualen Anteil verdaechtiger Tags berechnen
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
    # History des HTTP-Requests auf ihre Laenge pruefen (>1: redirect)
    redirects = len(res.history)
    if redirects <= 1:
        return -1
    elif redirects >= 2 and redirects < 4:
        return 0
    else:
        return 1

def check_on_mouseover(url, res):
    print('checking for status bar change onMouseover')
    # HTML verarbeiten und auf onMouseOver-Event pruefen, das die Statusbar aendert
    html = res.text
    if 'onmouseover="window.status=' in html:
        return 1
    else:
        return -1

def check_RightClick(url, res):
    print('checking for right click prevention')
    # HTML verarbeiten und auf Event pruefen, das Rechtsklick verhindert
    html = res.text
    if 'event.button==2' in html:
        return 1
    else:
        return -1

def check_popUpWindow(url):
    return 0

def check_Iframe(url, res):
    print('checking for iframes with external content')
    # HTML verarbeiten
    hostname = parse.urlparse(url).hostname
    html = res.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # alle iFrames finden
    iframes = soup.findAll('iframe')
    malicious_iframes_found = 0
    # Quellen der iFrames auf Domain pruefen
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

def check_age_of_domain(w):
    print('checking for domain age\n')
    created = w.creation_date
    if isinstance(created, list):
        created = created[0]
    # Zeitspanne seit Erstellung berechnen
    today = datetime.today()
    try:
        delta = today - created
        months = delta.days / 30
        if months <= 6:
            return 1
        else:
            return -1
    except:
        print('skipping')
        return 'skip'

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