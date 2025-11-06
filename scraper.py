import sqlite3
import pandas as pd
import folium


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
    folium.Marker([38,-125], popup="Cali").add_to(m)
    folium.Marker([38,-128], popup="Cali2").add_to(m)



    for result in res:
        
        long,lat,numCriminal = result
        print(long)
        print(lat)

        if long!= None and lat != None and numCriminal != None:
            print("ENTERED")
            mapCoordinates(lat, long,numCriminal,m)

    m.save("map.html")


if __name__ == "__main__":
    print("IN MAIN")

    conn = connectTable()
    getTableNames(conn)
    mapCriminal(conn)
