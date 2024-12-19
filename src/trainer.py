# -*- coding: utf-8 -*-
import logging
import re
import pandas as pd
from lifetimes import ModifiedBetaGeoFitter, GammaGammaFitter
from sklearn.metrics import mean_absolute_error
from src.utils import logging

logger = logging.get_logger()


# class ltv_trainer(self) -> None:
#     def __init__(self, model_dir=None, penalty=None):
#         if penalty:
#             self._mbg = ModifiedBetaGeoFitter(penalizer_coef=penalty)
#             self._ggf = GammaGammaFitter(penalizer_coef=penalty)
#         else:
#             self._mbg = ModifiedBetaGeoFitter()
#             self._ggf = GammaGammaFitter()

#     def load_data(self, data_path):
#         data = pd.read_csv(data_path) # what checks are reqd?

#     def train_mbg(self):


def load_data(data_path):
    """Load dataset into a pandas dataframe from csv.
    The data should have the following columns:
        customer_id: key
        frequency_cal: # of unique days of txn.
        recency_cal: # of days between first and last txn.
        T_cal: # of days between first txn and last day of time period.
        monetary_value: avg. product margin (per txn)
    """
    data = pd.read_csv(data_path)  # I need to set up ingestion from cloud storage / BQ
    logging.info('Data loaded to pandas DF.')
    if 'customer_id' in data.columns.tolist():
        data['customer_id'] = data['customer_id'].astype("object")
    return data


def mbg_fitter(data, penalty=0.1):
    """
    Fit calibration data to derive Modified BG/NBD parameters.
    """
    mbg = ModifiedBetaGeoFitter(penalizer_coef=penalty)
    mbg.fit(data['frequency_cal'], data['recency_cal'], data['T_cal'])
    logging.info('MBG parameters fit on training data.')
    return mbg


def ggf_fitter(data, penalty=0):
    """
    Fit repeat calibration data to derive Gamma Gamma mixing parameters.
    """
    ggf = GammaGammaFitter(penalizer_coef=penalty)
    ggf.fit(data['frequency_cal'], data['monetary_value'])
    logging.info('Gamma Gamma parameters fit on repeat customer data.')
    return ggf


def training_error(repeat, ggf):
    """
    Save error in repeat-customer average profit estimation.
    """
    return mean_absolute_error(
        repeat['monetary_holdout'].mean(),
        ggf.conditional_expected_average_profit(repeat['frequency_cal'],
                                                repeat['monetary_value']).mean,
    )


def save_pickle(mbg, ggf):
    """
    Save Modified BG/NBD & GG parameters to pickle files.
    """
    mbg.save_model('mbg.pkl', save_date=False, save_generate_data_method=False)
    ggf.save_model('ggf.pkl', save_date=False, save_generate_data_method=False)
    logging.info('Model shape and scale parameters saved to file.')


def run_training(train_data):
    data = load_data(data=train_data)
    mbg = mbg_fitter(data=data)
    repeat = data[data['frequency_cal'] > 0]
    repeat.loc[repeat['monetary_value'] <= 0, ['monetary_value']] = 0.0001
    # checking the independence assumption
    p_corr = repeat[['frequency_cal', 'monetary_value'
                     ]].corr()['frequency_cal']['monetary_value']
    if abs(p_corr) < 0.1:
        ggf = ggf_fitter(data=repeat)
        print(
            "Expected conditional average profit: %s, Average future profit: %s"
            % (round(
                ggf.conditional_expected_average_profit(
                    repeat['frequency_cal'], repeat['monetary_value']).mean(),
                2), round(repeat['monetary_holdout'].mean(), 2)))
        absolute_val_error = save_training_error(
            repeat=repeat, ggf=ggf)  # how to spit this out to console
        save_pickle(mbg=mbg, ggf=ggf)
        # better yet, save error to file or print to console...
        return absolute_val_error
    else:
        logging.warning(
            "Pearson correlation co-efficient {} appears to be too high (independence assumption violated...)"
            .format(round(p_corr, 5)))
