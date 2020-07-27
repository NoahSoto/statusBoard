from bs4 import BeautifulSoup
import requests
import weathercom
from _datetime import datetime, timedelta
import json

#def updateBoard(): #NOT DONE
start_date=str(datetime.date(datetime.now())).split("-")
end_date=start_date

###
#ide Predictions: /api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20200726&end_date=20200727&datum=MLLW&station=8637624&time_zone=lst_ldt&units=english&interval=hilo&format=json
###

def loading(loadingWhat):
    print("Getting "+loadingWhat, end="")
    for i in range(100):
        print(".", end="")
    print("\n")

def getTides(loadingWhat): #DONE AND UPDATING
    loading(loadingWhat)
    #JC=8636735
    #GW=8636142
    #GP=8637624
    areas={"JC":"8636735","GW":"8636142","GP":"8637624"}
    for key in areas.keys():
        tidesURL = requests.get("https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date={0}{1}{2}&end_date={0}{1}{2}&datum=MLLW&station={3}&time_zone=lst_ldt&units=english&interval=hilo&format=json".format(start_date[0], start_date[1], start_date[2],areas[key]))
        result=tidesURL.content
        jsonData=json.loads(result)

        print(jsonData["predictions"])


        #print(json.dumps(jsonData))

        #print("Tides for " + key + " are : \n"+str(result))
    print("\n")
def getAirTemp(loadingWhat): #NOT DONE
    loading(loadingWhat)


    query="\"temperature\""
    weatherDetailsJSON = weathercom.getCityWeatherDetails("Gwynn, Virginia")
    jsonData=json.loads(weatherDetailsJSON)
    temp=int(jsonData["vt1observation"]["temperature"])

    temp=(temp*9/5 + 32)
    print("AIR TEMP(at gwynn island, virginia) : {0}".format(temp)+"\n")
def getWaterTemp(loadingWhat):
    loading("Air Temp/Speed/Direction Water Temp (Data collected from stingray point)")
    url=requests.get("https://buoybay.noaa.gov/locations/stingray-point")
    src=url.content
    soup=BeautifulSoup(src,'html.parser')


    #print(src)
    table=soup.find("table")
    table_row=table.find_all("tr")

    #counter=0
    rows=[]

    for table in table_row:
        td=table.find_all("td")
        for i in td:
            #print(i.text)
            rows.append(i.text)
    index=rows.index("Significant Wave Height")

    print("Data Collecion Time : " + rows[5])
    print("Water Temperature: "+ rows[73])
    print("Wind Direction: " + rows[87]+" "+rows[88])
    print("Wind Speed "+ rows[94] + " "+ rows[95])
    print("Wave Height "+ rows[52]+ " " + rows[53])

    #print(rows)
    #print(counter)
    #print(data.content)

def getSunSet(loadinWhat):
    loading(loadinWhat)
    url=requests.get("https://api.sunrise-sunset.org/json?lat=37.504860&lng=-76.280610")
    jsonData=json.loads(url.content)
#####SUNRISE####
    sunrise_list=jsonData["results"]["sunrise"].split(" ")
    sunrise=sunrise_list[0]
    #print(sunrise)
    target1=datetime.strptime(sunrise,"%H:%M:%S")
    target_list=target1-timedelta(hours=4)
    good=str(target_list).split(" ")
    print("Sunrise is at "+good[1])
#####SUNSET######
    sunset_list=jsonData["results"]["sunset"].split(" ")
    sunset=sunset_list[0]
    #print(sunrise)
    target2=datetime.strptime(sunset,"%H:%M:%S")

    target_list2=target2-timedelta(hours=4)
    good2=str(target_list2).split(" ")
    print("Sunset is at "+good2[1])


    #print(jsonData)




getAirTemp("Air Temperature")
getTides("Tide Information")
getWaterTemp("Water Temperature")
getSunSet("Sun Set Times")