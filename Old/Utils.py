import json,re

class Request:
    def __init__(self) -> None:
        self.method = None
        self.url = None
        self.version = None
        self.headers = {}
        self.data = {}
    
    def __str__(self) -> str:
        result = "请求方法: " + str(self.method) + "\n" + \
            "请求路径: " + str(self.url) + "\n" + \
            "请求版本: " + str(self.version) + "\n" + \
            "请求头: " + str(self.headers) + "\n" + \
            "请求参数: " + str(self.data)
        return result

class Response:
    def __init__(self) -> None:
        self.agreement = "HTTP"
        self.version = "1.1"
        self.statusCode = "200"
        self.text = "<h1> True </h1>"
        self.headers = {
            "Content-Type": "text/html;charset=utf-8",
        }
        self.info = {
            "application":"None",   # 应用名称
            "function":"None",      # 功能名称
            "result":"None",        # 功能返回数据
            "runTime":"0",          # 运行时间
            "showDatabase":"None",  # 显示数据 
        }

    def __str__(self) -> str:
        result = "返回版本: " + self.agreement + "/" + self.version + "\n" + \
            "返回状态码: " + self.statusCode + "\n" + \
            "返回信息: " + self.text + "\n" + \
            "返回请求头: " + str(self.headers)
        return result
    
    def getHeaders(self):
        s = ""
        for i in self.headers:
            s += "%s: %s\n" % (i, self.headers[i])
        return s[:-1]
    
    def result(self):
        return "%s/%s %s OK \n%s\r\n\r\n %s" % (self.agreement, self.version, self.statusCode, self.getHeaders(), self.text)

class Utils:
    def serverInfo(self):
        print("*" * 50)
        print("Based: [go-cqhttp][python, socket]")
        print("Author: 晴兽")
        print("version: 1.0")
        print("*" * 50)
        print("...")
        print("\n"*3)

    def analysisSource(self, source:str) -> Request:
        request = Request()

        # 获取第一行(method url version)
        requestLine = source.splitlines()[0]
        request.method = requestLine.split(" ")[0]
        request.url = requestLine.split(" ")[1]
        request.version = requestLine.split(" ")[-1]

        # GET
        if request.method == "GET":
            # 获取第二行(headers)
            requestHeaders = {}
            for i in source.splitlines()[1:]:
                if i == "":
                    continue
                entry = i.split(": ")
                requestHeaders[entry[0]] = entry[-1]
            request.headers = requestHeaders

            # 获取第三行(空行)
            emptyLine = None
            
            # 获取第四行(Body)(只有POST才有)
            body = None
            if "?" in request.url:
                request.data = {}
                data = request.url.split("?")[-1]
                request.url = request.url.split("?")[0]
                for i in data.split("&"):
                    k = i.split("=")[0]
                    v = i.split("=")[-1]
                    request.data[k] = v


        # POST
        if request.method == "POST":
            # 获取第二行(headers)
            requestHeaders = {}
            for i in source.split("\r\n\r\n")[0].splitlines()[1:]:
                if i == "":
                    continue
                entry = i.split(": ")
                requestHeaders[entry[0]] = entry[-1]
            request.headers = requestHeaders

            # 获取第三行(空行)
            emptyLine = None

             # 获取第四行(Body)(只有POST才有)
            body = None
            request.data = json.loads(source.split("\r\n\r\n")[-1])
        
        return request




    

        


