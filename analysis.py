import folium

def mapCoordiates(long, lat):
    m = folium.Map(location=[long, lat], zoom_start=12)  # San Francisco
    folium.Marker([long, lat,criminal], popup="Cali").add_to(m)
    return m



def mapCriminal(conn):

    cursor = conn.cursor()
    cursor.execute("SELECT long,lat, numCriminals FROM CAFINALDATA")
    
    res =  cursor.fetchall()
    
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12) 

    for result in res:
        
        long,lat,_ = result
        m = mapCoordinates(long, lat)

    m.save("map.html")




