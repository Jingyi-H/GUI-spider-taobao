import os
import re
import requests
import json
import time
import pandas as pd
import datetime as dt
from utils import *

class LiveSpider():
    def __init__(self, api, cookie, data, token, tstmp, appKey="12574478"):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            'authority': 'h5api.m.taobao.com',
            'method': 'GET',
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4; G7-TL00 Build/G7-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
            "X-Requested-With": "com.android.browser",
            "Host": "h5api.m.taobao.com",
            "content-type": "application/json",
            "Connection": "keep-alive",
            "cookie": cookie,
            # "Referer": "https://h5.m.taobao.com/taolive/video.html?id=270224460267&sharerId=3346403614&anchorGuard=true&timestamp=1593758387098&signature=9dc7c7a903549e2b53c5b22bc08c2f22&livesource=guard&cp_origin=taobaozhibo%7Ca2141.8001249%7C%7B%22account_id%22%3A%221759494485%22%2C%22app_key%22%3A%2221646297%22%2C%22feed_id%22%3A%22270224460267%22%2C%22os%22%3A%22android%22%2C%22spm-cnt%22%3A%22a2141.8001249%22%7D&sourceType=talent&suid=7cbdd053-7206-4861-b2d7-640abf856cef&ut_sk=1.Wnv7Q60K4FsDAC08ObmQITZJ_21646297_1593758063925.Alipay.tblive_guard&chInfo=ch_share__chsub_DingTalkSession"
        }
        self.cookie = cookie
        self.params = {
            "jsv": "2.4.0",
            "appKey": appKey,
            "t": tstmp,
            "sign": get_sign(token, tstmp, appKey, data),   # "signature": sign,
            "AntiCreep": "true",
            "api": api,
            "v": "1.0",
            "type": "jsonp",        #originjson
            "dataType": "jsonp",
            "callback": "mtopjsonp4",
            "data": data
        }

        self.sign = get_sign(token, tstmp, appKey, data)

    def run(self, url):
        # url = "https://h5api.m.taobao.com/h5/mtop.mediaplatform.video.livedetail.itemlist/1.0/?jsv=2.4.0&appKey=12574478&t=1594948604826&sign={}&AntiCreep=true&api=mtop.mediaplatform.video.livedetail.itemlist&v=1.0&type=jsonp&dataType=jsonp&callback=mtopjsonp4&data=%7B%22type%22%3A%220%22%2C%22liveId%22%3A%22272260030860%22%2C%22creatorId%22%3A%221759494485%22%7D".format(self.sign)
        # url = "https://h5api.m.taobao.com/h5/mtop.mediaplatform.video.livedetail.itemlist/1.0/"
        resp = requests.request('GET', url, headers=self.headers, params=self.params)
        ret = str(resp.content, encoding='utf-8').strip()

        next = (re.match(r".*?({.*}).*", ret)).group(1)

        items = json.loads(next).get('data').get('itemList')
        hot = json.loads(next).get('data').get('hotList')
        hotList = []
        goods = []
        price = []
        coupon = []
        buyCount = []
        cate = []
        # print(items)
        for h in hot:
            if h.get('itemId')!='600455639989':
                hotList.append(h.get('itemId'))
        print("hot list:", hotList)
        for i in range(len(items)):
            goods.append(items[i].get('goodsList')[0].get('itemName'))
            price.append(items[i].get('goodsList')[0].get('itemPrice'))
            coupon.append(items[i].get('goodsList')[0].get('extendVal').get('customizedItemRights'))
            buyCount.append(items[i].get('goodsList')[0].get('buyCount'))
            cate.append(items[i].get('goodsList')[0].get('extendVal').get('categoryLevelOneName'))

        recommend = pd.DataFrame(goods, columns=['商品名称'])
        recommend['价格'] = pd.Series(price)
        recommend['优惠'] = pd.Series(coupon)
        recommend['销量'] = pd.Series(buyCount)
        recommend['一级分类'] = pd.Series(cate)

        return recommend


