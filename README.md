# Energy Insight
Electricity consumption analysis and forecasting using seasonal linear regression.

## Run locally
Install Python 3.10+ and open a terminal in this folder.

    python -m pip install -r requirements.txt
    python -m streamlit run app.py

Open the local URL printed in the terminal. Upload a CSV with `date,kwh` columns and at least 24 consecutive monthly records, or use the included synthetic sample. Adjust forecast horizon and tariff. Forecasts are estimates, not guaranteed future readings. The last six months are held out for MAE evaluation; the final model is fitted on all records.

## GitHub
Create a repository on github.com, select Add file > Upload files, upload app.py, model.py, sample.csv, requirements.txt and README.md, then commit. Copy the repository URL into your report.
