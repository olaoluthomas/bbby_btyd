# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import pandas as pd
import os
from xform.scorer import load_params, ltv_predict, run_model

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/user_input")
def user_input():
    return render_template('user_input.html')


@app.route("/demo", methods=['GET', 'POST'])
def demo():
    '''
    Load model parameters and score population file OR score HTML form input.
    '''
    mbg, ggf = load_params("mbg.pkl", "ggf.pkl")
    t = 12
    d = 0.00764
    if request.method == 'GET':
        for file in os.listdir('./data'):
            if file.endswith('to_score.csv'):
                data_file = file  # how do you make sure you have a single "to_score" file?
        run_model('./data/'+data_file, mbg=mbg, ggf=ggf, t=t, r=d)
        return render_template('train_score.html')

    if request.method == 'POST':
        # pick up inputs from HTML form
        input_row = pd.DataFrame(columns=[
            'frequency_cal', 'recency_cal', 'T_cal', 'monetary_value'
        ])
        input_row.loc[0] = [x for x in request.form.values()]
        for col in input_row.columns:
            if col in ['frequency_cal', 'recency_cal', 'T_cal']:
                input_row[col] = input_row[col].astype('int')
            else:
                input_row[col] = input_row[col].astype('float')
        # score data from filled HTML form and send prediction
        output = ltv_predict(input_row,
                             mbg=mbg,
                             ggf=ggf,
                             discount_rate=d,
                             time=t)
        return render_template('demo_result.html', output=round(output[0], 2))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))