import requests,json


class Qiass:
    def __init__(self) -> None:
        self.__initlizationVariable()
        self.__createSession()
        self.__refreshSessionHeaders()
    def __initlizationVariable(self):
        self.ip = "http://127.0.0.1:5700/"
    def __createSession(self):
        self.session = requests.session()
    def __refreshSessionHeaders(self):
        self.session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    
    # 私聊/群临时会话消息
    def sendPrivateMessage(self, userID:int, groupID:int, message:str, autoEscape=False):
        url = "send_group_msg"
        params = {
            "user_id":userID,           # QQ号
            "group_id":groupID,         # 临时对话所需要的群号
            "message":message,          # 内容
            "auto_escape":autoEscape,   # 是否作为纯文本发送(即是否解析CQ码)
        }
        # 响应内容: message_id(int32, 消息ID)
        return self.session.get(self.ip+url, params=params)
    
    # 群消息
    def sendGroupMessage(self, groupID:int, message:str, autoEscape=False):
        url = "send_group_msg"
        params = {
            "group_id":groupID,         # 群号
            "message":message,          # 内容
            "auto_escape":autoEscape,   # 是否作为纯文本发送(即是否解析CQ码)
        }
        # 响应内容: message_id(int32, 消息ID)
        return self.session.get(self.ip+url, params=params)

    # 合并转发消息
    def sendGroupForwardMessage(self, groupID:int, message):
        url = "send_group_forward_msg"
        params = {
            "group_id":groupID,         # 群号
            "message":message,          # 内容( forward node[] 自定义转发消息, 具体看 CQcode)
        }
        return self.session.get(self.ip+url, params=params)

    # 发送消息
    def sendMessage(self, messageType:str, userID:int, groupID:int, message:str, autoEscape=False):
        url = "send_msg"
        params = {
            "message_type":messageType, # 消息类型(private,group)(不传则根据*_id参数判断)
            "user_id":userID,           # QQ号
            "group_id":groupID,         # 临时对话所需要的群号
            "message":message,          # 内容
            "auto_escape":autoEscape,   # 是否作为纯文本发送(即是否解析CQ码)
        }
        # 响应内容: message_id(int32, 消息ID)
        return self.session.get(self.ip+url, params=params)
    
    # 撤回消息
    def deleteMessage(self, messageID:int):
        url = "delete_msg"
        params = {
            "message_id":messageID  # 消息ID
        }
        return self.session.get(self.ip+url, params=params)
    
    # 获取消息
    def getMessage(self, messageID:int):
        url = "get_msg"
        params = {
            "message_id":messageID  # 消息ID
        }
        # 响应内容: 
        # message_id(int32,消息id)
        # real_id(int32,消息真实id)
        # sender(object,发送者)
        # time(int32, 发送时间)
        # message(message,消息内容)
        # raw_message(message,原始消息内容)
        return self.session.get(self.ip+url, params=params)

    # 获取合并转发内容
    def getForwardMessage(self, messageID:str):
        url = "get_forward_msg"
        params = {
            "message_id":messageID  # 消息ID
        }
        # 响应内容: messages(forward message[], 消息列表)
        return self.session.get(self.ip+url, params=params)

    # 获取图片信息
    def getImage(self, file:str):
        url = "get_image"
        params = {
            "file":file  # 图片缓存文件名
        }
        # 响应内容: size(int32,图片源文件大小), filename(string,图片文件原名), url(string,图片下载地址)
        return self.session.get(self.ip+url, params=params)

    # 群组踢人
    def getImage(self, groupID:int, userID:int, rejectAddRequest=False):
        url = "set_group_kick"
        params = {
            "group_id":groupID,                     # 群号
            "user_id":userID,                       # QQ号
            "reject_add_request":rejectAddRequest   # 是否拒绝此人的加群请求
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 群组单人禁言
    def setGroupBan(self, groupID:int, userID:int, duration=30*60):
        url = "set_group_ban"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
            "duration":duration,   # 禁言时长(秒)(0位取消禁言)
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 群组匿名用户禁言
    def setGroupAnonymousBan(self, groupID:int, anonymous, anonymousFlag:str, duration=30*60):
        url = "set_group_anonymous_ban"
        params = {
            "group_id":groupID,                 # 群号
            "anonymous":anonymous,              # 要禁言的匿名用户对象(可选)(群消息上报的anonymous字段)
            "anonymous_flag":anonymousFlag,     # 要禁言的匿名用户的flag(可选)(需从群消息上报的数据中获得)
            "duration":duration,                # 禁言时长(秒)(无法取消匿名用户禁言)
        }
        # 上面的 anonymous 和 anonymous_flag 两者任选其一传入即可, 若都传入, 则使用 anonymous
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 群组全员禁言
    def setGroupWholeBan(self, groupID:int, enable=True):
        url = "set_group_whole_ban"
        params = {
            "group_id":groupID,    # 群号
            "enable":enable,       # 是否禁言
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 群组设置管理员
    def setGroupAdmin(self, groupID:int, userID:int, enable=True):
        url = "set_group_admin"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
            "enable":enable,       # true为设置,false为取消

        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 群组匿名
    def setGroupAnonymous(self, groupID:int, enable=True):
        url = "set_group_anonymous"
        params = {
            "group_id":groupID,    # 群号
            "enable":enable,       # 是否允许匿名聊天
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 群组设置群名片(群备注)
    def setGroupCard(self, groupID:int, userID:int, card=""):
        url = "set_group_card"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
            "card":card,           # 群名片内容(不填或为空字符串表示删除群名片)
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 设置群组
    def setGroupName(self, groupID:int, groupName:str):
        url = "set_group_name"
        params = {
            "group_id":groupID,         # 群号
            "group_name":groupName,     # 群名称
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 退出群组
    def setGroupLeave(self, groupID:int, isDismiss=False):
        url = "set_group_leave"
        params = {
            "group_id":groupID,     # 群号
            "is_dismiss":isDismiss, # 是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 设置群组专属头衔
    def setGroupSpecialTitle(self, groupID:int, userID:int, specialTitle="", duration=-1):
        url = "set_group_special_title"
        params = {
            "group_id":groupID,                 # 群号
            "user_id":userID,                   # QQ号
            "special_title":specialTitle,       # 专属头衔(不填或空字符串表示删除专属头衔)
            "duration":duration,                # 专属头衔有效期(秒)(-1 表示永久)
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 处理加好友请求
    def setFriendAddRequest(self, flag:str, approve=True, remark=""):
        url = "set_friend_add_request"
        params = {
            "flag":flag,          # 加好友请求的 flag(需从上报的数据中获得)
            "approve":approve,    # 是否同意请求
            "remark":remark,      # 添加后的好友备注(仅在同意时有效)
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    
    # 处理加群请求/邀请
    def setGroupAddRequest(self, flag:str, subType:str, type:str, approve=True, reason=""):
        url = "set_group_add_request"
        params = {
            "flag":flag,            # 加群请求的flag(需从上报的数据中获得)
            "sub_type":subType,     # 请求类型(add或invite)(需要和上报消息中的 sub_type 字段相符)
            # sub_type或使用type
            "approve":approve,      # 是否同意请求/邀请
            "reason":reason,        # 拒绝理由(仅在拒绝时有效)
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取登录号/企点号信息
    def getLoginInfo(self, mode:int):
        if mode == 0:
            url = "get_login_info"
            # 响应内容: user_id(int64, QQ号), nickname(string, QQ昵称)

        if mode == 1:
            url = "qidian_get_account_info"
            # 响应内容: master_id(int64, 父账号ID), ext_name(string, 用户昵称), create_time(int64, 账号创建时间)
        
        return self.session.get(self.ip+url)
     
    # 获取陌生人信息
    def getStrangerInfo(self, userID:int, noCache=False):
        url = "get_stranger_info"
        params = {
            "user_id":userID,        # QQ号
            "no_cache":noCache,      # 是否不使用缓存(使用缓存可能更新不及时, 但响应更快)
        }
        # 响应内容: 
        # user_id(int64, QQ号)
        # nickname(string, QQ昵称)
        # sex(string, 性别, male 或 female 或 unknown)
        # age(int32, 年龄)
        # qid(string, qid ID身份卡)
        # level(int32, 等级)
        # login_days(int32, 等级)
        res = self.session.get(self.ip+url, params=params)
        data = json.loads(res.text)
        return data
    
    # 获取好友列表
    def getFriendList(self):
        url = "get_friend_list"
        # 响应内容: user_id(int64, QQ号), nickname(string, 昵称), remark(string, 备注名), 
        return self.session.get(self.ip+url)
    
    # 删除好友
    def deleteFriend(self, friendID:int):
        url = "delete_friend"
        params = {
            "friend_id":friendID,    # 好友 QQ 号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)
    

    # 获取群信息
    # 获取群列表
    # 获取群成员信息
    # 获取群成员列表
    # 获取群荣誉信息
    # 获取Cookies
    # 获取CSRF Token
    # 获取QQ相关接口凭证(即上面两个接口的合并)
    # 获取语音
    # 检查是否可以发送图片/语音
    # 获取版本信息
    # 重启go-cqhttp
    # 清理缓存
    # 设置群头像
    # 获取中文分词(隐藏API)
    # 图片OCR
    # 获取群系统消息
    # 上传群文件
    # 获取群文件系统信息
    # 获取群根目录文件列表
    # 获取群子目录文件列表
    # 获取群文件资源链接
    # 获取状态
    # 获取群 @全体成员 剩余次数
    # 对事件执行快速操作(隐藏API)
    # 获取VIP信息
    # 发送群公告
    # 重载事件过滤器
    # 下载文件到缓存目录
    # 获取当前账号在线客户端列表
    # 获取群消息历史记录
    # 设置精华消息
    # 移除精华消息
    # 获取精华消息列表
    # 检查链接安全性
    # 获取在线机型
    # 设置在线机型









