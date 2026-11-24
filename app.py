from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from model import prepare, forecast

st.set_page_config(page_title='Energy Insight', layout='wide')
st.title('Energy Insight | Electricity Consumption')
st.caption('Monthly analysis and machine learning forecasting')
file = st.sidebar.file_uploader('Upload CSV (date, kwh)', type='csv')
months = st.sidebar.slider('Forecast months', 1, 12, 6)
rate = st.sidebar.number_input('Tariff (INR per kWh)', min_value=0.0, value=8.0)
try:
    df = prepare(pd.read_csv(file if file else Path(__file__).with_name('sample.csv')))
    future, mae = forecast(df, months)
except (ValueError, KeyError, TypeError) as exc:
    st.error(str(exc))
    st.stop()
if file is None:
    st.info('Demo: synthetic monthly data, not actual utility readings.')
a,b,c,d = st.columns(4)
a.metric('Latest month', f'{df.kwh.iloc[-1]:,.1f} kWh')
b.metric('Monthly average', f'{df.kwh.mean():,.1f} kWh')
c.metric('Next month forecast', f'{future.kwh.iloc[0]:,.1f} kWh')
d.metric('Estimated next bill', f'INR {future.kwh.iloc[0]*rate:,.0f}')
st.plotly_chart(px.bar(df, x='date', y='kwh', title='Monthly consumption'), use_container_width=True)
annual = df.assign(year=df.date.dt.year).groupby('year',as_index=False).kwh.sum()
st.plotly_chart(px.bar(annual,x='year',y='kwh',title='Annual totals (partial years may occur)'),use_container_width=True)
peak, low = df.loc[df.kwh.idxmax()], df.loc[df.kwh.idxmin()]
st.write(f'Highest: {peak.kwh:.1f} kWh ({peak.date:%b %Y}) | Lowest: {low.kwh:.1f} kWh ({low.date:%b %Y})')
combined = pd.concat([df.assign(series='Historical'),future.assign(series='Forecast')])
st.plotly_chart(px.line(combined,x='date',y='kwh',color='series',markers=True,title='Consumption forecast'),use_container_width=True)
st.write(f'Holdout MAE (last six months): {mae:.2f} kWh')
st.caption('Forecasts are estimates. Bill excludes fixed charges, taxes and slab pricing.')
st.dataframe(future, hide_index=True)
st.download_button('Download forecast CSV',future.to_csv(index=False),'forecast.csv','text/csv')
