import config 
from icecream import ic
import polars as pl
import seaborn as sns

def import_filt(dg = 'new'):
    data = pl.read_csv(config.CSV_INPUT_FILEPATH(),infer_schema_length=int(1e10))
    x = filt(data,dg)
    print(x.columns)
    return x

def filt(data: pl.DataFrame,dg = 'new'):

    # Declare Filter Line
    m,b = line_from_points2d(200,50,300,80)

    return data.with_columns(
        correct = pl.col("charStats").str.split(";").list.get(0).str.to_integer(),
        incorrect = pl.col("charStats").str.split(";").list.get(1).str.to_integer(),
        extra = pl.col("charStats").str.split(";").list.get(2).str.to_integer(),
        missed = pl.col("charStats").str.split(";").list.get(3).str.to_integer(),
        timeIndex= pl.len()-pl.Series(range(1,len(data)+1))

    ).with_columns(
        testLen = pl.col("correct")+pl.col("incorrect")+pl.col("missed"),
        incorrect_prop = pl.col('correct')/pl.col('incorrect'),
        missed_prop = pl.col('correct')/pl.col('missed'),
        extra_prop = pl.col('correct')/pl.col('extra')
    ).filter(
        #Filter out all 
        pl.col('quoteLength') == -1,
        pl.col('afkDuration') == 0

    ).with_columns(
        dataGroup = (
            pl.when(pl.col("timestamp") > 1.715*(10**12)).then(
                    pl.when(pl.col('wpm')<70).then(
                        pl.lit("outlier")
                    ).when(pl.col('acc')<80).then(
                        pl.lit("outlier")
                    ).otherwise(
                        pl.lit("new")
                    )
            ).when(pl.col('timestamp') < 1.7*(10**12)).then(
                pl.lit('old')
            ).when(pl.col("timeIndex")*m+b > pl.col('wpm')).then(
                pl.lit('qwert_col')
            ).otherwise(
                pl.lit('colemak')
            )
        ),
        isQuote = pl.col('quoteLength') != -1,

    ).filter(
        pl.col("dataGroup")==dg,
        pl.col('afkDuration')==0,
        pl.col('wpm') is not pl.Null,
        pl.col('testLen') < 400
    ).with_columns(
        testIsShort = pl.col('testDuration') < 18
    )


def line_from_points2d(x1,y1,x2,y2):
    '''Returns the m and b required according to y=mx+b to fit the given points'''
    dx = x2-x1
    dy = y2-y1

    m = dy/dx

    b = y1-m*x1

    return m,b

def extract_correct(string):
    return int(string.split(';')[0])

def extract_incorrect(string):
    return int(string.split(';')[1])

def extract_extra(string):
    return int(string.split(';')[2])

def extract_missed(string):
    return int(string.split(';')[3])


if __name__ == "__main__":
    data = import_filt(plot = True)
