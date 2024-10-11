import pandas as pd
import seaborn as sns
import matplotlib
import sklearn.linear_model as lm
from typing import Any

def linreg(data:pd.DataFrame,x:str,y:str,ax: Any|None =None,color:str|None=None,label:str|None=None):
    X = [0,max(data[[x]])]
    model = lm.LinearRegression().fit(data[[x]],data[[y]])
    Y = model.predict(X=X)

    return sns.regplot(x=X,y=Y,data=data,color=color,label=label,ax=ax)
