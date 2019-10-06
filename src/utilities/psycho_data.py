'''
Created on 22. 12. 2018

@author: miros
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as sm
from statsmodels.api import add_constant
import os

TIME = 'mouse_target.time'

def show_plot(csv_files, x_axis, title):
    for file in csv_files:
        data = pd.read_csv(os.path.join(args.dir,file))
        
        data = data[data[TIME] <= 2]
        avg_times = data.groupby([x_axis]).mean()[TIME]      
        avg_times.plot()
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel('Average response time')
    plt.legend([file.split('_')[0] for file in csv_files])
    plt.show()
    
def show_regresion(csv_files, x_axis, title):
    for file in csv_files:
        data = pd.read_csv(os.path.join(args.dir,file))
        
        data = data[data[TIME] <= 2]
        x = data[x_axis]
        y = data[TIME]
        
        x_agg = sorted(data[x_axis].unique())
        lr = LinearRegression()
        lr.fit(x, y)
        predictions = lr.predict(x_agg)
        plt.plot(x, predictions)
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel('Average response time - linear regression')
    plt.legend([file.split('_')[0] for file in csv_files])
    plt.show()
    
def sklearn_regression(csv_files, x_axis):
    for file in csv_files:
        data = pd.read_csv(os.path.join(args.dir,file))
        
        data = data[data[TIME] <= 2]
        x = data[x_axis]
        y = data[TIME]
        x = sorted(data[x_axis].unique())
        y = data.groupby([x_axis]).mean()[TIME] 
        
        fit_and_print(file,x, y)
        
        
        
        
def fit_and_print(file,x,y):
    
    #x= np.array(x).reshape((-1, 1))
    #x = np.concatenate((x, np.ones(x.shape)), axis=1)
    x = add_constant(x)
    model=sm.OLS(y, x)
    fitted = model.fit()
    #print(fitted.summary())
    summary = str(fitted.summary()).splitlines()
    
    print(file,summary[3].split()[-1])

    
       
def show_fitt(csv_files, title):
    for file in csv_files:
        data = pd.read_csv(os.path.join(args.dir,file))
        data = data[data[TIME] <= 2]
        data['new'] = 2*data['distance'] / data['size']
        plt.scatter(data['new'],data[TIME])
        avg_times = data.groupby(['new']).mean()[TIME] 
        #avg_times = data.groupby(['distance','size']).mean()[TIME] 
        #print(avg_times)
        x = data['new']
        
        #x = []
        #for dist in [100*x for x in range(1,6)]:
        #    for size in [100*x for x in range(1,5)]:
        #        x.append((dist,size))
        #print(np.array(x))
        #x = np.array(x)
        #print(x.shape)
        y = avg_times
        x = sorted(x.unique())
        
        #x= np.log2(x)
        coef = np.polyfit(x, y, 1)
        a = [coef[0]*x+coef[1] for x in x]
        plt.plot(x, a)
        
        #print(x_agg)
        #print(y)
        
        fit_and_print(file, x, y)
        plt.show()
    
def compute_variance(csv_file):
    for file in csv_files:     
        data = pd.read_csv(os.path.join(args.dir,file))  
        data = data[data[TIME] <= 2]
        avg_times = data.groupby(['distance', 'size', 'direction']).std()[TIME]
        #print(avg_times)    
        print(avg_times.mean())
        
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="C:\\users\\miros\\downloads\\data", type=str, help="Path of the downloaded image")
    args = parser.parse_args()
    csv_files = [ file for file in os.listdir(args.dir) if file.split('.')[-1] == 'csv']
    #show_plot(csv_files, 'distance', "Figure 1")
    #show_plot(csv_files, 'size', 'Figure 2')
    #show_plot(csv_files, 'direction', 'Figure 3')
    #sklearn_regression(csv_files, 'distance')
    #sklearn_regression(csv_files, 'size')
    #sklearn_regression(csv_files, 'direction')
    #show_regresion(csv_files, 'distance', "Figure 4")
    #show_regresion(csv_files, 'size', "Figure 5")
    #show_regresion(csv_files, 'direction', "Figure 6")
    show_fitt(csv_files, "Figure 4")
    #compute_variance(csv_files)