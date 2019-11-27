import pandas as pd
import numpy as np



def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="C:\\Users\\mkrabec\\csv.csv", type=str, help="Path of the file")
    args = parser.parse_args()

    file = args.f
    df = pd.read_csv(file)
    seznamka = ['Seznamka' in str(missing).split(',') or ' Seznamka' in str(missing).split(',') for missing in df['Jaké akce ti ve VKH chybí? '].to_list()]
    se_seznamkou = df[seznamka]
    muzi_se_seznamkou = se_seznamkou [se_seznamkou['Pohlaví'] == 'Muž']
    zeny_se_seznamkou = se_seznamkou [se_seznamkou['Pohlaví'] != 'Muž']



if __name__ == "__main__":
    main()