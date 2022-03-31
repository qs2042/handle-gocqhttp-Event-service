from unittest import result
from Decorator import mapping,InstructionMapping
import random,requests,json,time,re

from Utils import Request,Response

# 工具类
class CQCode:
    # 未被go-cqhttp支持的CQcode 
    def __init__(self) -> None:
        # [CQ:rps]          猜拳魔法表情
        # [CQ:dice]         掷骰子魔法表情
        # [CQ:shake]        窗口抖动(戳一戳)
        # [CQ:anonymous]    匿名发消息
        # [CQ:contact,type=qqID,id=10001000]  推荐好友   
        # [CQ:contact,type=groupID,id=100100] 推荐群
        # [CQ:location,lat=39.8969426,lon=116.3109099]  位置
        pass

    # 表情
    @staticmethod
    def face(id:str):
        # https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
        if not id.isdigit():
            id = random.randint(0, 221)
        id = int(id)
        if id < 0 or id > 221:
            id = random.randint(0, 221)
        return "[CQ:face,id=%d]" % id
    
    # 语音
    @staticmethod
    def record(file="http://baidu.com/1.mp3"):
        # magic     0=正常(Default), 1=变声
        # url       语音URL
        # cache     只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 0=不使用, 1=使用(Default)
        # Proxy     只在通过网络 URL 发送时有效, 表示是否通过代理下载文件(需通过环境变量或配置文件配置代理), 0=不使用, 1=使用(Default)
        # timeout   只在通过网络 URL 发送时有效, 单位秒, 表示下载网络文件的超时时间 , 默认不超时
        return "[CQ:record,file=%s]" % file
    
    # 短视频
    @staticmethod
    def video(file="http://baidu.com/1.mp4", cover="http://baidu.com/1.jpg"):
        # c         通过网络下载视频时的线程数, 默认单线程. (在资源不支持并发时会自动处理), params=2or3
        return "[CQ:video,file=%s,cover=%s]" % (file, cover)
    
    # @
    @staticmethod
    def at(qq=2042136767, name="at的群友不在当前群里"):
        return "[CQ:at,qq=%s,name=%s]" % (qq, name)

    # 链接分享
    @staticmethod
    def share(url, title, content=None, image=None):
        # content       内容描述
        # image         图片URL
        return "[CQ:share,url=%s,title=%s]" % (url, title)
    
    # 音乐分享
    @staticmethod
    def music(type="163", id=28949129):
        # qq, 163, xm
        return "[CQ:music,type=%s,id=%s]" % (type, id)
    def musicCustom(self, url="http://baidu.com", audio="http://baidu.com/1.mp3", title="音乐标题", content=None, image=None):
        return "[CQ:music,type=custom,url=%s,audio=%s,title=%s]" % (url, audio, title)

    # 图片
    @staticmethod
    def image(file="http://baidu.com/1.jpg", type="show", id="40004"):
        # value = 图片文件名
        # flash = 闪照, show = 秀图 (默认普通图片)
        # value = 发送秀图时的特效id, 默认为40000
        return "[CQ:image,file=%s,type=%s,id=%s]" % (file,type,id)
    
    # [CQ:reply,id=123456]          回复
    # [CQ:reply,text=Hello World,qq=10086,time=3376656000,seq=5123] 自定义回复
    # [CQ:redbag,title=恭喜发财]    红包
    
    # 戳一戳
    @staticmethod
    def poke(qq):
        return "[CQ:poke,qq=%s]" % qq

    # [CQ:gift,qq=123456,id=8]      发送礼物
    # [CQ:forward,id=xxxx]          合并转发
    # ...                           合并转发消息节点
    # [CQ:xml,data=xxxx]            XML消息
    # [CQ:json,data={"app":"com.tencent.miniapp"&#44;"desc":""&#44;"view":"notification"&#44;"ver":"0.0.0.1"&#44;"prompt":"&#91;应用&#93;"&#44;"appID":""&#44;"sourceName":""&#44;"actionData":""&#44;"actionData_A":""&#44;"sourceUrl":""&#44;"meta":{"notification":{"appInfo":{"appName":"全国疫情数据统计"&#44;"appType":4&#44;"appid":1109659848&#44;"iconUrl":"http:\/\/gchat.qpic.cn\/gchatpic_new\/719328335\/-2010394141-6383A777BEB79B70B31CE250142D740F\/0"}&#44;"data":&#91;{"title":"确诊"&#44;"value":"80932"}&#44;{"title":"今日确诊"&#44;"value":"28"}&#44;{"title":"疑似"&#44;"value":"72"}&#44;{"title":"今日疑似"&#44;"value":"5"}&#44;{"title":"治愈"&#44;"value":"60197"}&#44;{"title":"今日治愈"&#44;"value":"1513"}&#44;{"title":"死亡"&#44;"value":"3140"}&#44;{"title":"今**亡"&#44;"value":"17"}&#93;&#44;"title":"中国加油, 武汉加油"&#44;"button":&#91;{"name":"病毒 : SARS-CoV-2, 其导致疾病命名 COVID-19"&#44;"action":""}&#44;{"name":"传染源 : 新冠肺炎的患者。无症状感染者也可能成为传染源。"&#44;"action":""}&#93;&#44;"emphasis_keyword":""}}&#44;"text":""&#44;"sourceAd":""}]  JSON消息
    # [CQ:cardimage,file=https://i.pixiv.cat/img-master/img/2020/03/25/00/00/08/80334602_p0_master1200.jpg]     cardimage 
    
    # 文本转语音
    @staticmethod
    def tts(text="大家好我是萌新"):
        return "[CQ:tts,text=%s]" % text