class BcpageSpider():
    def __init__(self, broadcasterId, cookie, token, bcname, start_time, tstmp, api="mtop.mediaplatform.anchor.info", appKey="12574478"):
        self.headers = {
            "Host": "h5api.m.taobao.com",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "x-wap-profile": "http://wap1.huawei.com/uaprof/HUAWEI_G7-TL00_UAProfile.xml",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4; G7-TL00 Build/G7-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "Cookie": cookie,
            "X-Requested-With": "com.android.browser"
        }
        self.data = str({"broadcasterId": broadcasterId, "start": 0, "limit": 10})

        self.params = {
            "jsv": "2.4.8",
            "appKey": appKey,
            "t": tstmp,
            "sign": get_sign(token, tstmp, appKey, self.data),   # "signature": sign,
            "api": api,
            "v": "1.0",
            "AntiCreep": "true",
            "type": "jsonp",        #originjson
            "dataType": "jsonp",
            "callback": "mtopjsonp2",
            "data": self.data
        }
        self.creatorId = broadcasterId  # 后续爬直播间需要
        self.token = token
        self.cookie = cookie
        self.start_time =start_time
        self.bcname = bcname

    def get_replay_list(self, url, start):
        '''
        获取上一周直播间的liveId
        :param url: 主播个人页链接
        :param start: 爬取的起始时间（毫秒级时间戳）
        :return: replaylist
        '''
        resp = requests.request('GET', url, headers=self.headers, params=self.params)

        ret = str(resp.content, encoding='utf-8').strip()
        raw = (re.match(r".*?({.*}).*", ret)).group(1)
        replays = eval(raw).get('data').get('replays')

        replaylist = []
        for r in replays:
            if int(r.get('liveTime')) > start:
                # print(r.get('videoUrl'))
                liveId = r.get('liveId')
                vdate = time.strftime("%Y%m%d", time.localtime(int(r.get('liveTime'))/1000))
                replaylist.append([liveId, vdate])
            else:
                break

        # print(replaylist)
        return replaylist

    def get_replay_item(self, replayList, filename, path):
        # 可能需要维护的地方vapi, vurl对应直播间页面抓包获取的headers中的api以及url
        vapi = "mtop.mediaplatform.video.livedetail.itemlist"
        vurl = "https://h5api.m.taobao.com/h5/mtop.mediaplatform.video.livedetail.itemlist/1.0/"

        writer = pd.ExcelWriter(os.path.join(path, filename))
        for live in replayList:
            vdata = str({"type": "0", "liveId": live[0], "creatorId": self.creatorId})
            tstmp = str(int(round(time.time() * 1000)))
            # vsign = get_sign(self.token, tstmp, appKey, vdata)
            # api, cookie, data, token, tstmp
            vspider = LiveSpider(vapi, self.cookie, vdata, self.token, tstmp)
            df = vspider.run(vurl)
            print(df.head())
            df.to_excel(writer, sheet_name=live[1], index=False)
        writer.save()

    def run(self, path):
        # 可能要维护的地方，此url为主播个人页的url
        url = "https://h5api.m.taobao.com/h5/mtop.mediaplatform.anchor.info/1.0/"
        replays = self.get_replay_list(url, self.start_time)
        self.get_replay_item(replays, self.bcname +"直播间.xlsx", path)

# def get_bc_dict():
#     bc_dict = {}
#     with open(r'inbc.txt', 'r') as f:
#         while True:
#             bcs = f.readline()
#             if not bcs:
#                 break
#             bc_name, bc_id = bcs.split()
#             bc_dict[bc_name] = bc_id
#         f.close()
#     # print(bc_dict)
#
#     return bc_dict

def main(cookie, broadcaster, path=""):
    '''
    可通过其他.py文件调用tb_week.main方法
    :param cookie: Fiddler抓包获取的Cookies
    :param broadcaster: 中文姓名
    :param path: 生成的excel文件的存储路径
    :return:
    '''
    token = get_token(cookie)
    # bc_dict = get_bc_dict()
    bc_dict = {"李佳琦": "1759494485", "薇娅": "69226163", "盒马鲜生": "3012860579"}


    tstmp = str(int(round(time.time() * 1000)))
    start_time = get_start_time()
    # appKey = "12574478"

    spider = BcpageSpider(bc_dict.get(broadcaster), cookie, token, broadcaster, start_time, tstmp)  # api, broadcasterId, cookie, token, 主播姓名, 直播开始时间
    spider.run(path)


"""
https://h5api.m.taobao.com/h5/mtop.mediaplatform.anchor.info/1.0/?jsv=2.4.8&appKey=12574478&t=1595924912486&sign=84e8351b34fe538f0b05a57984688e7b&api=mtop.mediaplatform.anchor.info&v=1.0&AntiCreep=true&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22broadcasterId%22%3A%2269226163%22%2C%22start%22%3A0%2C%22limit%22%3A10%7D

Cookie: 
enc=1j%2BriJP1xkgGdg8WzCoVFsdGtPKsRtYk2Xqwz59pSOwchpi3zrxgyYFnpSyW8Jd%2BW6DaCKvffaFf7siaKRZrgQ%3D%3D; t=e3d1294cb0bd7a622af1dc99929d89f4; l=eBOCmyEcOr3lRsJsBOfanurza7uFSCOYYuPzaNbMiOCPOYfH5k5hWZoase8MC3ORh6bBR3ketZseBeYBVQAonxv9fxhD0nkmn; tfstk=cFl5BwxZTvs4od9Fa4T44jAs-5FFZgpblwZZPxPM0sa2wJg5MRzbozXhC9q8o; cookie2=12fc5af48264ec70bc081e10d1c0c418; _tb_token_=f0e811e6bf0e1; cna=BOEOD8TINSoCAXFbClPuqNlD; _m_h5_tk=53bb2e8a0c88ec062f622f1fd9013a63_1597381044679; _m_h5_tk_enc=31c735731ffbc169d825df42f3d14052; isg=BDMz5IBAaO-B3SXwAOG3CUcryTVdaMcq4i2V0-XQj9KJ5FOGbThXepFimNKo3x8i
"""