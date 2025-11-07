import sqlite3
import pandas as pd
import folium
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score


def analyze(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT list_price, numCriminal FROM CAFINALTABLE")
    results = cursor.fetchall()
    x = []
    y = [] 

    z = []
    for result in results:
        if result[1] != None and result[0] != None:
            x.append(result[0]/100000)
            y.append(result[1])
            z.append(1/  (result[0]/100000))  
         
    np.array([1,2,3])
 
    print("R^2:", r2_score(np.array(y),np.array( z)))


#FINDINGS: INVERSE COORELATION FACTOR OF -0.57


def relatePriceofHouseToCrim(conn):
    print("IN RELATE")
    
    cursor = conn.cursor()
    cursor.execute("SELECT list_price, numCriminal FROM CAFINALTABLE")
    
    results = cursor.fetchall()
    plt.xlabel("PRICE(in 100000)")
    plt.ylabel("NumCriminals")
    for price, numCriminal in results:
        
        print("THSI SI THE PRICE")
        print(price)
        print("THIS IS NUM CRIMINALS")
        print(numCriminal)
    
        plt.scatter(price/100000,numCriminal)
            
    


    plt.title("Price vs numberofCriminals")
    plt.savefig("scatter_plot.png")
    
    plt.xlim(0, 20)
    plt.savefig("zoomedIn.png")




def getTableNames(conn):
    
    print("HERE I AM CONNECTING")
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
    analyze(conn)
