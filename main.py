# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template
import pandas as pd
import os
from utils.scorer import load_params, ltv_predict

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
    Load model parameters and score HTML form input.
    '''
    if request.method == 'GET':
        return Response("Click on the 'User Input' link to get a demo.")

    if request.method == 'POST':
        # Check for presence of pickle files and then load HTML form.
        mbg, ggf = load_params("mbg.pkl", "ggf.pkl")
        print('Model parameters loaded successfully.')
        # pick up inputs from HTML form
        input_row = pd.DataFrame(columns=[
            'frequency_cal', 'recency_cal', 'T_cal', 'monetary_value'
        ])
        input_row.loc[0] = [x for x in request.form.values()]
        for col in input_row.columns:
            if col in ['frequency_cal', 'recency_cal', 'T_cal']:
                input_row[col] = input_row[col].astype('int')
        # score data from filled HTML form and send prediction
        output = ltv_predict(input_row,
                             mbg=mbg,
                             ggf=ggf,
                             discount_rate=0.00764,
                             time=12)
        return render_template('demo_result.html', output=round(output[0], 2))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))