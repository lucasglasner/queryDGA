'''
 # @ Author: Lucas Glasner (lgvivanco96@gmail.com)
 # @ Create Time: 1969-12-31 21:00:00
 # @ Modified by: Lucas Glasner, 
 # @ Modified time: 2024-05-13 17:28:10
 # @ Description:
 # @ Dependencies:
 '''

import os
import pandas as pd
import requests
import time


def check_corrupted_download(inputfile, remove=True, verbose=False):
    """
    Simple function to check if an excel download file is corrupt or not.
    (If the request asks for data on a not valid year, the requests seems
    to write an .xml file with errors and a bunch of crap.) This function
    just try to load the excel file and if something goes wrong return False
    and optionally removes the file.

    Args:
        inputfile (str): Path to the spreadsheet
        remove (bool, optional): Defaults to True.
        verbose (bool, optional): Defaults to False.

    Returns:
        (bool): Corrupt or not
    """
    try:
        pd.read_excel(inputfile)
        return True
    except Exception as e:
        if verbose:
            print(e, f'{inputfile}: corrupt')
        if remove:
            os.remove(inputfile)
        return False


def DGA_makerequest(ofile, url, cookies, headers, data):
    """
    This functions makes the request to the DGA server given 
    and output file name (excel spreadsheet), the server url, the cookies,
    headers and data of the post request.

    Args:
        ofile (str): _description_
        url (str): _description_
        cookies (dict): _description_
        headers (dict): _description_
        data (dict): _description_

    Returns:
        (bool): If the download worked or not
    """
    response = requests.post(url, cookies=cookies, headers=headers, data=data)
    if response.status_code == 200:
        with open(ofile, 'wb') as file:
            file.write(response.content)
    else:
        print('Request ended with:', response.status_code, 'Trying again...')
        time.sleep(2)
        return DGA_makerequest(ofile, url, cookies, headers, data)
    if os.path.isfile(ofile):
        corrupt = check_corrupted_download(ofile, remove=True)
        if corrupt:
            return False
        else:
            return True
    return False
