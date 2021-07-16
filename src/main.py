# -*- coding: utf-8 -*-
from flask import Flask
from utils import scorer

input_file = "data.csv"
mbg_pkl = "mbg.pkl"
ggf_pkl = "ggf.pkl"
t = 12
r = 0.00764

app = Flask(__name__)
@app.route("/")
def main():
    scorer.run_model(input_file, mbg_pkl, ggf_pkl, t, r)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)