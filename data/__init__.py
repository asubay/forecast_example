from statistics import quantiles
from config import (
    DATABASE_HOST,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_PORT
)

from .db import Database
from .queries import queries
from .log import LOGGER
from train.train_usd_daily import train_usd
from train.train_rub_daily import train_rub
import pandas as pd
import datetime
import sys

db = Database(
    DATABASE_HOST,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_PORT
)


def init_script():
    try:
        # get dataset to train model
        df_usd = db.select_rows_df(queries['select_currency_usd'])
        df_rub = db.select_rows_df(queries['select_currency_rub'])
        if len(df_usd) <= 0:
            return None
        # get forecast id from table currency.forecast
        forecast_id = db.select_id(queries['insert_currency_forecast'])
        # train usd model
        process_usd(df_usd, forecast_id, queries['insert_forecast_rate'])
        if len(df_rub) <= 0:
            return None
        # train rub model
        process_rub(df_rub, forecast_id, queries['insert_forecast_rate'])

    except Exception as e:
        LOGGER.error(e)

    finally:
        LOGGER.info(f'process data finished successfully')
        db.connection_check()
        sys.exit()


def process_usd(dataset, forecast_id, query):
    """ start process usd forecast """
    start_date = dataset.date.iloc[-1] + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=6)
    date_range = pd.date_range(start=start_date, end=end_date)
    prediction = train_usd(dataset)
    if len(prediction) > 0:
        insert_forecast_values(query, 'USD', prediction, date_range, forecast_id)


def process_rub(dataset, forecast_id, query):
    """start process rub forecast"""
    start_date = dataset.date.iloc[-1] + datetime.timedelta(days=1)  # get
    end_date = start_date + datetime.timedelta(days=6)
    date_range = pd.date_range(start=start_date, end=end_date)
    prediction = train_rub(dataset)
    if len(prediction) > 0:
        insert_forecast_values(query, 'RUB', prediction, date_range, forecast_id)


def insert_forecast_values(query, currency, predictions, date_range, forecast_id):
    """ extracting predictions ... """
    print('inserting forecast values...')
    qry = None
    for i in range(len(predictions)):
        qry += '(\'' + str(date_range[i].date()) + '\', ' + '\'' + currency + '\', ' + str(forecast_id) + ', ' \
                 + str(round(predictions.iloc[i], 2)) + '),'

    res = db.insert_rows(query.replace('*', qry.rstrip(qry[-1])))
    LOGGER.info(f'{res} {currency} rows inserted into table forecast_rate')