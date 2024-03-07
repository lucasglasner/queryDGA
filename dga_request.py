'''
 # @ Author: Lucas Glasner (lgvivanco96@gmail.com)
 # @ Create Time: 1969-12-31 21:00:00
 # @ Modified by: Lucas Glasner, 
 # @ Modified time: 2024-01-05 12:56:46
 # @ Description:
 # @ Dependencies:
 '''

import os
import sys
import pandas as pd
import requests
import time


def get_dgacurl_url(string):
    url = string.split('-X')[0].split("curl")[1]
    url = url.replace('\'', '').replace(' ', '')
    return url


def get_dgacurl_headers(string):
    hkeys = [H.split(": ")[0][1:] for H in string.split('-H ')[1:-1]]
    hvalues = [H.split(": ")[1][:-2] for H in string.split('-H ')[1:-1]]
    headers = {key: value for key, value in zip(hkeys, hvalues)}
    return headers


def get_dgacurl_data(string):
    data = string.split('--data-raw ')[-1].split('&')
    datakeys = [key.split("=")[0].replace('\'', '') for key in data]
    datakeys = [key.replace('%3A', ':') for key in datakeys]
    datavalues = [key.split("=")[1].replace('\'', '') for key in data]
    datavalues = [key.replace('%3A', ':').replace('+', ' ')
                  for key in datavalues]
    datavalues = [key.replace('%2F', '/') for key in datavalues]
    data = {key: value for key, value in zip(datakeys, datavalues)}
    return data


def request_data_edit_dates(data, startdate, enddate):
    ndata = data.copy()
    ndata['filtroscirhform:fechaDesdeInputDate'] = startdate
    ndata['filtroscirhform:fechaHastaInputDate'] = enddate
    return ndata


def check_corrupted_download(inputfile, remove=True):
    print('Checking raw downloaded file consistency...')
    try:
        pd.read_excel(inputfile)
        print(f'All good with {inputfile}')
        return True
    except Exception as e:
        print(e)
        print(f'{inputfile}: corrupt')
        if remove:
            print(f'{inputfile}: removing')
            os.remove(inputfile)
        return False


def dga_download_request(dga_curl, fileprefix, output_dir, startyear, endyear):
    url = get_dgacurl_url(dga_curl)
    headers = get_dgacurl_headers(dga_curl)

    cookie = headers['Cookie'].split("=")
    cookies = {cookie[0]: cookie[1]}
    years = range(startyear, endyear+1)
    data = get_dgacurl_data(dga_curl)

    for yr in years:
        print(f'Requesting data for {yr}...')
        tdata = request_data_edit_dates(data, f'01/01/{yr}', f'31/12/{yr}')
        response = requests.post(url,
                                 cookies=cookies,
                                 headers=headers,
                                 data=tdata)
        if response.status_code == 200:
            print("Request was successful!")
            if os.name == 'nt':
                filename = f'{output_dir}\{fileprefix}_{yr}.xls'
            else:
                filename = f'{output_dir}/{fileprefix}_{yr}.xls'

            with open(filename, "wb") as excel:
                excel.write(response.content)
                excel.close()
            check_corrupted_download(filename, remove=True)
        else:
            print(f"Request failed with status code {response.status_code}")
        print('\n')
        time.sleep(1)
    return response, (headers, cookies, data)


# data = pd.read_excel('tmp/pozo_2004.xls')

if __name__ == '__main__':
    path_DGA_curl = 'DGA_cURL'
    DGA_curl = open(path_DGA_curl).read()
    response, _ = dga_download_request(DGA_curl, 'RioLigua',
                                       'tmp',
                                       2010, 2014)
