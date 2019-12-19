# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

from ConstellationsCrawler import Crawler1
from WordsCrawler import Crawler2

import time

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
                
                #try:
                #    crawler1 = Crawler1(event.message.text)
                #    text = crawler1.Get_Contents()
                #except:
                #    text = event.message.text
                    
                #line_bot_api.reply_message(event.reply_token, TextSendMessage(text))
            
            #if time.strftime("%H") in [8, 12, 18]:
            #crawler2 = Crawler2()
            #text = crawler2.Get_Word()
            #user_id = event.source.user_id
            #line_bot_api.push_message(user_id, TextSendMessage(text))
            
                try:
                    crawler1 = Crawler1(event.message.text)
                    text1 = crawler1.Get_Contents()
                    crawler2 = Crawler2()
                    text2 = crawler2.Get_Word()
                    user_id = event.source.user_id
            
                    button_template_message = ButtonsTemplate(
                                    thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
                                    title='Menu', 
                                    text='Please select',
                                    ratio="1.51:1",
                                    image_size="cover",
                                    actions=[
        #                                PostbackTemplateAction 點擊選項後，
        #                                 除了文字會顯示在聊天室中，
        #                                 還回傳data中的資料，可
        #                                 此類透過 Postback event 處理。
                                        #PostbackTemplateAction(
                                        #    label='postback還會回傳data參數', 
                                        #    text='postback text',
                                        #    data='action=buy&itemid=1'
                                        #),
                                        MessageTemplateAction(
                                            label = "Constellations", text = text1
                                        ),
                                        MessageTemplateAction(
                                            label = "Words", text = text2
                                        )
                                        #URITemplateAction(
                                        #    label='uri可回傳網址', uri='http://www.xiaosean.website/'
                                        #)
                                    ]
                                )
                    line_bot_api.push_message(user_id, TemplateSendMessage(alt_text="Template Example", template=button_template_message))
                except:
                    #text = event.message.text
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "Hi"))
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()