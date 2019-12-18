import requests
import random
from bs4 import BeautifulSoup as soup

class Crawler:
    def __init__(self):
        
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                   'Cookie':'pilot_happix_noti_showed_timestamp=1576112833618; _pta=CgEBHF3rEIiOnwqXGBLGAgP=; __auc=6657798f16edee02c95bd79f728; is_obstruct=1; AviviD_uuid=efff1da6-d339-4a3e-9b60-453521143567; webuserid=d08eaed0-eaf6-2528-5d56-5307edca0b35; _ym_uid=1575730343949863108; _ym_d=1575730343; _gid=GA1.2.703652420.1576557712; _ym_isad=1; PIXFRONTID=rc25l5p12791o5b2gfchuid2d4; uid=AAAAAF36GY8AADGbBfAVAg==; preferences=null; __asc=a682532716f18f3e25ed4e2d059; _ga=GA1.3.1786818810.1575697263; _gid=GA1.3.703652420.1576557712; _ym_visorc_54775048=b; mp_de68fb7561d61e2fa21b5d584e246ede_mixpanel=%7B%22distinct_id%22%3A%20%2216ee0d8e7bb2d2-0f38068eb82e97-2393f61-e1000-16ee0d8e7bc1c4%22%2C%22%24device_id%22%3A%20%2216ee0d8e7bb2d2-0f38068eb82e97-2393f61-e1000-16ee0d8e7bc1c4%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fabcian.pixnet.net%2Fblog%2Fpost%2F35273384%22%2C%22%24initial_referring_domain%22%3A%20%22abcian.pixnet.net%22%2C%22%24search_engine%22%3A%20%22google%22%7D; mp_9bf666011f2e0d6e333f9bfa242d0c21_mixpanel=%7B%22distinct_id%22%3A%20%2216ee0d8e7ca5b-0e398516f4c549-2393f61-e1000-16ee0d8e7cb2a8%22%2C%22%24device_id%22%3A%20%2216ee0d8e7ca5b-0e398516f4c549-2393f61-e1000-16ee0d8e7cb2a8%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fabcian.pixnet.net%2Fblog%2Fpost%2F35273384%22%2C%22%24initial_referring_domain%22%3A%20%22abcian.pixnet.net%22%2C%22%24search_engine%22%3A%20%22google%22%7D; _ga=GA1.1.1786818810.1575697263; _ga_EKWP9V58TJ=GS1.1.1576671635.14.1.1576671667.0',
                   'Connection':'keep-alive',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                   'Referer':'https://douze.pixnet.net/blog/post/276018149',
                   'Upgrade-Insecure-Requests':'1'}

        url = "https://douze.pixnet.net/blog/post/398218087"
            
        # 對網站發出請求
        html = requests.get(url, headers = headers)
        # requests、BeautifulSoup皆會自行猜測原文編碼方式，以猜測的編碼方式進行解碼轉換成 unicode
        # 因此中文顯示亂碼，須先進行正確編碼，由目標網站得知 Content-Encoding: gzip
        html.encoding = 'gzip'
        # 解析html
        self.page = soup(html.text,'html.parser')
        
    def Get_Word(self):
        # 找出單字位置
        words = self.page.find_all('div',{'class':'article-content-inner'})[0].text
        # 清理html之空格
        words = words.replace("\xa0","").split("\n")
        # 清除非單字項目
        words = words[13:len(words)-9]
        
        return random.choice(words)
        
if __name__ == "__main__":
    crawler = Crawler()
    print(crawler.Get_Word())