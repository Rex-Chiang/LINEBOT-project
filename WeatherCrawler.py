import requests
import json
from bs4 import BeautifulSoup as soup

class Crawler3:
    def __init__(self, location):
        
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                   'Cookie':'fbm_355863885083166=base_domain=; TS01dbf791=0107dddfefd0a47165637cc243981e66bfce6384f2586041a683ae0efa88ae11356a99eeae',
                   'Connection':'keep-alive',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                   'Host':'opendata.cwb.gov.tw',
                   'Upgrade-Insecure-Requests':'1'}
        
        Authorization = "CWB-6DF4F34D-3A8E-400C-B68E-B71D462F50B2"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + Authorization + "&locationName=" + location
            
        # 對網站發出請求
        html = requests.get(url, headers = headers)
        # 解析html
        self.page = soup(html.text,'html.parser')
        
        
    def Get_Weather(self):
        page_json = json.loads(str(self.page))
        data = page_json["records"]
        
        title = data["location"][0]["locationName"] +"\n"+ data["datasetDescription"] +"\n\n"
        Wx = data["location"][0]["weatherElement"][0]        
        WxDate = ["Date & Time:\n" + Wx["time"][x]["startTime"][:-3] + " to " + Wx["time"][x]["endTime"][:-3] +"\n"for x in range(3)]
        WxDescription = ["Description:\n" + Wx["time"][x]["parameter"]["parameterName"] +"\n" for x in range(3)]
        
        PoP = data["location"][0]["weatherElement"][1]
        PopDescription = ["Probability of Precipitation:\n" + PoP["time"][x]["parameter"]["parameterName"] + "%\n" for x in range(3)]
        
        MinT = data["location"][0]["weatherElement"][2]    
        MinDescription = ["Minimum temperature:\n" + MinT["time"][x]["parameter"]["parameterName"] + "°C\n" for x in range(3)]
        
        MaxT = data["location"][0]["weatherElement"][4]    
        MaxDescription = ["Maximum  temperature:\n" + MaxT["time"][x]["parameter"]["parameterName"] + "°C\n" for x in range(3)]
        
        CI = data["location"][0]["weatherElement"][3]
        CiDescription = ["Comfort index:\n" + CI["time"][x]["parameter"]["parameterName"] +"\n\n"for x in range(3)]
        
        WeatherContent = title
        Content = [WxDate[x] + WxDescription[x] + PopDescription[x] + MinDescription[x] + MaxDescription[x] + CiDescription[x] for x in range(3)]
        
        for i in range(3):
            WeatherContent += Content[i]
        
        return WeatherContent.rstrip()
    
if __name__ == "__main__":
    crawler = Crawler3("臺北市")
    print(crawler.Get_Weather())