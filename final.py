import sqlite3
import pandas as pd
import folium
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.metrics import r2_score
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.optimize import curve_fit
# Exponential decay function: y = a * exp(-b * x)
def exp_decay(x, a, b):

   return a * np.exp(-b * x)



def analyze(conn):

    densities = [1,25,50,75,100]
    for dens in densities:
        x,y = getCoordinatesDensity(dens, 0, 10, 0, 1250)
        idx = np.argsort(x)
        x_sorted = x[idx]
        y_sorted = y[idx]

        params, _ = curve_fit(exp_decay, x_sorted, y_sorted, p0=(1, 0.01))
        a, b = params
        
        print("FOR DENSITY:" + str(dens))

        print("THIS IS A AND B")
        print(a)
        print(b)
        z = exp_decay(x_sorted, a, b)
        print("R^2:", r2_score(y_sorted,z))


#FINDINGS: INVERSE COORELATION FACTOR OF -0.57

def getPriceNumCriminals(conn, lowerX, upperX, lowerY, upperY):
    #print("IN GET PRICE")

    cursor = conn.cursor()
    cursor.execute("SELECT list_price, numCriminal FROM CAFINALTABLE")
    x = []
    y=  []
 

    results = cursor.fetchall()
    for price, numCriminal in results:
       
        if price and numCriminal:
            x.append(price/100000)
            y.append(numCriminal)
    
    
    x = (np.array(x))
    y = np.array(y)
    #mask = (x < upperX) & (y < upperY) & (x > 1)
    x1= x
    y1 = y
    


    return (x1,y1)
     





def getHistogram(conn):

    cursor = conn.cursor()
    x,y =  getPriceNumCriminals(conn,lowerX,upperX, lowerY, upperY)
    plt.hexbin(x, y, gridsize=40, cmap='viridis')
    plt.colorbar(label='count')
    plt.savefig("Histogram.png")

 



def getCoordinatesDensity(dens,lowerX, upperX, lowerY, upperY):
    plt.figure() 
    x,y =  getPriceNumCriminals(conn,lowerX,upperX, lowerY, upperY)
   
    xy = np.vstack([x, y])
    z = gaussian_kde(xy, bw_method=  0.1)(xy)
    
    percentiles = [1,25, 50, 75, 99]

    mask = z < np.percentile(z, dens)
    plt.scatter(x[mask], y[mask], c=z[mask], s=2)
    plt.savefig("DENSITY.png")

    return (x[mask], y[mask])
def relatePriceofHouseToCrim(conn,lowerX, upperX, lowerY, upperY):
   # print("IN RELATE *+")
    
    cursor = conn.cursor()
    cursor.execute("SELECT list_price, numCriminal FROM CAFINALTABLE")
    
    results = cursor.fetchall()
    plt.xlabel("PRICE(in 100000)")
    plt.ylabel("Number of Criminals")
    

    #print("THIS IS LOWERSX")
   # print(lowerX)
    #print(upperX)
    #print(lowerY)
    #print(upperY)



    x,y =  getPriceNumCriminals(conn,lowerX, upperX, lowerY, upperY)
    #print(x.size) 
    x = x[int(x.size/2): x.size]
    y = y[int(y.size/2): y.size]
    #print(max(x))
    #print(max(y))


    #print("THIS IS X:" + str(x))
    #print("THSI SIS Y:" + str(y))
    
    smooth = lowess(y, x, frac=0.25)
    #print("PERCENT")
    percents = (np.percentile(x, [0, 25, 50, 75, 90, 95, 99]))




    plt.scatter(x, y)
    #plt.plot(smooth[:,0], smooth[:,1], color='red', linewidth=2)
    plt.savefig("Scattered.png")

 
def getTableNames(conn):
    
    #print("HERE I AM CONNECTING")
    cursor = conn.cursor();

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';");

    res  = cursor.fetchall()
 
    for tab in res:
        print("THIS IS TABLE:" +str(tab[0]))
    
    req = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'CAFINALTABLE'";
    req ="PRAGMA table_info(CAFINALTABLE);"
    print("THESE ARE THE COLUMNS:i----------------")
    cursor.execute(req)
    results  = cursor.fetchall()
    print(results)

    print("-----------------------------")
    return res





def connectTable():

    conn = sqlite3.connect("HC.db")
    print("THIS IS CONN")
    print(conn)
    return conn

def getCoordinates():
    
    with open("Crime_Data_from_2020_to_Present.csv", newline = '') as f:
        reader = csv.reader(f)
    return reader



def getTable(conn, state):

    cursor = conn.cursor()
    res  = cursor.execute("SELECT * FROM CAFINALTABLE")
    
    results = res.fetchall()
    print(results[0])
    return res
    

def mapCoordinates(long, lat,numCriminal,m):
    folium.Marker([long, lat], popup="Cali").add_to(m)




def mapCriminal(conn):

    cursor = conn.cursor()
    cursor.execute("SELECT longitude,latitude, numCriminal FROM CAFINALTABLE")
    
    res =  cursor.fetchall()
     
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12) 
    #folium.Marker([38,-125], popup="Cali").add_to(m)
    #folium.Marker([38,-128], popup="Cali2").add_to(m)



    for result in res:
        
        long,lat,numCriminal = result
       # print(long)
        #print(lat)

        if long!= None and lat != None and numCriminal != None:
           #print("ENTERED")
            mapCoordinates(lat, long,numCriminal,m)

    m.save("map.html")


if __name__ == "__main__":
    print("IN MAIN")

    conn = connectTable()
   # getTableNames(conn)
   # mapCriminal(conn)
    print("BEFORE METHOD")
   # relatePriceofHouseToCrim(conn)
    #analyze(conn)
    #getHistogram(conn)
    relatePriceofHouseToCrim(conn, 0, 10, 0, 1250)
    getCoordinatesDensity(75,3.5, 5, 0, 1250)
    
    print("THIS IS THE FINAL ANALYSIS")

    analyze(conn) 
