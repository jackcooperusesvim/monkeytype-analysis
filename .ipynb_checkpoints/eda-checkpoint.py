import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import config 
import sqlite3 as sql
import numpy as np
import pandas as pd
import seaborn as sns

def import_filt(plot = False):
    data = pd.read_csv(config.CSV_INPUT_FILEPATH())
    return filt(data,plot)

def filt(data, plot = False):
    # Remove everything with afk time
    #Make the charStats managable

    data["missed"] = data.charStats.apply(extract_missed)
    data["extra"] = data.charStats.apply(extract_extra_letters)
    data["incorrect"] = data.charStats.apply(extract_incorrect)
    data["ind"] = pd.Series(data.index)
    data["rawWpm"] = data["wpm"]/data["rawWpm"]

    if plot:
        sns.relplot(data = data, x = "ind", y = "wpm").set(title="Before")


    # this section filters out the Colemak days and non-representative datapoints and outliers



    m,b = line_from_points2d(370,70,500,20)

    colemak_filter = (data.timestamp>1.7*(10**12)) & (data.wpm<data.ind*m+b) & (data.wpm<70) & (300<data.ind)
    outlier_filter = ((300>data.ind) & (data.wpm<70)) | (data.acc<80)
    col_qwert_filter = (data.timestamp>1.7*(10**12)) & (data.timestamp<1.715*(10**12)) & ~colemak_filter
    old_filter = (360<data.ind) & (data.wpm>(data.ind*m+b)) & ~col_qwert_filter

    colemak_data = data[colemak_filter]
    col_qwert_data = data[col_qwert_filter]
    old_data = data[old_filter & ~col_qwert_filter]
    new_data = data[~colemak_filter & ~col_qwert_filter & ~old_filter & ~outlier_filter]
    #old_data = data.where(data.old_data).dropna(how="all")
    #colemak_data = data.where(data.colemak).dropna(how="all")

    new_data = new_data.assign(dataGroup = "new")
    old_data =  old_data.assign(dataGroup = "old")
    colemak_data = colemak_data.assign(dataGroup = "colemak")
    col_qwert_data= col_qwert_data.assign(dataGroup = "col_qwert")

    out_data = pd.concat([old_data,colemak_data,new_data,col_qwert_data], axis = 0) 
    
    if plot:
        sns.relplot(out_data,y="wpm",x="ind",hue='dataGroup').set(title="After")
    return out_data


def line_from_points2d(x1,y1,x2,y2):
    '''Returns the m and b required according to y=mx+b to fit the given points'''
    dx = x2-x1
    dy = y2-y1

    m = dy/dx

    b = y1-m*x1

    return m,b

def extract_incorrect(string):
    return string.split(';')[1]

def extract_extra_letters(string):
    return string.split(';')[2]

def extract_missed(string):
    return string.split(';')[3]





if __name__ == "__main__":
    data = import_filt(plot = True)
