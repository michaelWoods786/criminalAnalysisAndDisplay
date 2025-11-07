import folium
import matplotlib.pyplot as plt



def mapCoordiates(long, lat):
    m = folium.Map(location=[long, lat], zoom_start=12)  # San Francisco
    folium.Marker([long, lat,criminal], popup="Cali").add_to(m)
    return m


def relatePriceofHouseToCrim():



    cursor.execute("SELECT price numCriminal density FROM CAFINALDATA")

    results = cursor.fetchall()

    for price, numCriminal in results;
    plt.scatter(x,y)
    plt.title("Price vs numberofCriminals")
    plt.show(()


def mapCriminal(conn):

    cursor = conn.cursor()
    cursor.execute("SELECT long,lat, numCriminals FROM CAFINALDATA")
    
    res =  cursor.fetchall()
    
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12) 

    for result in res:
        
        long,lat,_ = result
        m = mapCoordinates(long, lat)

    m.save("map.html")




