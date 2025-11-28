import sqlite3
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np


def exp_decay(x, a, b):

   return a * np.exp(-b * x)



def getGeoCluster(conn):
    conn = sqlite3.connect("../HC.db")
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table';")
    print(cursor.fetchall())
    df = pd.read_sql_query("select * from cafinaltable", conn)
    model = smf.ols(
    "numcriminal ~ np.log(sold_price) + density + c(zip_code)",
    data=df
    ).fit()
    print(model.params)






#compare the average price  of the houes in cluster 1,  to the average price of
#the houses in cluster 3




def normalizeNumCrim():
    print("ENTERED")
    conn = sqlite3.connect("../HC.db")
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table';")
    print(cursor.fetchall())
    df = pd.read_sql_query("select * from CAFINALTABLE", conn)
    print(df.columns)
    df = df.dropna(subset=["latitude","longitude"])
  
    
    #df_filtered = df[df["price"] < np.percentile(df["price"], 99)]
    print("*************") 
    print(np.percentile(df["sold_price"], 99))
    print("++++++++++++")

    coords = df[["latitude","longitude"]]
    coords_scaled = StandardScaler().fit_transform(coords)
    kmeans = KMeans(n_clusters=15, random_state=42)
    df["geo_cluster"] = kmeans.fit_predict(coords_scaled)
    df["crimePerDensity"] = df["numCriminal"] / df["Density"]



    model = smf.ols(
    "crimePerDensity ~ np.log(sold_price) * np.log( Density) + C(city) +  C(geo_cluster)",
    data=df
    ).fit()
    print(model.params)
    print(model.rsquared_adj)
    df.to_sql(
    name="CATABLECluster",
    con=conn,
    if_exists="replace",   # or "append"
    index=False            # don’t write DataFrame index as a column
    )

    result=  cursor.execute("SELECT  * FROM CATABLECluster WHERE\
                            geo_cluster == 1")
     
    
    df["log_price"] = np.log(df["sold_price"])
    df["log_density"] = np.log1p(df["Density"])
    df["log_crime"] = np.log1p(df["crimePerDensity"])
    print("HERE I AM &&&&&&&&&&&")
    model = smf.ols(
    "log_crime ~ log_price + log_density + C(city) + C(geo_cluster)",
    data=df
    ).fit()
    
    with open("finalSummary.txt") as f:
        f.write(model.summary())
        f.write(model.params)
        f.write(model.rsquared_adj)


    f.close()
    
    



    pvals = model.pvalues
    for param in pvals.index:
        if "log_price" in param or "log_density" in param:
            print(param, ":", pvals[param])




def anaylze(conn):
    densities = [1,25,50,75,100]
    for dens in densities:
        x,y = getCoordinatesDensity(conn,dens, 0, 10, 0, 1250)
        idx = np.argsort(x)
        x_sorted = x[idx]
        y_sorted = y[idx]

        params, _ = curve_fit(exp_decay, x_sorted, y_sorted, p0=(1, 0.01))
        a, b = params
        z = exp_decay(x_sorted, a, b)
        print("R^2:", r2_score(y_sorted,z))



def getHistogram(conn):

    cursor = conn.cursor()
    x,y =  getPriceNumCriminals(conn,lowerX,upperX, lowerY, upperY)
    plt.hexbin(x, y, gridsize=40, cmap='viridis')
    plt.colorbar(label='count')
    plt.savefig("Histogram.png")

 
def getCoordinatesDensity(conn, dens,lowerX, upperX, lowerY, upperY):
    plt.figure() 
    x,y =  getPriceNumCriminals(conn,lowerX,upperX, lowerY, upperY)
   
    xy = np.vstack([x, y])
    z = gaussian_kde(xy, bw_method=  0.1)(xy)
    
    percentiles = [1,25, 50, 75, 99]

    mask = z < np.percentile(z, dens)
    plt.scatter(x[mask], y[mask], c=z[mask], s=2)
    plt.savefig("DENSITY.png")

    return (x[mask], y[mask])








def getPriceNumCriminals(conn, lowerX, upperX, lowerY, upperY):
    print("IN GET PRICE")

    cursor = conn.cursor()
    cursor.execute("SELECT list_price, numCriminal FROM criminalTab")
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
    

    print("MINS")
    print(min(x1))
    print(min(y1))
    
    with open("file.txt", "w") as f:
        
        for i in range(len(x1)):
            f.write(str(x1[i]) + "," + str(y1[i]) + "\n")




    return (x1,y1)
     
def relatePriceofHouseToCrim(conn,lowerX, upperX, lowerY, upperY):
    print("IN RELATE *+")
    
    cursor = conn.cursor()
    cursor.execute("SELECT price, numCriminal FROM crimTab")
    
    results = cursor.fetchall()
    plt.xlabel("PRICE(in 100000)")
    plt.ylabel("Number of Criminals")
    

    print("THIS IS LOWERSX")
    print(lowerX)
    print(upperX)
    print(lowerY)
    print(upperY)



    x,y =  getPriceNumCriminals(conn,lowerX, upperX, lowerY, upperY)
    print(x.size) 
    x = x[int(x.size/2): x.size]
    y = y[int(y.size/2): y.size]
    print(max(x))
    print(max(y))


    print("THIS IS X:" + str(x))
    print("THSI SIS Y:" + str(y))
    
    smooth = lowess(y, x, frac=0.25)
    print("PERCENT")
    percents = (np.percentile(x, [0, 25, 50, 75, 90, 95, 99]))

    #HERE, WE ARE SCATTERING THE COORDINATES. WITH SCATTERIGN THE COORDINAATES<
    #WER are able to see the relationship


    plt.scatter(x, y)
    plt.savefig("Scattered.png")

 
    
#this method maps the coordinates, with a popup "Balt"
def mapCoordinates(long, lat,numCriminal,m):
    folium.Marker([long, lat], popup="Balt").add_to(m)



#this method willl map the criminal, and list the lognitude and lattiude of
#address along with the number of criminals nearby
def mapCriminal(conn):

    cursor = conn.cursor()
    cursor.execute("SELECT longitude,latitude, numCriminal FROM crimTab")
    
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


 

normalizeNumCrim()




