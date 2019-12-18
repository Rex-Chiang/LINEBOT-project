import requests
from bs4 import BeautifulSoup as soup

class Crawler1:
    def __init__(self, constellation, date = ""):
        
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                   'Cookie':'PHPSESSID=abcdd57ec05363567c5aae5b5e8cc1e2; __BWfp=c1576639947961x518000b54; __lt__cid=40dbfb2a-bea7-4dbd-9df0-d0e8d714677f; __lt__sid=a29adf45-ba9e3457; _ga=GA1.3.2069145451.1576639956; _gid=GA1.3.1214579209.1576639956; FRIST_HTTP_HOST=astro.click108.com.tw; agreeGdprPop=1; _atrk_ssid=3NQKrFopKm3YfQhEuJEusB; _atrk_siteuid=DI3V464XQKVtPLAU; _fbp=fb.3.1576639956314.1889442373; enchantInitLang=1; _qg_fts=1576639948; QGUserId=3781736014835884; _qg_identified=true; _qg_cm=1; __asc=7c809bdc16f1710fe8f9ac2fc8a; __auc=7c809bdc16f1710fe8f9ac2fc8a; click108_buseekador=733aa2a2-7668-462e-883a-62ba2d3bf070-6f1661b2977b666c08e24a7056088e83; ieUpgradePop=1; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1576639988%2C%22lcsr%22%3A%22google%22%7D; _qg_pushrequest=true; m_VenderFrom=index_navbar_108; _gat=1; _gat_gtag_UA_4282017_13=1; m_VenderLastFrom=index_top_AST; appier_page_isView_2BZZaQdfDtX6TSr=983ec5333f76705b60a0cd06c89c051533191606311d986537fb72e25a725109; _atrk_sessidx=24; appier_pv_counter2BZZaQdfDtX6TSr=21',
                   'Connection':'keep-alive',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                   'Referer':'https://www.google.com/',
                   'Upgrade-Insecure-Requests':'1'}
        
        ConstellationsDict = {"牡羊":"0", "金牛":"1", "雙子":"2",
                              "巨蟹":"3", "獅子":"4", "處女":"5",
                              "天秤":"6", "天蠍":"7", "射手":"8",
                              "摩羯":"9", "水瓶":"10", "雙魚":"11"}
        
        num = ConstellationsDict[constellation]
        
        if date:
            url = "http://astro.click108.com.tw/daily_" + num + ".php?iAstro=" + num + "&iType=0&iAcDay=" + date
        else:
            url = "http://astro.click108.com.tw/daily_" + num + ".php?iAstro=" + num
            
        # 對網站發出請求
        html = requests.get(url, headers = headers)
        # 解析html
        self.page = soup(html.text,'html.parser')
    
    def Get_Contents(self):
        # 整理字串
        today_content = self.page.find('div',{'class':'TODAY_CONTENT'}).text.lstrip()
        today_content = today_content.replace("\n", "\n\n")   
        today_content = today_content.replace("：", ":"+"\n")
        # 取出幸運數及顏色
        today_lucky = self.page.find_all('div',{'class':'LUCKY'})
        lucky_number = today_lucky[0].text.strip()
        lucky_color = today_lucky[1].text.strip()
        
        result = today_content + "幸運色: " + lucky_color + "\n" + "幸運號碼: " + lucky_number
        
        return result
        
if __name__ == "__main__":
    crawler = Crawler1("射手", "2019-12-19")
    print(crawler.Get_Contents())