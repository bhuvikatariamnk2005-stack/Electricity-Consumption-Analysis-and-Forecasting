import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def prepare(df):
    df = df[['date','kwh']].copy()
    df['date'] = pd.to_datetime(df['date'], errors='raise').dt.to_period('M').dt.to_timestamp()
    df['kwh'] = pd.to_numeric(df['kwh'], errors='raise')
    if not np.isfinite(df.kwh).all() or (df.kwh < 0).any():
        raise ValueError('Consumption must be finite and non-negative.')
    df = df.sort_values('date').reset_index(drop=True)
    if len(df) < 24 or not df.date.equals(pd.Series(pd.date_range(df.date.iloc[0], periods=len(df), freq='MS'))):
        raise ValueError('Provide at least 24 consecutive months, one row per month.')
    return df

def features(dates):
    t = dates.dt.year * 12 + dates.dt.month - 1 - 2020*12
    angle = 2*np.pi*(dates.dt.month-1)/12
    return np.column_stack([t, np.sin(angle), np.cos(angle)])

def forecast(df, months):
    df = prepare(df)
    x, y = features(df.date), df.kwh
    split = len(df)-6
    model = LinearRegression().fit(x[:split], y.iloc[:split])
    test = np.maximum(0, model.predict(x[split:]))
    mae = mean_absolute_error(y.iloc[split:], test)
    model.fit(x,y)
    dates = pd.Series(pd.date_range(df.date.iloc[-1]+pd.offsets.MonthBegin(1), periods=months, freq='MS'))
    future = pd.DataFrame({'date':dates,'kwh':np.maximum(0,model.predict(features(dates))).round(2)})
    return future, mae
