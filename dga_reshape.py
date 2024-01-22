'''
      _             _          
  _ _(_)_ _____ _ _(_)_ _  ___ 
 | '_| \ V / -_) '_| | ' \/ -_)
 |_| |_|\_/\___|_| |_|_||_\___|

 # @ Author: Lucas Glasner (lgvivanco96@gmail.com)
 # @ Create Time: 1969-12-31 21:00:00
 # @ Modified by: Lucas Glasner, 
 # @ Modified time: 2024-01-11 08:58:48
 # @ Description:
 # @ Dependencies:
 '''

import pandas as pd
import numpy as np
from glob import glob
import os


def fix_single_dga_excel(path, cell_start=11):
    data = pd.read_excel(path, skiprows=cell_start-1, skipfooter=1)
    data = data.T.dropna(how='all').T
    dates = data.iloc[:, ::2].values.flatten()
    values = data.iloc[:, 1::2].values.flatten()
    data = pd.Series(values, index=dates).dropna()
    data = pd.to_numeric(data)
    return data


def fix_dga_excel(paths, **kwargs):
    files = []
    for p in paths:
        data = fix_single_dga_excel(p, **kwargs)
        files.append(data)
    files = pd.concat(files, axis=0)
    return files


if __name__ == '__main__':
    name = 'Pozo_Parcela2SanRamon'
    data = fix_dga_excel(glob(f'tmp/{name}*'))
    data.to_csv(f'data/{name}.csv')
