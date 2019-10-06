import pandas as pd
import datetime
import re

def get_this_week_names(csv_file, na=1):
    data = pd.read_csv(csv_file)
    data = data[data['Člen VKH']=='ano']
    narozeniny = data[['Jméno','Datum narození']]
    
    for offset in range(na):
        
        day_of_week = (datetime.datetime.today().weekday() + offset*7) % 7
        currentDay = (datetime.datetime.now() + datetime.timedelta(days=offset*7)).day
        currentMonth= (datetime.datetime.now()+ datetime.timedelta(days=offset*7)).month 
        today = datetime.datetime.strptime("{}/{}".format(currentMonth,currentDay), '%m/%d')
        #today = datetime.datetime.today().weekday()
        streda = 2
        lower = (7  + day_of_week - streda - 1) % 7
        upper = (7 + streda - day_of_week) % 7
        minula_streda = today - datetime.timedelta(days=lower)
        pristi_streda = today + datetime.timedelta(days=upper)
        
        
        oslavenci = []
        for _, row in narozeniny.iterrows():
            jmeno = row[0]
            narozeni =  try_lomeno_format(str(row[1]))
            
            if narozeni and narozeni>=minula_streda and narozeni<=pristi_streda:
                oslavenci.append(jmeno)
        if not oslavenci:
            oslavenci.append("Nikdo")
        print("Mše {}.{}.".format(pristi_streda.day , pristi_streda.month))
        print ("V týdnu od {}.{}. do {}.{}. oslavili:".format(minula_streda.day , minula_streda.month, pristi_streda.day , pristi_streda.month))
        print(*oslavenci)
        print()

    
        
def try_lomeno_format(datum):
    splited = datum.split('/')
    if len(splited) == 3:
        return datetime.datetime.strptime(splited[1]+'/'+splited[2], '%m/%d')
    else:
        return None
        
        

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", default="C:\\Users\\miros\\downloads\\clenove.csv", type = str)
    
    args = parser.parse_args()
    get_this_week_names(args.csv_file, na=22)