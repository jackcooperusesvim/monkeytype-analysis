import matplotlib.pyplot as plt
import config 
import sqlite3 as sql
import numpy as np
import pandas as pd

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
    if plot:
        #Ordered data according to the order in which the tests were taken
        fig, ax = plt.subplots()
        ax.set_label("wpm by id")
        ax.scatter(data.index, data.wpm)
        #
        # fig2, ax2 = plt.subplots()
        # ax2.scatter(data.timestamp[::-1], data.wpm[::-1])
        # ax2.set_label("wpm by time")
        plt.show()


    # this section filters out the Colemak days and non-representative datapoints and outliers



    m,b = line_from_points2d(370,70,500,20)

    # != is the same as xor
    colemak_filter = (data.wpm<data.ind*m+b) & (data.wpm<70) & (300<data.ind)
    outlier_filter = (300>data.ind) & (data.wpm<70)
    old_filter = (360<data.ind) & (data.wpm>(data.ind*m+b))
    
    colemak_data = data[colemak_filter]
    old_data = data[old_filter]
    new_data = data[~colemak_filter & ~old_filter & ~outlier_filter]
    #old_data = data.where(data.old_data).dropna(how="all")
    #colemak_data = data.where(data.colemak).dropna(how="all")
    #The following lines show the filtering
    if plot:
        plt.scatter(colemak_data.ind, colemak_data.wpm)
        plt.scatter(old_data.ind, old_data.wpm)
        plt.scatter(new_data.ind, new_data.wpm)
        #plt.scatter(np.array(data.index), data.wpm, c = data.old_data)
        plt.plot(data.ind,data.ind*m+b)
        plt.show()

    new_data = new_data.assign(dataGroup = "new")
    old_data =  old_data.assign(dataGroup = "old")
    colemak_data = colemak_data.assign(dataGroup = "colemak")
    
    return pd.concat([old_data,colemak_data,new_data], axis = 0)


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
