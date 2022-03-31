import time,random,re,requests,json


# 因为时间有点久, 忘记这个文件是否可以删除了
class Qiass:
    def __init__(self) -> None:
        self.__createSession()
        
    def __createSession(self):
        self.__session = requests.session()
        self.__refreshSessionHeaders()
    def __refreshSessionHeaders(self):
        self.__session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}

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
    
    def __timeNetwork(self):pass
    def timeNetwork(self):pass

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

    # 前缀匹配(前缀, 模糊, 正则)
    def __prefix(self, text:str, prifixList:list):
        result = False
        for i in prifixList:
            # 默认语句(不带参数)
            if len(text) == len(i) and text == i:
                result = "Default"
                break

            # 带参语句
            if text[:len(i)] == i:
                result = text[len(i):]
                break
        # 这里是为了去掉空格
        if result != False and result != "Default":
            number = 0
            for i in result:
                if i == " ":
                    number += 1
                    continue
                break
            if number > 0:
                result = result[number:]
        # 这里是因为上面去掉空格, 那就是没有传参, 那就是使用Default了, 被误伤了
        if result == "":
            return "Default"
        return result
    def prefix(self, text: str, prifixList: list) -> str:
        if len(prifixList) > 0:
            return self.__prefix(text, prifixList)
        
        prifixList = [
            '#',
            '[CQ:at,qq=1053287283]',
            '大晴',
        ]

        prifixReList = [
            "\[CQ:reply,id=.*?\]", # 为了匹配回复: [CQ:reply,id=.*?][CQ:at,qq=1053287283] [CQ:at,qq=1053287283]  在吗
            "\[CQ:at,qq=1053287283\]" # 为了匹配回复: [CQ:reply,id=.*?][CQ:at,qq=1053287283] 不在吗
        ] 
        return self.__prefix(text, prifixList)

    # 词库屏蔽
    def __shielding(self, text:str, reList:list, shieldingWord=None):
        isExecute = False
        if shieldingWord == None:
            shieldingWord = "*"
        for pattern in reList:
            l = re.findall(pattern, text)
            if len(l) >= 1:
                for j in l:
                    keyWord = j
                    if shieldingWord == "*":
                        text = text.replace(keyWord, shieldingWord * len(keyWord))
                    if shieldingWord != "*":
                        text = text.replace(keyWord, shieldingWord)
                isExecute = text
        return isExecute
    def shielding(self, text:str) -> str:
        re0 = [
            "[0-9]{11}", "[0-9]{10}", "jj",
            "\{face:[0-9]\}|\{face:[0-9]{2}\}|\{face:[0-9]{3}\}",
            "狂撸", "狂射", "9000次", "求草"
            "你就不能搞点新创意出来嘛", "face57","我不是大便，我的粉丝也不是苍蝇",
            "别发这么无聊的信息行不",
        ]
        re1 = [
            '傻逼', '煞笔', '神经病', '母猪', "tianyu"
        ]

        re2 = [
            '菲菲', '浩哥', '小燕', '吴珂', '王雨昕', '茉姐', "杨秀花"
        ]
        text = self.__shielding(text, re0)
        text = self.__shielding(text, re1, "小可爱")
        text = self.__shielding(text, re2, "小晴")
        return text

    # 分页
    def __paging(self, qslb:list, pageRows:int, pageSee:int):
        countTotal = len(qslb)

        pageTotal = countTotal / pageRows
        if not pageTotal.is_integer():
            pageTotal = int(pageTotal) + 1
        
        if pageSee > pageTotal:
            return False
        
        if pageSee <= 1:
            start = 0
            end = pageRows
        if pageSee > 1:
            start = pageRows * pageSee - pageRows
            end = pageRows * pageSee
        
        data = {}
        for i in list(qslb)[start:end]:
            data[i] = qslb[i]
        
        result = {
            "pageSee":pageSee,
            "pageTotal":pageTotal,
            "data":data
        }
        return result
    def paging(self, qslb:list, pageRows=5, pageSee=1):
        try:
            pageRows = int(pageRows)
            pageSee = int(pageSee)
        except:
            return False
        return self.__paging(qslb, pageRows, pageSee)

    # 概率
    def __probability(self, number=10, percentage=2):
        data = {"True" : 0, "False" : 0}
        for i in range(0, number):
            lucky = random.randint(0, 100 * 10) # 概率公式

            if lucky <= percentage * 10:
                data["True"] += 1
            else:
                data["False"] += 1
        return data
    def probability(self, number=1, percentage=2):
        if number < 1:
            return None
        data = self.__probability(number, percentage)
        if number == 1:
            if data["True"] > 0:
                return True
            else:
                return False
        return data

    # 聊天(本地词库, 图灵123, 青云客)
    def __chatThesaurus(self, text:str):
        #TODO 后期改为数据库储存
        data = {
            "早":"早啊,祝你今天愉快!",
            "中午好": "中午好,吃午饭没呀",
            "晚上好": "晚上好,我去睡觉觉啦",
        }
        for i in data:
            if i == text:
                return data[i]
        return False
    
    def __chatTuLing123(self, text:str) -> requests.Response:
        # TODO 这里需要填写自己的apiKey
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
        answer = self.__chatThesaurus(text)
        return answer
    
    def chatTuLing123(self, text:str):
        res = self.__chatTuLing123(text)
        data = json.loads(res.text)
        answer = data["results"][0]["values"]["text"]
        if answer == "请求次数超限制!":
            answer = False
        return answer

    def chatQingYunKe(self, text:str):
        res = self.__chatQingYunKe(text)
        if res.status_code == 200:
            data = json.loads(res.text)
            answer = data["content"]
        else:
            answer = False
        return answer

    # 帮我选择
    def helpMeChoose(self, text:str):
        l = text.split("*")
        return "已为您选择: " + l[random.randint(0, len(l)-1)]

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
            '''
            result = ""
            i = 0
            for items in data:
                result += "%d.%s\n" % (i, items)
                i += 1
            return result + "Tips: 发送'查看功能 功能名'即可获取功能信息"
            '''
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
            result = data.get(text)
            if result == None:
                return "未找到[%s]公告的信息" % text
            if result != None:
                return "[%s]\n作者:%s\n内容:%s\n发布时间:%s" % (text, result[0],result[1],result[2])
        return False
    










    



if __name__ == "__main__":
    q = Qiass()