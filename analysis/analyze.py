import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
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

def recordStats(filename, model):
    print("THS IS ITHE FILENAME " + str(filename))
    pvals = model.pvalues
    with open(filename, "w") as file:
        for param in pvals.index:
            file.write(str(param)  + ":" +  str(pvals[param]))

       
        summary_str = str(model.summary())
        
        print("THIS IS THE FILE SUMMARAY I AM LOOKING FOR" + str(summary_str))

        for line in summary_str.split('\n'):
                        file.write(line + "\n")
    file.close()




def normalizeNumCrim():
    print("ENTERED")
    conn = sqlite3.connect("../HC.db")
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table';")
    print(cursor.fetchall())
    df = pd.read_sql_query("select * from CACRIMEANAL", conn)
    print(df.columns)
    df = df.dropna(subset=["latitude","longitude"])
    
    df["Density"] = df["population"].astype(float) / df["area"].astype(float)
    
    print(df["population"])

    print(df["Density"]) 
    #df_filtered = df[df["price"] < np.percentile(df["price"], 99)]
    print("*************") 
    print(np.percentile(df["sold_price"], 99))
    print("++++++++++++")
    
    df = df.dropna(subset=['latitude', 'longitude', 'sold_price' , 'Density', 'numCriminal'])
    coords = df[['latitude', 'longitude', 'sold_price', 'Density', 'numCriminal']]
    

    print(coords)


    coords_scaled = StandardScaler().fit_transform(coords)
    
    #inertias = []
    
    #print(coords_scaled)    

    kmeans = KMeans(n_clusters=4, random_state=42)
    
#    print(inertias)
    df["geo_cluster"] = kmeans.fit_predict(coords_scaled)
    df["crimePerDensity"] = df["numCriminal"] / df["Density"]



    model = smf.ols(
    "crimePerDensity ~ np.log(sold_price) * np.log( Density) +  C(geo_cluster)",
    data=df
    ).fit()
    

    recordStats("crimePerDensity.txt", model)

   
    df.to_sql(
    name="CATABLECluster",
    con=conn,
    if_exists="replace",   # or "append"
    index=False            # don’t write DataFrame index as a column
    )

    df["log_price"] = np.log(df["sold_price"])
    df["log_density"] = np.log1p(df["Density"])
    df["log_crime"] = np.log1p(df["crimePerDensity"])
    


    #here, we are recording crime as a function fo the log of the price and 
    #the log of the density. Additionally, we set C(city) and C(geo_cluster) as 
    #categorical variables in which the crime is dependent on 

    model = smf.ols(
    "log_crime ~ log_price + log_density + C(geo_cluster)",
    data=df
    ).fit()
    
    recordStats("crimeAsFunction.txt", model)        

    model = smf.ols(
    "numCriminal ~ (sold_price) + ( Density) + educationLevel +  C(geo_cluster)",
    data=df
    ).fit()

  
    model = smf.ols("numCriminal ~ log_price + log_density + educationLevel  +\
                    C(geo_cluster)", data=df).fit()

   
    
    recordStats("numCrimShallow.txt", model)

    model = smf.ols("numCriminal ~ log_price +  educationLevel +\
 + sqft  + C(geo_cluster)", data=df).fit()

    recordStats("numCriminalsRelation.txt",model)


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




