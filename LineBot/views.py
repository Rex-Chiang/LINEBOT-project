# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from ConstellationsCrawler import Crawler

# 這邊是Linebot的授權TOKEN(註冊LineDeveloper帳號會取得)，
# 使用時記得設成環境變數，不要公開在程式碼
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):

    if request.method == 'POST':
        # 取得憑證，用於解析時確認訊息是真的來自 Line Server
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        # 解析事件類型
        try:
            events = parser.parse(body, signature)
        # 訊息並非來自 Line Server
        except InvalidSignatureError:
            return HttpResponseForbidden()
        # Line Server 出現狀況
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            # 確保為文字訊息
            #　isinstance判斷對象是否為已知類型
            if isinstance(event, MessageEvent):
                
                try:
                    crawler = Crawler(event.message.text)
                    text = crawler.Get_Contents()
                except:
                    text=event.message.text
                    
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text))
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()