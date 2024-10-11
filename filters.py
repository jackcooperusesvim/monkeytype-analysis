import config 
import polars as pl

def import_filt(*dataGroups):
    data = pl.read_csv(config.CSV_INPUT_FILEPATH(),infer_schema_length=int(1e10))

    if len(dataGroups) == 0: 
        dataGroups = ['new']

    x = filt(data,dataGroups)
    print(x.columns)
    return x

def filt(data: pl.DataFrame, dataGroups: list[str] = ['new']):

    m,b = line_from_points2d(200,50,300,80)

    return data.with_columns(
        timeIndex = pl.len()-pl.Series(range(1,len(data)+1)),
    ).with_columns(
        testType = (
            pl.when(pl.col('testDuration') <= 29).then(
                pl.lit('short')
            ).when(pl.col('testDuration') == 30).then(
                pl.lit('long')
            ).when(pl.col('quoteLength') != -1).then(
                pl.lit('quote')
            ).otherwise(
                pl.lit('other')
            )
        ),
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
                pl.lit('colemak')
            ).otherwise(
                pl.lit('qwert_col')
            )
        ),
        correct = pl.col("charStats").str.split(";").list.get(0).str.to_integer(),
        incorrect = pl.col("charStats").str.split(";").list.get(1).str.to_integer(),
        extra = pl.col("charStats").str.split(";").list.get(2).str.to_integer(),
        missed = pl.col("charStats").str.split(";").list.get(3).str.to_integer(),
    ).filter(
        pl.col('testType') != pl.lit('quote'),
        pl.col('afkDuration') == 0,
        pl.col("dataGroup").is_in(dataGroups),
        pl.col('wpm') is not pl.Null,
    )

def graph_ops(data: pl.DataFrame, select:bool=False) -> pl.DataFrame:
    if select:
        return data.select(
            restartCountAdjusted = pl.col('restartCount').log1p(),
            oldAvgWpm = pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='old').mean(),
            newAvgWpm = pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='new').mean(),
            colemakAvgWpm = pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='colemak').mean(),
            qwert_colAvgWpm = pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='qwert_col').mean(),
        )
    else:
        return data.with_columns(
            restartCountAdjusted = pl.col('restartCount').log1p(),
            AvgWpmComparison = (
                    pl.when(pl.col('dataGroup') == 'old').then(
                        pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='old').mean(),
                    ).when(pl.col('dataGroup') == 'new').then(
                        pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='new').mean(),
                    ).when(pl.col('dataGroup') == 'colemak').then(
                        pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='colemak').mean(),
                    ).when(pl.col('dataGroup') == 'qwert_col').then(
                        pl.col('wpm')-pl.col('wpm').where(pl.col('dataGroup')=='qwert_col').mean(),
                    ).otherwise(
                    0
                    )
            ),
        )

def line_from_points2d(x1,y1,x2,y2):
    '''Returns the m and b required according to y=mx+b to fit the given points'''
    dx = x2-x1
    dy = y2-y1

    m = dy/dx

    b = y1-m*x1

    return m,b

if __name__ == "__main__":
    dataGroupOptions= ['new','old','colemak','qwert_col']
    data = import_filt(dataGroupOptions)
