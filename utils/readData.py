import pandas as pd


def readDataFromExcel(path, option, request, columnList):
    # 数据中不包含列名
    # df = pd.read_excel(path, sheet_name=0, header=None, skiprows=1)
    df = pd.read_excel(path, sheet_name=0)
    df = df[df[option] == request].loc[:, columnList]
    return df
