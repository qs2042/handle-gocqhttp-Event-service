from Robot.Function import Function



class Event:
    def __init__(self) -> None:pass
    def funMessage(self):
        # TODO
        # 这里利用反射批量调用Function类里的方法功能
        pass
    def funNotice(self):pass    # TODO
    def funRequest(self):pass   # TODO


    def main(self, map:dict):
        self.map = map

        request = map["request"]
        response = map["response"]

        if request.data.get("interval") != None:
            map["result"]["function"] = "interval"
            map["result"]["result"] = "无触发"
            return None
        
        data = request.data
        post_type = data["post_type"]

        # 匿名
        if post_type == "message":
            if data.get("anonymous") != None:pass

        # 私聊, 群聊
        if post_type == "message":
            map["result"]["function"] = "message"
            map["result"]["result"] = "暂无返回值"
            # 执行功能
            # 发送结果
            self.funMessage()
            pass
        
        if post_type == "notice":
            map["result"]["function"] = "notice"
            map["result"]["result"] = "暂无返回值"
            # 执行功能
            # 发送结果
            pass

        if post_type == "request":
            map["result"]["function"] = "request"
            map["result"]["result"] = "暂无返回值"
            # 执行功能
            # 发送结果
            pass