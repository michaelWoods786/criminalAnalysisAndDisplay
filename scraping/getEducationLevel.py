import pandas as pd
import sqlite3
import requests
def get_county_fips(lat, lon):
    ron = requests.get(
        "https://geocoding.geo.census.gov/geocoder/geographies/coordinates",
        params={
            "x": lon,
            "y": lat,
            "benchmark": "Public_AR_Current",
            "vintage": "Current_Current",
            "format": "json"
        }
    ).json()
    
    print(ron)
    print("THESE ARE THE KEYS")
    print(ron.keys()) 
    

    if "result" in ron.keys():

        print("THIS IS THE RESULT")
        county = ron["result"]["geographies"]["Counties"][0]["COUNTY"]
        state  = ron["result"]["geographies"]["Counties"][0]["STATE"]
        tract  = ron["result"]["geographies"]["Census Tracts"][0]["TRACT"]

        return county
    else:
        return None
def toPandas(conn,query):

    cursor = conn.cursor()
    df = pd.read_sql_query(query, conn)
    return df

def getEducationByLat(lat, lon):

    url = "https://api.census.gov/data/2022/acs/acs5"
    county = get_county_fips(lat, lon)
    print("THIS IS THE COUNTY:" + str(county))  
    
    if county != None:

        params = {
        "get": "B15003_001E,B15003_017E,B15003_018E,B15003_019E,B15003_020E",
        "for": "tract:*",
        "in": f"state:06 county:{county}"  # example: Baltimore City
        }
        response = requests.get(url, params=params)
        data = response.json()

        print("THIS SI THE RESPOINSE" + str(response) )
        
        header = data[0]
        first_row = data[1]

        total = int(first_row[0])
        bach  = int(first_row[1])
        mast  = int(first_row[2])
        prof  = int(first_row[3])
        doc   = int(first_row[4])
        ret  =  (bach + mast + prof + doc) / total
        print(str(ret))
        return (county, (bach + mast + prof + doc) / total)
    else:
        return None


def getEducation(conn):
    
    cursor = conn.cursor()
    df = toPandas(conn, "SELECT  *  from CAFINALTABLE") 
    seen = []
    for index,row in df.iterrows():
        
        if row["county"] not in seen:
            check = getEducationByLat(row["latitude"], row["longitude"])
            if check != None:
                _ ,educationLevel= check
                
                print("THIS IS THE EDUCATIONLEVEL" + str(educationLevel))
                if row["county"] not in seen:
                    seen.append(row["county"])
                query = "UPDATE CAFINALTABLE SET educationLevel = ? WHERE county = ?"
                print("-----------------------")
                cursor.execute(query, (educationLevel, row["county"]))
                print("------------------------")
                conn.commit()
conn = sqlite3.connect("../HC.db")
getEducation(conn)





