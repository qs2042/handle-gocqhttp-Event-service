import json
from Utils import Request, Response                     # 可删除        作用为: 写的时候编辑器有提示
from Reflection import Qiass as Reflection              # 作用极大      作用为: ...
from Robot.Function import QiassNews as Function        # 作用极大      作用为: 功能
from Robot.API import Qiass as API                      # ...
from Log import Qiass as Log                            # ...

class Notice:
    def __init__(self) -> None:
        self.initializationFinal()
    
    def initializationFinal(self):
        self.GROUP_UPLOAD = "group_upload"
        self.GROUP_ADMIN = "group_admin"
        self.GROUP_INCREASE = "group_increase"
        self.GROUP_DECREASE = "group_decrease"
        self.GROUP_BAN = "group_ban"
        self.GROUP_RECALL = "group_recall"
        self.FRIEND_RECALL = "friend_recall"
        self.FRIEND_ADD = "friend_add"

        self.NOTIFY = "notify"
        self.NOTIFY_POKE = "poke"
        self.NOTIFY_LUCKY_KING = "lucky_king"
        self.NOTIFY_HONOR = "honor"

        self.GROUP_CARD = "group_card"
        self.OFFLINE_FILE = "offline_file"
        self.CLIENT_STATUS = "client_status"
        self.ESSENCE = "essence"


