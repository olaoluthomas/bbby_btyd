# -*- coding: utf-8 -*-
import pandas as pd
import re
from lifetimes import ModifiedBetaGeoFitter, GammaGammaFitter

output_file = 'predictions.csv'

def snakify(column_name):
    """
    Function to convert pandas column names into snake case.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', column_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def load_params(mbg_, ggf_):
    """
        Load model parameters.
    """
    mbg = ModifiedBetaGeoFitter()
    ggf = GammaGammaFitter()
    mbg.load_model(mbg_)
    ggf.load_model(ggf_)
    return mbg, ggf


def load_data(file):
    """
    Load dataset as a pandas dataframe from csv.
    """
    data = pd.read_csv(file)
    data.columns = [
        snakify(col) if col not in ('T_CAL', 'T_cal') else 'T_cal'
        for col in data.columns
    ]
    key = 'customer_id'
    data[key] = data[key].astype("object")
    return data


def alive(data, mbg):
    """
    Predict likelihood of customers to be active purchasers
    """
    return mbg.conditional_probability_alive(data['frequency_cal'],
                                             data['recency_cal'],
                                             data['T_cal'])


def ltv_predict(data, mbg, ggf, discount_rate, time):
    """
    Predict dollar value of customers from today up to time t.
    """
    return ggf.customer_lifetime_value(mbg,
                                       data['frequency_cal'],
                                       data['recency_cal'],
                                       data['T_cal'],
                                       data['monetary_value'],
                                       time=time,
                                       discount_rate=discount_rate)


def run_model(input_file, mbg_pkl, ggf_pkl, t, r):
    """
    Initialize model, run predictions, and save output to file.

    Args:

    """
    mbg, ggf = load_params(mbg_pkl, ggf_pkl)
    data = load_data(file=input_file)
    data['alive'] = alive(data, mbg)
    data['prediction'] = ltv_predict(data, mbg, ggf, time=t, discount_rate=r)
    data[['customer_id', 'alive', 'prediction']].to_csv(output_file,
                                                        index=False,
                                                        encoding='utf-8')