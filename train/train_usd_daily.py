import statsmodels.api as sm
from data.log import LOGGER

'''training a model to predict the exchange rate for a week ahead'''


def train_usd(df_currency_usd):
    try:
        print('start train usd')
        df_currency_usd.sort_values(by=['date'])
        df = df_currency_usd['value']
        sarima_model = sm.tsa.SARIMAX(df, trend='c', order=(2, 2, 1), seasonal_order=(1, 1, 0, 9))

        sarima_model.ssm.memory_no_filtered = True
        sarima_model.ssm.memory_no_gain = True
        sarima_model.ssm.memory_no_smoothing = True
        sarima_model.ssm.memory_no_std_forecast = True
        results_sarima = sarima_model.fit(return_params=True, low_memory=True)
        sarima_opt = sarima_model.filter(results_sarima)
        predict = sarima_opt.forecast(7, alpha=0.7)

        return predict

    except Exception as ex:
        LOGGER.error(ex)
