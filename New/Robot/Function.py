import random,requests,json,time,re

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


class Function:pass