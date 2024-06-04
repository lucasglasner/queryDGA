'''
 # @ Author: Lucas Glasner (lgvivanco96@gmail.com)
 # @ Create Time: 1969-12-31 21:00:00
 # @ Modified by: Lucas Glasner, 
 # @ Modified time: 2024-05-13 17:31:13
 # @ Description:
 # @ Dependencies:
 '''

import pandas as pd
import numpy as np


def DGAGrab_Metadata(DGA_excel):
    metadata = DGA_excel.iloc[4:8, :].T.dropna(how='all').T
    name, stid, c1, c2 = metadata.iloc[:, 1]
    z, lat, lon = metadata.iloc[1:, 3]
    y, x = metadata.iloc[1:-1, -1]
    metadata = pd.Series((c1, c2, name, x, y, lon, lat, z),
                         index=['Cuenca', 'SubCuenca', 'Nombre',
                                'x', 'y', 'lon', 'lat', 'Altura'])
    metadata.name = stid
    metadata = pd.DataFrame(metadata)
    return metadata


def process_DGA_QTable(DGA_excel):
    # Drop usesless stuff from spreadsheet and compute metadata
    DGA_excel = DGA_excel.T.dropna(how='all').T
    metadata  = DGAGrab_Metadata(DGA_excel)

    # grab only necesary cells
    months = DGA_excel[DGA_excel.iloc[:, 0].map(lambda x: 'MES' in str(x))]
    months = months.T.dropna(how='all').T.iloc[:, -1]
    data = [DGA_excel.iloc[months.index[i]:months.index[i+1], :]
            for i in range(len(months.index)-1)]
    data.append(DGA_excel.iloc[months.index[-1]:-1])
    data = [d.T.dropna(how='all').T for d in data]

    # grab data and build timestamp
    headers = data[0].iloc[1, :]
    masks = [headers.map(lambda x: string in x).values
             for string in ['DIA', 'HORA', 'CAUDAL', 'ALTURA']]
    runoff, heights = [np.hstack([d.iloc[:, m].iloc[2:].values.flatten()
                                  for d in data])
                       for m in masks[2:]]
    days, hrs = [[d.iloc[:, m].iloc[2:].stack().reset_index(drop=True)
                  for d in data]
                 for m in masks[:2]]
    timestamp = [(hrs[i]+'T'+days[i].astype(str)+'/'+months.values[i]).values
                 for i in range(len(days))]
    timestamp = np.hstack(timestamp)
    data = pd.DataFrame([runoff, heights], index=['q_m3s', 'h_m']).T.dropna()
    data.name = metadata.columns[0]
    data.index = pd.to_datetime(timestamp, format='%H:%MT%d/%m/%Y')
    return data, metadata


def process_DGA_PrMaxTable(DGA_excel):
    # Drop usesless stuff from spreadsheet and compute metadata
    DGA_excel = DGA_excel.T.dropna(how='all').T
    metadata = DGAGrab_Metadata(DGA_excel)

    # grab data and build timestamp
    data = DGA_excel.loc[9:]
    data = data.T.dropna(how='all').T
    data.columns = data.iloc[0, :].values
    data = data.iloc[1:, :]
    timestamp = [pd.to_datetime(f'{y}/{x}', format='%d/%m/%Y')
                 for x, y in zip(data['AÑO'],
                                 data['FECHA'])]
    data = data.iloc[:, -1]
    data.name = metadata.columns[0]
    data = pd.DataFrame(pd.to_numeric(data))
    data.index = timestamp
    return data, metadata


def process_DGA_Pr24hTable(DGA_excel):
    # Drop usesless stuff from spreadsheet and compute metadata
    DGA_excel = DGA_excel.T.dropna(how='all').T
    metadata = DGAGrab_Metadata(DGA_excel)

    data = DGA_excel.loc[9:]
    data = data.T.dropna(how='all').T
    years = data.iloc[:, 0].map(lambda x: 'AÑO' in str(x))
    years = data.loc[years].index
    ndata = []
    for yr in years:
        x = data.loc[(yr+2):(yr+31+1)].iloc[:, 1:]
        yr = np.tile(data.loc[yr].iloc[0].split(' ')[-1], 12*31)
        m = np.hstack([np.ones(31)*y for y in range(1, 12+1, 1)])
        d = np.tile(np.arange(1, 31+1, 1), 12)
        tt = pd.DataFrame([yr, m, d]).T.map(lambda x: str(int(x)))
        tt = tt[0]+'-'+tt[1]+'-'+tt[2]
        tt = tt.values
        timestamp = []
        for t in tt:
            try:
                timestamp.append(pd.to_datetime(t))
            except:
                timestamp.append(np.nan)

        x = pd.Series(x.values.flatten(), index=timestamp)
        ndata.append(x)
    ndata = pd.concat(ndata)
    ndata = ndata.dropna()
    ndata = ndata.loc[ndata.index.notnull()]
    ndata.name = metadata.columns[0]
    return ndata, metadata


def process_DGAtable(DGA_excel, vtype):
    DGA_excel = DGA_excel.T.dropna(how='all').T
    if vtype == 'AlturayCaudalInstantaneo':
        data, metadata = process_DGA_QTable(DGA_excel)
    elif vtype == 'PrecipitacionesMaximasEn24Horas':
        data, metadata = process_DGA_PrMaxTable(DGA_excel)
    elif vtype == 'PrecipitacionesDiarias':
        data, metadata = process_DGA_Pr24hTable(DGA_excel)
    else:
        raise ValueError(f'{vtype} Variable desconocida!')
    return data, metadata
