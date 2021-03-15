import os
import pandas as pd

sources_folder = r'C:\Users\Work\Documents\M106\Hausarbeit\Praxisteil\M106_ML_in_ITSec\Sources'
URL_lists_folder = r'C:\Users\Work\Documents\M106\Hausarbeit\Praxisteil\M106_ML_in_ITSec\URLs'

def get_column_of_csv_file(file):
    df = pd.read_csv(file)
    saved_column = df.url

    return saved_column

def get_lists_of_websites():
    # create list of valid, non-malicious websites from csv files
    valid_list_folder = os.path.join(sources_folder, 'Valid_Sites')
    url_list = []
    for filename in os.listdir(valid_list_folder):
        valid_list_file = os.path.join(valid_list_folder, filename)
        column = get_column_of_csv_file(valid_list_file)
        for line in column:
            url_list.append(f'{line}\n')

    file_write = open(os.path.join(URL_lists_folder, 'valid_sites.txt'), encoding='utf-8', mode='w')
    file_write.writelines(url_list)
    file_write.close()


    # create list of phishing websites from csv
    url_list = []
    phishing_list_file = os.path.join(sources_folder, 'verified_online.csv')
    column = get_column_of_csv_file(phishing_list_file)
    for line in column:
        url_list.append(f'{line}\n')

    file_write = open(os.path.join(URL_lists_folder, 'phishing_sites.txt'), encoding='utf-8', mode='w')
    file_write.writelines(url_list)
    file_write.close()

def get_average_URL_length(isPhishing):
    if isPhishing:
        filename = 'phishing_sites.txt'
    else:
        filename = 'valid_sites.txt'
    file_write = open(os.path.join(URL_lists_folder, filename), encoding='utf-8', mode='r')
    urls = file_write.readlines()
    url_count = len(urls)
    url_sum = 0
    url_max_len = 0
    longest = ''
    shortest = ''
    url_min_len = 75
    for url in urls:
        length = len(url)
        if length > url_max_len:
            url_max_len = length
            longest = url
        if length < url_min_len:
            url_min_len = length
            shortest = url
        url_sum += length
    
    average_len = url_sum / url_count

    return(average_len)

def print_average_URL_lengths():
    average_benign = get_average_URL_length(False)
    average_malicious = get_average_URL_length(True)

    print('Durchschnittliche URL-Länge valider Webseiten:\t\t' + str(average_benign))
    print('Durchschnittliche URL-Länge von Phishing-Webseiten:\t' + str(average_malicious))