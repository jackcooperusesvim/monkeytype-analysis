import matplotlib.pyplot as plt
import config 
import sqlite3 as sql
import numpy as np
import pandas as pd

def import_filt(plot = False):
    data = pd.read_csv(config.CSV_INPUT_FILEPATH())
    return filt(data,plot)

def filt(data, plot = False):
    #Make the charStats managable
    data["missed"] = data.charStats.apply(extract_missed)
    data["extra"] = data.charStats.apply(extract_extra_letters)
    data["incorrect"] = data.charStats.apply(extract_incorrect)
    if plot:
        #Ordered data according to the order in which the tests were taken
        fig, ax = plt.subplots()
        ax.set_label("wpm by id")
        ax.scatter(data.index, data.wpm[::-1])
        #
        # fig2, ax2 = plt.subplots()
        # ax2.scatter(data.timestamp[::-1], data.wpm[::-1])
        # ax2.set_label("wpm by time")
        # plt.show()



    # this section filters out the Colemak days and non-representative datapoints and outliers



    m,b = line_from_points2d(185,70,300,30)

    colemak_filter = (data.wpm<(pd.Series(data.index)*m+b)) & (pd.Series(data.index)>160) | (data.wpm >110) | (data.index>40) & (data.wpm<40) & (data.index<100)
    data["colemak_filter"] = colemak_filter


    #The following lines show the filtering
    if plot:
        fig2, ax2 = plt.subplots()
        ax2.set_label("cleaned")
        plt.scatter(np.array(data.index[::-1]), data.wpm, c = data.colemak_filter)
        plt.show()

    return data


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
    data = import_filt()
