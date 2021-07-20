# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import pandas as pd
import os
from utils import trainer, scorer

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def btyd():
    if request.method == 'GET':
        '''
        Train model and score population data.
        '''
        trainer.run_training()  # check that training completed successfully
        print('Model trained successfully.')
        mbg_pkl = "mbg.pkl"
        ggf_pkl = "ggf.pkl"
        input_file = "data.csv"  # point input to bq table/content of cloud storage (with arg_parse?)
        t = 12
        r = 0.00764
        # set it up such that predictions are dumped to BQ/ Cloud storage
        scorer.run_model(input_file, mbg_pkl, ggf_pkl, t, r)
        return Response(
            'Model run on supplied data and predictions saved to output table/directory'
        )

    if request.method == 'POST':
        '''
        Load model parameters and score HTML form input.
        '''
        # Check for presence of pickle files and then load HTML form.
        mbg_pkl = "mbg.pkl"
        ggf_pkl = "ggf.pkl"
        print('Model parameters loaded successfully.')
        # pick up inputs from HTML form
        input_row = pd.DataFrame([x for x in request.form.values()],
                                 columns=[
                                     'frequency_cal', 'recency_cal', 'T_cal',
                                     'monetary_value'
        ])
        # score data from filled HTML form and send response
        output = scorer.ltv_predict(input_row,
                                    mbg_pkl,
                                    ggf_pkl,
                                    discount_rate=0.00764,
                                    time=12)
        return Response('Customer NPV: $', round(output, 2))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))