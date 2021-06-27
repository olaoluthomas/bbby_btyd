# -*- coding: utf-8 -*-
from utils import scorer

input_file = "data.csv"
output_file = "predictions.csv"
mbg_pkl = "mbg.pkl"
ggf_pkl = "ggf.pkl"
t = 12
r = 0.00764

def main():
    scorer.run_model(input_file, mbg_pkl, ggf_pkl, t, r)


if __name__ == '__main__':
    main()