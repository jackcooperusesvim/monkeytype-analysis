import config 
import pandas as pd
import seaborn as sns

def import_filt(plot = False):
    data = pd.read_csv(config.CSV_INPUT_FILEPATH())
    return filt(data,plot)

def filt(data, plot = False):

    # Extract charStats

    data["correct"] = data.charStats.apply(extract_correct)
    data["missed"] = data.charStats.apply(extract_missed)
    data["extra"] = data.charStats.apply(extract_extra_letters)
    data["incorrect"] = data.charStats.apply(extract_incorrect)
    data["Index"] = pd.Series(data.index[::-1])

    if plot:
        sns.relplot(data = data, x = "Index", y = "wpm").set(title="Before")

    # Declare Filters

    m,b = line_from_points2d(200,50,300,80)

    colemak_filter = (
        (data.timestamp>1.7*(10**12)) 
            & (data.wpm<data.Index*m+b) 
            & (data.wpm<70) 
            & (300>data.Index)
    )

    outlier_filter = (
        ((1.715*(10**12)<data.timestamp) 
            & (data.wpm<70)) 
        | (data.acc<80)
    )

    col_qwert_filter = (
        (data.timestamp>1.7*(10**12)) 
            & (data.timestamp<1.715*(10**12)) 
            & ~colemak_filter
    )

    old_filter = (
        (1.7*(10**12)>data.timestamp) 
            & (data.wpm>(data.Index*m+b)) 
            & ~col_qwert_filter
    )

    # Split Data
    new_data = data[
        ~colemak_filter 
        & ~col_qwert_filter 
        & ~old_filter 
        & ~outlier_filter
    ]

    old_data = data[
        old_filter 
        & ~col_qwert_filter
    ]

    colemak_data = data[colemak_filter]

    col_qwert_data = data[col_qwert_filter]

    # Label Data

    new_data = new_data.assign(dataGroup = "new")
    old_data =  old_data.assign(dataGroup = "old")
    colemak_data = colemak_data.assign(dataGroup = "colemak")
    col_qwert_data= col_qwert_data.assign(dataGroup = "col_qwert")

    # Rejoin Data

    out_data = pd.concat([old_data,colemak_data,new_data,col_qwert_data], axis = 0) 

    if plot:
        sns.relplot(out_data,y="wpm",x="Index",hue='dataGroup').set(title="After Grouping")

    # Filtering all data that
        # is not new
        # is typed in the normal typing mode (as opposed to quotes mode)
        # has no time spent AFK (away from keyboard)
        # no wpm was recorded

    out_data = out_data.where(
            (out_data.dataGroup == "new") 
            & (out_data.afkDuration == 0) 
            & (out_data.quoteLength == -1)
            & ~out_data.wpm.isna()
    )

    if plot:
        sns.relplot(out_data,y="wpm",x="Index",hue='dataGroup').set(title="After Grouping")

    return out_data


def line_from_points2d(x1,y1,x2,y2):
    '''Returns the m and b required according to y=mx+b to fit the given points'''
    dx = x2-x1
    dy = y2-y1

    m = dy/dx

    b = y1-m*x1

    return m,b

def extract_correct(string):
    return string.split(';')[0]

def extract_incorrect(string):
    return string.split(';')[1]

def extract_extra_letters(string):
    return string.split(';')[2]

def extract_missed(string):
    return string.split(';')[3]


if __name__ == "__main__":
    data = import_filt(plot = True)