class Qiass:
    def __init__(self) -> None:
        self.fun = Reflection(Function())
        self.api = API()
        self.log = Log("Robot.Event")
        self.notice = Notice()

    def funMessage(self):
        text = self.request.data["message"]
        # [反射] 获取功能模块的全部方法
        methods:list = self.fun.getMethods()["method"]
        try:methods.remove("fun")
        except:pass
        try:methods.remove("template")
        except:pass
        self.log.DEBUG(len(methods), title=["解析", "功能数量"])
        for methodName in methods:
            # 获取方法实体
            method = self.fun.getAttribute(methodName)
            result = method(text=text, request=self.request, response=self.response, self=self.fun.obj)
            functionString = self.response.info["function"]
            if result != False and functionString != "None":
                self.response.info["function"] = "%s(%s)" % (methodName, functionString)
                self.log.DEBUG("已解决当前请求", title=["解析",methodName])
                break
            #self.log.DEBUG(result, title=["解析", methodName])
        return None

    def funNotice(self):
        data = self.request.data
        notice_type = data["notice_type"]

        # 设置返回数据场景
        self.request.data["message_type"] = "group"

        # 设置返回展示数据
        self.response.info["showDatabase"] = data

        # 暂时没测试的事件: 加群,退群,添加好友

        # 群文件
        if notice_type == self.notice.GROUP_UPLOAD:
            userId = data["user_id"]
            groupId = data["group_id"]
            file = data["file"]
            info = self.api.getStrangerInfo(userId)
            self.response.info["function"] = "群文件"
            result = "%s(%s)上传了一个文件\n[文件名] %s\n[文件大小] %s" % (str(info["data"]["nickname"]), userId, file["name"], file["size"])
            self.response.info["result"] = result
            return None

        # 群管理(成为|被卸, set|unset)
        if notice_type == self.notice.GROUP_ADMIN:
            userId = data["user_id"]
            groupId = data["group_id"]
            sub_type = data["sub_type"]
            info = self.api.getStrangerInfo(userId)
            self.response.info["function"] = "群管理"
            if sub_type == "set":
                self.response.info["result"] = "%s(%s)成为管理" % (info["data"]["nickname"], userId)
            if sub_type == "unset":
                self.response.info["result"] = "%s(%s)被卸管理" % (info["data"]["nickname"], userId)
            return None

        # 加群(管理同意入群|管理邀请入群, approve|invite)
        if notice_type == self.notice.GROUP_INCREASE:
            userId = data["user_id"]
            groupId = data["group_id"]
            operatorId = data["operator_id"]

            info1 = self.api.getStrangerInfo(userId)
            info2 = self.api.getStrangerInfo(operatorId)
            sub_type = data["sub_type"]
            self.response.info["function"] = "加群事件"
            if sub_type == "approve":
                self.response.info["result"] = "欢迎新人%s(%s),操作者为(%s)" % (info["data"]["nickname"], userId, operatorId)
            if sub_type == "invite":
                self.response.info["result"] = "欢迎新人%s(%s),新人是(%s)的好朋友吗?" % (info["data"]["nickname"], userId, operatorId)
            return None

        # 退群(主动退群|成员被踢|机器人被踢, leave|kick|kick_me)
        if notice_type == self.notice.GROUP_DECREASE:
            userId = data["user_id"]
            groupId = data["group_id"]
            operatorId = data["operator_id"]
            info = self.api.getStrangerInfo(userId)
            sub_type = data["sub_type"]
            self.response.info["function"] = "退群事件"
            if sub_type == "kick":
                self.response.info["result"] = "%s(%s)被踢出群,操作者为(%s)" % (info["data"]["nickname"], userId, operatorId)
            if sub_type == "leave":
                self.response.info["result"] = "%s(%s)主动退群" % userId
            if sub_type == "kick_me":
                self.response.info["result"] = "%s(%s)登录号被踢,操作者为(%s)" % (info["data"]["nickname"], userId, operatorId)
            return None

        # 禁言(禁言|解禁, ban|lift_ban)
        if notice_type == self.notice.GROUP_BAN:
            userId = data["user_id"]
            groupId = data["group_id"]
            operatorId = data["operator_id"]
            duration = data["duration"]
            info = self.api.getStrangerInfo(userId)
            sub_type = data["sub_type"]
            self.response.info["function"] = "禁言事件"
            if sub_type == "lift_ban":
                self.response.info["result"] = "(%s)被(%s)解禁了" % (info["data"]["nickname"],userId,operatorId)
            if sub_type == "ban":
                self.response.info["result"] = "(%s)被(%s)禁言%s秒" % (info["data"]["nickname"],userId,operatorId,duration)
            return None

        # 撤回消息(群聊)
        if notice_type == self.notice.GROUP_RECALL:
            userId = data["user_id"]
            groupId = data["group_id"]
            operatorId = data["operator_id"]
            messageId = data["message_id"]
            info = self.api.getStrangerInfo(userId)
            self.response.info["function"] = "撤回事件"
            if userId == operatorId:
                self.response.info["result"] = "%s(%s)撤回了一条消息" % (info["data"]["nickname"], userId)
                return None
            self.response.info["result"] = "%s(%s)的消息被(%s)撤回了" % (info["data"]["nickname"],userId, operatorId)
            return None

        # 撤回消息(私聊)
        if notice_type == self.notice.FRIEND_RECALL:
            self.request.data["message_type"] = "private"
            userId = data["user_id"]
            messageId = data["message_id"]
            info = self.api.getStrangerInfo(userId)
            self.response.info["function"] = "撤回事件"
            self.response.info["result"] = "%s(%s)撤回了一条消息" % (info["data"]["nickname"],userId)
            return None

        # 添加好友(这个为加完好友后的事件)
        if notice_type == self.notice.FRIEND_ADD:
            self.request.data["message_type"] = "private"
            userId = data["user_id"]
            self.response.info["function"] = "添加好友事件"
            self.response.info["result"] = "你好, 我是大晴, 如果有更好的想法, 可加690293425进行讨论"
            return None

        # 戳一戳, 群红包运气王, 群成员荣誉变更
        if notice_type == self.notice.NOTIFY:
            sub_type = data["sub_type"]
            # 戳一戳
            if sub_type == self.notice.NOTIFY_POKE:
                self.response.info["function"] = "戳一戳事件"
                try:
                    groupId = data["group_id"]
                    userId = data["user_id"]
                    targetId = data["target_id"]
                    info = self.api.getStrangerInfo(userId)
                    if str(targetId) == "1053287283":
                        self.response.info["result"] = "不要再戳我啦, %s(%s)你个大坏蛋!" % (info["data"]["nickname"],userId)
                        return None
                    if targetId == userId:
                        self.response.info["result"] = "%s(%s)戳了一下自己" % (info["data"]["nickname"],userId)
                        return None
                    #self.response.info["result"] = "(%s)戳了一下(%s)" % (userId, targetId)
                except:
                    self.request.data["message_type"] = "private"
                    userId = data["user_id"]
                    targetId = data["target_id"]
                    senderId = data["sender_id"]
                    selfId = data["self_id"]
                    info = self.api.getStrangerInfo(userId)
                    self.response.info["result"] = "不要再戳我啦, %s(%s)你个大坏蛋!" % (info["data"]["nickname"],userId)
                return None
                
            # 群红包运气王提示
            if sub_type == self.notice.NOTIFY_LUCKY_KING:
                self.response.info["function"] = "群红包运气王提示事件"
                userId = data["user_id"]
                targetId = data["target_id"]
                self.response.info["result"] = "(%s)发送了红包,运气王是(%s)" % (userId, targetId)
                return None
            
            # 群成员荣誉变更提示
            if sub_type == self.notice.NOTIFY_HONOR:
                self.response.info["function"] = "群成员荣誉变更提示事件"
                userId = data["user_id"]
                honorType = data["honor_type"]
                if honorType == "talkative":
                    honor = "龙王"
                if honorType == "performer":
                    honor = "群聊之火"
                if honorType == "emotion":
                    honor = "快乐源泉"
                self.response.info["result"] = "(%s)获得了荣誉%s" % (userId, honor)
                return None

            if sub_type == "title":
                self.response.info["function"] = "群成员头衔事件"
                userId = data["user_id"]
                title = data["title"]
                self.response.info["result"] = "(%s)获得了头衔[%s]" % (userId, title)
                return None


        # 群成员名片更新
        if notice_type == self.notice.GROUP_CARD:
            userId = data["user_id"]
            cardNew = data["card_new"]
            cardOld = data["card_old"]
            self.response.info["function"] = "群成员名片更新事件"
            self.response.info["result"] = "(%s)更改了群名片\n%s\n↓↓↓↓\n%s" % (userId, cardOld, cardNew) 
            return None

        # 接收到离线文件
        if notice_type == self.notice.OFFLINE_FILE:pass

        # 其他客户端在线状态变更
        if notice_type == self.notice.CLIENT_STATUS:pass

        # 精华消息(添加精华消息|移除精华消息, add|delete)
        if notice_type == self.notice.ESSENCE:
            print(data)
            groupId = data["group_id"]
            message_id = data["message_id"]
            subType = data["sub_type"]
            senderId = data["sender_id"]
            operatorId = data["operator_id"]
            self.response.info["function"] = "精华消息事件"
            if subType == "add":
                if senderId == operatorId:
                    self.response.info["result"] = "(%s)将自己的消息添加进了精华消息" % senderId
                    return None
                self.response.info["result"] = "(%s)的消息被(%s)添加进精华消息" % (senderId, operatorId)
                
            if subType == "delete":
                if senderId == operatorId:
                    self.response.info["result"] = "(%s)将自己的消息从精华消息中移除" % senderId
                    return None
                self.response.info["result"] = "(%s)的消息被(%s)从精华消息移除" % (senderId, operatorId)
            return None

    def funRequest(self):
        data = self.request.data
        # 加好友
        if data["request_type"] == "friend":
            flag = data["flag"]
            self.response.info["function"] = "添加好友事件"
            self.api.setFriendAddRequest(flag, True, "机器人")
        
        if data["request_type"] == "group":
            flag = data["flag"]
            sub_type = data["sub_type"]
            self.response.info["function"] = "添加群事件"
            self.api.setGroupAddRequest(flag, sub_type, None, True, "None")



    def isInterval(self):
        if self.request.data.get("interval") != None:
            self.response.info["function"] = "interval"
            self.response.info["result"] = "无触发"
            return True
        return False
    def showDatabaseMessage(self, data):
        if data["message_type"] == "group":
            other = "收到来自群聊的消息 \n" + \
            "消息来自      : [group_id] \n" + \
            "发送者        : [sender_nickname]([user_id]) \n" + \
            "群昵称        : [sender_card] \n" + \
            "群等级        : [sender_level] \n" + \
            "身份          : [sender_role] \n" + \
            "性别          : [sender_age] \n" + \
            "头衔          : [sender_title] \n" + \
            "消息内容      : [message] \n" + \
            "消息内容(raw) : [raw_message] \n" + \
            "消息ID        : [message_id] \n" + \
            "anonymous     : [anonymous] \n" + \
            ",font,message_seq,self_id..."
            other = other.replace("[group_id]", str(data["group_id"]))
            other = other.replace("[user_id]", str(data["user_id"]))
            other = other.replace("[sender_nickname]", str(data["sender"]["nickname"]))
            other = other.replace("[sender_card]", str(data["sender"].get("card")))

            other = other.replace("[sender_level]", str(data["sender"]["level"]))
            other = other.replace("[sender_role]", str(data["sender"].get("role")))
            other = other.replace("[sender_age]", str(data["sender"]["age"]))
            other = other.replace("[sender_title]", str(data["sender"].get("title")))
            other = other.replace("[message]", str(data["message"]))
            other = other.replace("[raw_message]", str(data["raw_message"]))
            other = other.replace("[message_id]", str(data["message_id"]))
            other = other.replace("[anonymous]", str(data["anonymous"]))
            self.response.info["showDatabase"] = other
        if data["message_type"] == "private":
            other = "收到来自私聊的消息 \n" + \
            "消息来自      : [sender_nickname]([user_id]) \n" + \
            "年龄          : [sender_age] \n" + \
            "性别          : [sender_sex] \n" + \
            "消息内容      : [message] \n" + \
            "消息内容(raw) : [raw_message] \n" + \
            "消息ID        : [message_id] \n" + \
            "font,self_id,sub_type,target_id,time"
            other = other.replace("[user_id]", str(data["user_id"]))
            other = other.replace("[sender_nickname]", str(data["sender"]["nickname"]))
            other = other.replace("[sender_age]", str(data["sender"]["age"]))
            other = other.replace("[sender_sex]", str(data["sender"]["sex"]))
            other = other.replace("[message]", str(data["message"]))
            other = other.replace("[raw_message]", str(data["raw_message"]))
            other = other.replace("[message_id]", str(data["message_id"]))
            self.response.info["showDatabase"] = other
    def showDatabaseNotice(self, data):pass
    def showDatabaseRequest(self, data):pass
    def showDatabase(self):
        data = self.request.data
        post_type = data["post_type"]
        if post_type == "message":
            self.showDatabaseMessage(data)
        if post_type == "notice":
            self.showDatabaseNotice(data)
        if post_type == "request":
            self.showDatabaseRequest(data)
        return None
    def sendMessage(self):
        data = self.request.data
        result = self.response.info["result"]
        # 数据不为空才发送结果
        if result != "None":
            self.api.sendMessage(data.get("message_type"), data.get("user_id"), data.get("group_id"), result)
        return None

    def mainInitilization(self, request:Request, response:Response):
        self.request = request
        self.response = response
    def main(self, request:Request, response:Response):
        self.mainInitilization(request, response)

        # 如果是interval那就直接不往下执行了, 返回啥东西都无所谓的
        if self.isInterval():return None
        
        data = request.data
        post_type = data["post_type"]

        if post_type == "message":
            if data.get("anonymous") != None:
                self.log.DEBUG("message-匿名", title=["解析", "事件类型"])
                # 执行
                self.funMessage()
                # 展示数据
                self.showDatabase()
                # 发送结果
                self.sendMessage()
                return None

        if post_type == "message":
            self.log.DEBUG("message", title=["解析", "事件类型"])
            # 执行
            self.funMessage()
            # 展示数据
            self.showDatabase()
            # 发送结果
            self.sendMessage()

        if post_type == "notice":
            self.log.DEBUG("notice", title=["解析", "事件类型"])
            # 执行
            self.funNotice()
            # 发送结果
            self.sendMessage()

        if post_type == "request":
            self.log.DEBUG("request", title=["解析", "事件类型"])
            self.funRequest()
        return None
        
            