# 工具类
class Function:
    def __init__(self) -> None:
        self.__createSession()
    
    def __createSession(self):
        self.__session = requests.session()
        self.__refreshSessionHeaders()
    def __refreshSessionHeaders(self, map=None):
        if map == None:
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
        self.__session.headers = map
    # 聊天(本地词库, 图灵123, 青云客)
    def __chatThesaurus(self, text:str):
        # TODO 后期进数据库
        data = {
            "早": "早啊,祝你今天愉快!",
            "中午好": "中午好,吃午饭没呀",
            "晚上好": "晚上好,我去睡觉觉啦",

            "人类的本质": "人类的本质",
            "霸群": "举高高~",
        }
        for i in data:
            if i == text:
                return data[i]
        return False
    
    def __chatTuLing123(self, text:str) -> requests.Response:
        # TODO 更替为自己的apiKey
        url = "http://openapi.tuling123.com/openapi/api/v2"
        dataAll = {
            "reqType": "0",  # 0-文本(默认)、1-图片、2-音频
            "perception": {
                # 文本,图片,音频,客户端
                "inputText": {
                    "text": text,
                },
                "inputImage": {
                    "url": "",
                },
                "inputMedia": {
                    "url": "",
                },
                "selfInfo": {
                    # 所在城市 省份 街道
                    "location": {
                        "city": "",
                        "province": "",
                        "street": "",
                    },
                },
            },
            "userInfo": {
                # 机器人标识,用户唯一标识,群聊唯一标识,群内用户昵称
                "apiKey": "就是这个地方",
                "userId": "",
                "groupId": "",
                "userIdName": "",
            },
        }
        params = {
            "reqType": "0",
            "perception": {
                "inputText": {
                    "text": text,
                }
            },
            "userInfo": {
                "apiKey": "就是这个地方",
                "userId": "5",
            },
        }
        return self.__session.post(url, data=json.dumps(params))

    def __chatQingYunKe(self, text:str) -> requests.Response:
        url = "http://api.qingyunke.com/api.php"
        params = {
            "key": "free",
            "appid": "0",
            "msg": text,
        }
        return self.__session.get(url, params=params)

    def chatThesaurus(self, text:str):
        try:
            answer = self.__chatThesaurus(text)
        except:
            return False
        return answer
    
    def chatTuLing123(self, text:str):
        res = self.__chatTuLing123(text)
        data = json.loads(res.text)
        answer = data["results"][0]["values"]["text"]
        if answer == "请求次数超限制!":
            answer = False
        return answer

    def chatQingYunKe(self, text:str):
        try:
            res = self.__chatQingYunKe(text)
            data = json.loads(res.text)
            answer = data["content"]
        except:
            return False
        return answer

    def chat(self, text:str):
        switch = False
        if switch == False:
            switch = self.chatThesaurus(text)
        if switch == False:
            switch = self.chatTuLing123(text)
        if switch == False:
            switch = self.chatQingYunKe(text)
        return switch

    # 时间
    def __timeLocal(self):
        return time.localtime()
    def timeLocal(self, mode=0):
        date = self.__timeLocal()
        year = date.tm_year
        month = date.tm_mon
        day = date.tm_mday
        hour = date.tm_hour
        minute = date.tm_min

        if mode == 0:
            data = {
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "minute": minute,
            }
            return data
        if mode == 1:
            return "%s-%s-%s" % (year, month, day)
        if mode == 2:
            return "%s-%s-%s(%s:%s)" % (year, month, day, hour, minute)
        if mode == 3:
            return "%s年%s月%s日" % (year, month, day)
        if mode == 4:
            return "%s年%s月%s日(%s:%s)" % (year, month, day, hour, minute)
        return False
    
    # 时间戳
    def __timeStamp(self) -> int:
        return int(time.mktime(time.localtime()))
    def timeStamp(self, Mode:int) -> int:
        if Mode == 0:
            return self.__timeStamp()
        if Mode == 1:
            return self.__timeStamp() + random.randint(100,900)
        if Mode == 2:
            return int(str(self.timeStamp) + str(random.randint(100,999)))
        return False

    # 帮我选择
    def __helpMeChoose(self, text:str):
        l = text.split("*")
        return l[random.randint(0, len(l)-1)]
    def helpMeChoose(self, text:str):
        if not "*" in text:
            return "请输入正确的格式"
        result = self.__helpMeChoose(text)
        if result == "" or result == " ":
            return "请输入正确的格式"
        return "已为您选择: %s" % result

    # 投掷骰子
    def roll(self, text:str):
        if not text.isdigit():
            return "以为您投掷骰子(Default)\n结果为: %d" % random.randint(0, 10)
        
        text = int(text)
        if text < 0:
            return "以为您投掷骰子(Default): %d" % random.randint(0, 10)
        return "已为您投掷骰子(0,%d)\n结果为: %d" % (text, random.randint(0, text))

    # 功能列表/查看
    def functionList(self, text:str, mode:int):
        # 数据源
        start = "使用方法如下:\n"
        data = {
            "聊天系统":start+"1.发送'大晴 你好'\n2.发送'# 你好'\n3.发送'@大晴 你好'",
            "时间系统":start+"1.发送'当前时间'\n2.发送'获取时间戳'",
            
            "随机系统":start+"1.发送'帮我选择 打游戏*学习'\n2.发送'扔骰子 66'\n3.发送'随机食物'\n4.发送'随机表情'",
            "娱乐系统":start+"1.发送'戳一戳 @群友'",
            
            "功能系统":start+"1.发送'功能列表'\n2.发送'查看功能 聊天系统'",
            "公告系统":start+"1.发送'公告列表'\n2.发送'查看公告 v1.0'",

            "翻译系统":start+"暂无介绍...",
            "查询系统":start+"暂无介绍...",

            "新闻系统":start+"暂无介绍...",
            "模板系统":start+"暂无介绍...",

            "被动系统":start+"1.有概率自动回复\n2.主动欢迎新人入群\n",
            "计算系统":start+"暂无介绍...",

            "好感度系统":start+"暂无介绍...",
            "模拟器系统":start+"暂无介绍...",

            "黑白名单系统":start+"暂无介绍...",

        }
        
        # 列表
        if mode == 0:
            result = "[功能列表]\n"
            
            for i in range(0, len(data)):
                if i != 0 and i % 2 == 0:
                    result += "\n"
                name = list(data)[i]
                if len(name) > 4:
                    result += "%s%s" % (name, "    "*(4+(4-len(name))))
                    continue
                result += "%s%s" % (name, "    "*4)
            return result + "\nTips: 发送'查看功能 功能名'即可获取功能信息"


        # 信息
        if mode == 1:
            # 先使用roid
            if text.isdigit():
                if int(text) > -1 and int(text) < len(data):
                    k = list(data)[int(text)]
                    v = data[k]
                    return "[%s]\n%s" % (k, v)

            # 再使用key-value
            result = data.get(text)
            if result == None:
                return "未找到[%s]功能的信息" % text
            if result != None:
                return "[%s]\n%s" % (text, result)

        return False
    
    # 公告列表/查看
    def noticeList(self, text:str, mode:int):
        data = {
            "测试公告标题":("测试公告内容", "测试公告作者", "测试公告发布时间"),
            "v1.0":("暂无内容", "晴兽", "2022年3月3日18:45:47"),
        }
        # 列表
        if mode == 0:
            result = ""
            i = 0
            for items in data:
                result += "%d.%s\n" % (i, items)
                i += 1
            return result + "Tips: 发送'查看公告 公告名'即可获取公告信息"
        # 信息
        if mode == 1:
            if text.isdigit():
                if int(text) > -1 and int(text) < len(data):
                    k = list(data)[int(text)]
                    v = data[k]
                    return "[%s]\n%s" % (k, v)
            
            result = data.get(text)
            if result == None:
                return "未找到[%s]公告的信息" % text
            if result != None:
                return "[%s]\n作者:%s\n内容:%s\n发布时间:%s" % (text, result[0],result[1],result[2])
        return False
    
    # 词库
    def thesaurusMenu(self, title:str, l:list):
        if title[-2:] != "菜单":
            title += "菜单"
        result = "      〖%s〗\n" % title

        face = ["☆", "★"]
        for i in range(len(l)):
            if not i % 2 == 0:
                result += "%s\n" % l[i]
                continue
            result += "%s%s" % (l[i], face[random.randint(0, len(face)-1)])
                
        if result[-1:] == "\n":
            return result[:-1]
        return result
    def thesaurus(self, text:str):
        d = {
            "菜单":self.thesaurusMenu("菜单", ["文游菜单", "基础菜单", "娱乐菜单", "被动菜单"]),
            "文游菜单":self.thesaurusMenu("文游", ["角色相关", "转职相关", "新手相关", "装备相关", "背包相关", "组队相关", "强化相关", "公会相关", "私人相关", "排行相关", "抽奖相关", "新手教程", "装备图鉴", "道具图鉴", "怪物图鉴"]),
            "基础菜单":self.thesaurusMenu("基础", ["default1", "default2", "default3", "default4"]),
            "娱乐菜单":self.thesaurusMenu("娱乐", ["default1", "default2", "default3", "default4"]),
            "被动菜单":self.thesaurusMenu("被动", ["default1", "default2", "default3", "default4"]),
        }
        result = d.get(text)
        if result == None:
            return False
        return result
        
    # 点歌
    def chooseSongBase(self, musicName):
        url = "https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg"
        params = {
            '_': self.timeStamp(1),
            'cv': '4747474',
            'ct': '24',
            'format': 'json',
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '1',
            'uin': '0',
            'g_tk_new_20200303': '5381',
            'g_tk': '5381',
            'hostUin': '0',
            'is_xml': '0',
            'key': musicName,
        }
        self.__session.headers["Referer"] = 'http://y.qq.com'
        res = self.__session.get(url, params=params)
        self.__refreshSessionHeaders()

        data = json.loads(res.text)

        musics = data["data"]["song"]["itemlist"]
        if len(musics) < 1:
            return "False"
        if len(musics) == 1:
            music = musics[0]
        if len(musics) > 1:
            music = musics[0]
        musicDocid = music["docid"]  # musicId = music["id"]
        musicMid = music["mid"] # musicName = music["name"] musicSinger = music["singer"]

        # url = "https://y.qq.com/n/ryqq/albumDetail/%s" % musicMid    url = "https://y.qq.com/n/ryqq/songDetail/%s" % musicMid
        url = "https://i.y.qq.com/v8/playsong.html?ADTAG=ryqq.songDetail&songmid=%s&songid=%s&songtype=0#webchat_redirect"\
              % (musicMid, musicDocid)

        musicsImage = data["data"]["album"]["itemlist"]
        if len(musics) < 1:
            return "False"
        musicPic = musicsImage[0]["pic"]

        result = {
            "musicDocid":music["docid"],
            "musicMid": music["mid"],
            "musicName": music["name"],
            "musicSinger": music["singer"],
            "musicUrl":url,
            "musicPic":musicPic,
        }
        return result
    def chooseSongDownload(self, musicMid):
        # audio = "http://dl.stream.qqmusic.qq.com/%s.m4a?guid=%s&vkey=%s&uin=&fromtag=66" %\
        #        ("C400"+musicMid, "guid", "vKey")

        # https://dl.stream.qqmusic.qq.com/C400002kFRrU0q6QXD.m4a
        # guid=585592520
        # vkey=1D1D8807B15C4FD832379BBB066A7539B925EAE4871702DBAD76F07390A45533C76069822B874A55A843E0E9C88AFFD27CDD21CB37FC6B4B
        # uin=
        # fromtag=66

        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        params = {
            '_': time.time() * 1000,
            'sign': 'zzakgej75pk8w36d82032784bdb9204d99bf6351acb7d',
            "data": '{"req":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"7469768631","songmid":["' + musicMid + '"],"songtype":[0],"uin":"1164153961","loginflag":1,"platform":"20"}}}'
        }
        response = self.__session.get(url, params=params)
        data = json.loads(response.text)
        dataPro = data["req"]["data"]["midurlinfo"][0]

        songmid = dataPro["songmid"]
        filename = dataPro["filename"]
        vkey = dataPro["vkey"]
        purl = dataPro["purl"]
        audio = "http://dl.stream.qqmusic.qq.com/" + dataPro["purl"]

        result = {
            "dlSongMid":songmid,
            "dlFilename": filename,
            "dlVKey": vkey,
            "dlPurl": purl,
            "dlAudio": audio,
        }
        return result
    def chooseSongRaw(self, musicName):
        music = self.chooseSongBase(musicName)
        if music == "False":
            return "False"
        musicDocid = music["musicDocid"] # musicId = music["id"]
        musicMid = music["musicMid"]
        musicName = music["musicName"]
        musicSinger = music["musicSinger"]
        musicUrl = music["musicUrl"]
        musicPic = music["musicPic"]

        musicDownload = self.chooseSongDownload(musicMid)
        if musicDownload == "False":
            return "False"
        musicAudio = musicDownload["dlAudio"]

        #print(musicDownload)


        # data = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="2" templateID="1" action="web" brief="&#91;分享&#93; [title]" sourceMsgId="0" url="[url]" flag="0" adverSign="0" multiMsgFlag="0" ><item layout="2"><audio cover="[pic]" src="http://ws.stream.qqmusic.qq.com/C400003mAan70zUy5O.m4a?guid=1535153710&amp;vkey=D5315B8C0603653592AD4879A8A3742177F59D582A7A86546E24DD7F282C3ACF81526C76E293E57EA1E42CF19881C561275D919233333ADE&amp;uin=&amp;fromtag=3" /><title>[title]</title><summary>[singer]</summary></item><source name="QQ音乐" icon="https://i.gtimg.cn/open/app_icon/01/07/98/56/1101079856_100_m.png" url="http://web.p.qq.com/qqmpmobile/aio/app.html?id=1101079856" action="app"  a_actionData="com.tencent.qqmusic" i_actionData="tencent1101079856://" appid="1101079856" /></msg>'''
        data = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="2" templateID="1" action="web" brief="&#91;分享&#93; [title]" sourceMsgId="0" url="[url]" flag="0" adverSign="0" multiMsgFlag="0" ><item layout="2"><audio cover="[pic]" src="[audio]" /><title>[title]</title><summary>[singer]</summary></item><source name="QQ音乐" icon="https://i.gtimg.cn/open/app_icon/01/07/98/56/1101079856_100_m.png" url="http://web.p.qq.com/qqmpmobile/aio/app.html?id=1101079856" action="app"  a_actionData="com.tencent.qqmusic" i_actionData="tencent1101079856://" appid="1101079856" /></msg>'''
        data = data.replace("[singer]", musicSinger)
        data = data.replace("[url]", musicUrl)
        data = data.replace("[audio]", musicAudio)
        data = data.replace("[title]", musicName)
        data = data.replace("[pic]", musicPic)
        return "[CQ:xml,data=%s]" % data
    def chooseSong(self, text:str):
        return self.chooseSongRaw(text)


    #====================================================
    # [随机]
    #====================================================
    def food(self):
        l = {
            "肠粉":"暂无介绍",
            "炒米粉":"暂无介绍",
            "青椒炒肉":"暂无介绍",
        }
        key = list(l)[random.randint(0, len(l)-1)]
        return [key, l[key]]
    # 随机老婆/老公(动漫角色)
    # 随机超能力
    # 随机事件
    # 随机笑话

    #====================================================
    # [解析]
    #====================================================
    # 解析哔哩哔哩
    def analysisBiliBiliJSON(self,BV, AV):
        url = "https://api.bilibili.com/x/v2/reply/main"
        params = {
            "callback":"jQuery17204877570012846435_1646906954364",
            "jsonp":"jsonp",
            "next":"0",
            "type":"1",
            "oid":AV,
            "mode":"3",
            "plat":"1",
            "_":"1646907161286",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            "referer":"https://www.bilibili.com/video/%s?p=1&share_medium=android&share_plat=android&share_source=COPY&share_tag=s_i&timestamp=1646905753&unique_k=6LzhAFb" % BV,
        }
        self.__refreshSessionHeaders(headers)
        res = self.__session.get(url, params=params)
        self.__refreshSessionHeaders()

        text = res.text
        data = json.loads(text[text.index("{"):-1])

        replies = data["data"]["replies"]
        number = 0
        result = ""
        for i in replies:
            if number >= 3:
                break
            result += "%s(%s): %s\n" % (i["member"]["uname"], i["member"]["mid"], i["content"]["message"])
            number += 1
        return result[:-1]

    def analysisBiliBiliRe(self, pattern, text):
        result = re.findall(pattern, text)
        if len(result) == 0:
            return "False"
        if len(result) > 1:
            return result[0]
        return result[0]
    def analysisBiliBili(self,text:str):
        '''
        # url = re.findall("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", text)
        # url = re.findall("https://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", text)
        '''
        urls = re.findall("https://b23[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", text)
        if len(urls) == 0:
            return False
        
        res = self.__session.get(urls[0])
        text = res.text
        BV = self.analysisBiliBiliRe('content="https://www.bilibili.com/video/(.*?)/"', text)
        AV = self.analysisBiliBiliRe('"aid":(.*?),', text)
        
        keywords = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="keywords" name="keywords" content="(.*?)">', text)
        description = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="description" name="description" content="(.*?)"', text)
        if description == "False":
            description = self.analysisBiliBiliRe('<span class="desc-info-text">(.*?)</span>', text)

        author = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="author" name="author" content="(.*?)">', text)
        mid = self.analysisBiliBiliRe('"mid":(.*?),', text)
        
        
        title = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="name" name="title" content="(.*?)">', text)
        if title != False:
            title = title.replace("_哔哩哔哩_bilibili", "")

        url = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="url" content="(.*?)">', text)
        image = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="image" content="(.*?)">', text)
        thumbnailUrl = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="thumbnailUrl" content="(.*?)">', text)
        
        uploadDate = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="uploadDate" content="(.*?)">', text)
        datePublished = self.analysisBiliBiliRe('<meta data-vue-meta="true" itemprop="datePublished" content="(.*?)">', text)

        #download = self.analysisBiliBiliRe('"base_url":"(.*?)"', text)

        ''
        result = "[%s]\n" % urls[0]
        #if image != False:result += "%s\n" % CQCode.image(image)
        result += "BV: %s\n" % BV
        result += "AV: %s\n" % AV
        result += "UP: %s(%s)\n" % (author, mid)
        result += "[Image]\n%s\n" % image
        result += "[Title]\n%s\n" % title
        result += "[Description]\n%s\n" % description
        result += "[Upload]\n%s\n" % uploadDate
        result += "[Published]\n%s\n" % datePublished
        result += "[replies]\n%s" % self.analysisBiliBiliJSON(BV, AV)
        return result
        



# 逻辑类
class QiassNews:
    def __init__(self) -> None:
        self.fun = Function()
    
    # 这里注释是因为需要填写apiKey, 上面的Function里填写完就可以解掉注释了
    '''
    @InstructionMapping(["大晴", "#", "[CQ:at,qq=1053287283]"])
    def chat(self, **kwargs):
        result = kwargs["result"]                           # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        res = self.fun.chat(result)
        if res == False:return res
        
        response.info["function"] = "聊天系统"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行
        '''

    @InstructionMapping(["当前时间", "北京时间", ".time"])
    def currentTime(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的
        # 调用方法
        if result.isdigit():
            res = self.fun.timeLocal(int(result))
        if not result.isdigit():
            res = self.fun.timeLocal(4)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping("获取时间戳")
    def currentTimeStamp(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的
        # 调用方法
        if result.isdigit():
            res = self.fun.timeStamp(int(result))
        if not result.isdigit():
            res = self.fun.timeStamp(0)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping("帮我选择")
    def helpMeChoose(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.helpMeChoose(result)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping(["投掷骰子", "扔骰子"])
    def roll(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.roll(result)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping(["功能列表", ".help"])
    def functionList(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.functionList(result, 0)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping(["功能查看", "查看功能"])
    def functionInfo(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.functionList(result, 1)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping(["公告列表", ".notice"])
    def noticeList(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.noticeList(result, 0)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping(["公告查看", "查看公告"])
    def noticeInfo(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.noticeList(result, 1)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping(["随机食物", ".food"])
    def food(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.food()
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = "[随机食物]\n今天不妨试试%s\n%s" % (res[0],res[1])
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping()
    def menu(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的
        # 调用方法
        res = self.fun.thesaurus(result)
        if res == False:return res
        response.info["function"] = "词库"              # 
        response.info["result"] = res
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping()
    def bilibili(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的
        # 调用方法
        res = self.fun.analysisBiliBili(result)
        if res == False:return res
        response.info["function"] = "解析哔哩哔哩"              # 
        response.info["result"] = res
        return True                                         # 返回是啥无所谓, 只要不是值为False就行




    #====================================================
    # [需要权限]
    #====================================================
    @InstructionMapping(["跟我说", "发语音"])
    def tellMe(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        data = request.data
        switch = False
        if data["message_type"] == "private":
            response.info["result"] = "此功能暂时未开发私聊"
            return True
        l = [
            "2042136767",
            "2473016651",
            "3388277258"
        ]
        for i in l:
            if str(data["user_id"]) == i:
                switch = True
        l = [
            "690293425",
            "871232998",
            "560325915",
        ]
        for i in l:
            if str(data["group_id"]) == i:
                switch = True
        if not switch:
            return "该功能处于测试阶段, 您没有权限操作"

        # 调用方法
        res = CQCode.tts(result)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行


    #====================================================
    # [CQCode]
    #====================================================
    # 事件的功能, 先放在消息这里
    @InstructionMapping("欢迎新人")
    def weclome(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = CQCode.tts("欢迎萌新")        # 这里之后可以加上xxx新人的名字
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping("随机表情")
    def face(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = CQCode.face(result)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行

    @InstructionMapping("戳一戳")
    def poke(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = CQCode.poke(result)
        if res == False:return res
        
        response.info["function"] = "当前时间"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行


    @InstructionMapping(["点歌", "给我来一首", "我要听"])
    def chooseSong(self, **kwargs):
        result:str = kwargs["result"]                       # 截取指令后的参数文本
        request:Request = kwargs["kwargs"]["request"]       # 用来设置权限的
        response:Response = kwargs["kwargs"]["response"]    # 用来返回数据的

        # 调用方法
        res = self.fun.chooseSong(result)
        if res == False:return res
        
        response.info["function"] = "点歌"              # 
        response.info["result"] = res                       #
        return True                                         # 返回是啥无所谓, 只要不是值为False就行





