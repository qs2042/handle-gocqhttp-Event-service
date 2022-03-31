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
    def getGroupInfo(self, groupID:int, noCache=False):
        url = "get_group_info"
        params = {
            "group_id":groupID,    # 群号
            "no_cache":noCache,    # 是否不使用缓存(使用缓存可能更新不及时, 但响应更快)
        }
        # 响应内容: 
        # group_id(int64, 群号)
        # group_name(string, 群名称)
        # group_memo(string, 群备注)
        # group_create_time(uint32, 群创建时间)
        # group_level(uint32, 群等级)
        # member_count(int32, 成员数)
        # max_member_count(int32, 最大成员数-群容量)

        # 这里提供了一个API用于获取群图片, group_id 为群号
        # https://p.qlogo.cn/gh/{group_id}/{group_id}/100
        return self.session.get(self.ip+url, params=params)
    
    # 获取群列表
    def getGroupList(self):
        url = "get_group_list"
        # 响应内容: JSON数组
        # group_id(int64, 群号)
        # group_name(string, 群名称)
        # group_memo(string, 群备注)
        # group_create_time(uint32, 群创建时间)
        # group_level(uint32, 群等级)
        # member_count(int32, 成员数)
        # max_member_count(int32, 最大成员数-群容量)
        return self.session.get(self.ip+url)
    
    # 获取群成员信息
    def getGroupMemberInfo(self, groupID:int, userID:int, noCache=False):
        url = "get_group_member_info"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
            "no_cache":noCache,    # 是否不使用缓存(使用缓存可能更新不及时, 但响应更快)
        }
        # 响应内容: 
        # group_id(int64, 群号)
        # user_id(int64, QQ号)
        # nickname(string, 昵称)
        # card(string, 群名片/备注)
        # sex(string, 性别, male 或 female 或 unknown)
        # age(int32, 年龄)
        # area(string, 地区)

        # join_time(int32, 加群时间戳)
        # last_sent_time(int32, 最后发言时间戳)
        # level(string, 成员等级)
        # role(string, 角色, owner 或 admin 或 member)
        # unfriendly(boolean, 是否不良记录成员)
        # title(string, 专属头衔)
        # title_expire_time(int64, 专属头衔过期时间戳)
        # card_changeable(boolean, 是否允许修改群名片)
        # card_changeable(int64, 禁言到期时间)
        return self.session.get(self.ip+url, params=params)
    
    # 获取群成员列表
    def getGroupMmberList(self, groupID:int):
        url = "get_group_member_list"
        params = {
            "group_id":groupID,    # 群号
        }
        # 响应内容: json 数组
        # 每个元素的内容和上面的 get_group_member_info 接口相同
        # 但对于同一个群组的同一个成员, 获取列表时和获取单独的成员信息时
        # 某些字段可能有所不同, 例如 area、title 等字段在获取列表时无法获得, 具体应以单独的成员信息为准
        return self.session.get(self.ip+url, params=params)
    
    # 获取群荣誉信息
    def getGroupHonorInfo(self, groupID:int, type:str):
        url = "get_group_honor_info"
        params = {
            "group_id":groupID,    # 群号
            "type":type,           # 要获取的群荣誉类型, 可传入 talkative performer legend strong_newbie emotion 以分别获取单个类型的群荣誉数据, 或传入 all 获取所有数据
        }
        # 响应内容: 
        '''
        group_id	        int64	群号
        current_talkative	object	当前龙王, 仅 type 为 talkative 或 all 时有数据
        talkative_list	    array	历史龙王, 仅 type 为 talkative 或 all 时有数据
        performer_list	    array	群聊之火, 仅 type 为 performer 或 all 时有数据
        legend_list	        array	群聊炽焰, 仅 type 为 legend 或 all 时有数据
        strong_newbie_list	array	冒尖小春笋, 仅 type 为 strong_newbie 或 all 时有数据
        emotion_list	    array	快乐之源, 仅 type 为 emotion 或 all 时有数据


        其中 current_talkative 字段的内容如下: 
        user_id	    int64	QQ 号
        nickname	string	昵称
        avatar	    string	头像 URL
        day_count	int32	持续天数


        其它各 *_list 的每个元素是一个 json 对象, 内容如下:
        user_id	    int64	QQ 号
        nickname	string	昵称
        avatar	    string	头像 URL
        description	string	荣誉描述
        '''
        return self.session.get(self.ip+url, params=params)
    


    # 获取Cookies(False)
    def getCookies(self, domain:str):
        url = "get_cookies"
        params = {
            "domain":domain,    # 需要获取 cookies 的域名
        }
        # 响应内容: cookies(string, Cookies)
        return self.session.get(self.ip+url, params=params)

    # 获取CSRF Token(False)
    def getCsrfToken(self):
        url = "get_csrf_token"
        # 响应内容: token(int32, CSRF Token)
        return self.session.get(self.ip+url)

    # 获取QQ相关接口凭证(即上面两个接口的合并)(False)
    def getCredentials(self, groupID:int, userID:int, domain:str):
        url = "get_credentials"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取语音
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 检查是否可以发送图片/语音
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取版本信息
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 重启go-cqhttp
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 清理缓存
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 设置群头像
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取中文分词(隐藏API)
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 图片OCR
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取群系统消息
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 上传群文件
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取群文件系统信息
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取群根目录文件列表
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取群子目录文件列表
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取群文件资源链接
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取状态
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取群 @全体成员 剩余次数
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 对事件执行快速操作(隐藏API)
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)

    # 获取VIP信息
    def template(self, groupID:int, userID:int):
        url = "None"
        params = {
            "group_id":groupID,    # 群号
            "user_id":userID,      # QQ号
        }
        # 响应内容: None
        return self.session.get(self.ip+url, params=params)


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









