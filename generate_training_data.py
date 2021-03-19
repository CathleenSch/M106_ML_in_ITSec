from extract_features import *
from helpers import *
import os
import asyncio

URL_lists_folder = r'C:\Users\Work\Documents\M106\Hausarbeit\Praxisteil\M106_ML_in_ITSec\URLs'

valid_sites_file = 'valid_sites.txt'
phishing_sites_file = 'phishing_sites.txt'
trainingdata_file = 'trainingdata.txt'

def get_features(url, response):
    list_of_features = ''
    having_IP_Address = check_having_IP_Address(url)
    list_of_features += str(having_IP_Address)
    URL_Length = check_URL_Length(url)
    list_of_features += ',' + str(URL_Length)
    Shortening_Service = check_Shortening_Service(url)
    list_of_features += ',' + str(Shortening_Service)
    having_At_symbol = check_having_At_symbol(url)
    list_of_features += ',' + str(having_At_symbol)
    double_slash_redirecting = check_double_slash_redirecting(url)
    list_of_features += ',' + str(double_slash_redirecting)
    Prefix_Suffix = check_Prefix_Suffix(url)
    list_of_features += ',' + str(Prefix_Suffix)
    having_Sub_Domain = check_having_Sub_Domain(url)
    list_of_features += ',' + str(having_Sub_Domain)
    SSLfinal_State = check_SSLfinal_State(url)
    list_of_features += ',' + str(SSLfinal_State)
    Domain_registration_length = check_Domain_registration_length(url)
    list_of_features += ',' + str(Domain_registration_length)
    Favicon = check_Favicon(url)
    list_of_features += ',' + str(Favicon)
    port = asyncio.run(check_port(url))
    list_of_features += ',' + str(port)
    HTTPS_token = check_HTTPS_token(url)
    list_of_features += ',' + str(HTTPS_token)
    Request_URL = check_Request_URL(url, response)
    list_of_features += ',' + str(Request_URL)
    URL_of_Anchor = check_URL_of_Anchor(url, response)
    list_of_features += ',' + str(URL_of_Anchor)
    Links_in_tags = check_Links_in_tags(url, response)
    list_of_features += ',' + str(Links_in_tags)
    SFH = check_SFH(url)
    list_of_features += ',' + str(SFH)
    Submitting_to_email = check_Submitting_to_email(url)
    list_of_features += ',' + str(Submitting_to_email)
    Abnormal_URL = check_Abnormal_URL(url)
    list_of_features += ',' + str(Abnormal_URL)
    Redirect = check_Redirect(response)
    list_of_features += ',' + str(Redirect)
    on_mouseover = check_on_mouseover(url, response)
    list_of_features += ',' + str(on_mouseover)
    RightClick = check_RightClick(url, response)
    list_of_features += ',' + str(RightClick)
    popUpWindow = check_popUpWindow(url)
    list_of_features += ',' + str(popUpWindow)
    Iframe = check_Iframe(url, response)
    list_of_features += ',' + str(Iframe)
    age_of_domain = check_age_of_domain(url)
    list_of_features += ',' + str(age_of_domain)
    DNSRecord = check_DNSRecord(url)
    list_of_features += ',' + str(DNSRecord)
    web_traffic = check_web_traffic(url)
    list_of_features += ',' + str(web_traffic)
    Page_Rank = check_Page_Rank(url)
    list_of_features += ',' + str(Page_Rank)
    Google_Index = check_Google_Index(url)
    list_of_features += ',' + str(Google_Index)
    Links_pointing_to_page = check_Links_pointing_to_page(url)
    list_of_features += ',' + str(Links_pointing_to_page)
    Statistical_report = check_Statistical_report(url)
    list_of_features += ',' + str(Statistical_report)

    return list_of_features

def empty_trainingdata_file():
    file_trainingdata = open(trainingdata_file, encoding='utf-8', mode='w')
    file_trainingdata.write('')
    file_trainingdata.close()


empty_trainingdata_file()

file_phishing = open(os.path.join(URL_lists_folder, phishing_sites_file), encoding='utf-8', mode='r')
phishing_urls = file_phishing.readlines()
for index, url in enumerate(phishing_urls):
    if index == 0:
        file_trainingdata = open(trainingdata_file, encoding='utf-8', mode='w')
    else:
        file_trainingdata = open(trainingdata_file, encoding='utf-8', mode='a')
    print(f'Processing phishing URL {index+1} of {len(phishing_urls)}: {url}')
    url = url[:len(url)-2]
    response = get_request(url)
    if response == None:
        print('URL not available, skipping')
        continue
    features = get_features(url, response)
    Result = 1
    if '-2' in features:
        continue
    else:
        features += ',' + str(Result) + '\n'
        file_trainingdata.write(features)
    file_phishing.close()

file_valid = open(os.path.join(URL_lists_folder, valid_sites_file), encoding='utf-8', mode='r')
file_trainingdata = open(trainingdata_file, encoding='utf-8', mode='a')

valid_urls = file_valid.readlines()
for index, url in enumerate(valid_urls):
    print(f'Processing valid URL {index+1} of {len(valid_urls)}: {url}')
    features = get_features(url)
    Result = 0
    if '-2' in features:
        continue
    else:
        features += ',' + str(Result) + '\n'
        file_trainingdata.write(features)
file_valid.close()

file_trainingdata.close()