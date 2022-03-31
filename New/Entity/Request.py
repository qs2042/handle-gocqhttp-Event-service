import json


class Request:
    def __init__(self, conn, address, source) -> None:
        self.initlizationConstructorVariable(conn, address, source)
        self.initlizationVariable()
        self.analysis()
    
    def initlizationConstructorVariable(self, conn, address, source):
        self.conn = conn
        self.address = address
        self.source = source

    def initlizationVariable(self):
        self.method = None
        self.url = None
        self.agreement = None
        self.headers = {}
        self.data = {}

    def analysis(self):
        source = self.source
        sourceLines = source.splitlines()
        
        # 获取第一行(method, url, agreement, version)
        one:list = sourceLines[0].split(" ")
        self.method = one[0]
        self.url = one[1]
        self.agreement = one[-1].split("/")[0]
        self.version = one[-1].split("/")[-1]

        if self.method == "GET":
            # 获取第二行(headers)
            for i in sourceLines[1:]:
                if i == "":
                    break
                entry = i.split(": ")
                self.headers[entry[0]] = entry[-1]

            # 获取第三行(空格)

            # 获取第四行(body)
            if "?" in self.url:
                data = self.url.split("?")[-1]
                self.url = self.url.split("?")[0]

                for i in data.split("&"):
                    k = i.split("=")[0]
                    v = i.split("=")[-1]
                    self.data[k] = v
        
        if self.method == "POST":
            # 获取第二行(headers)
            for i in source.split("\r\n\r\n")[0].splitlines()[1:]:
                if i == "":
                    break
                entry = i.split(": ")
                self.headers[entry[0]] = entry[-1]
                    
            # 获取第三行(空格)

            # 获取第四行(body)
            self.data = json.loads(source.split("\r\n\r\n")[-1])
    
    def __str__(self) -> str:
        result = "请求方法: " + str(self.method) + "\n" + \
            "请求路径: " + str(self.url) + "\n" + \
            "请求版本: " + str(self.agreement) + "\n" + \
            "请求头: " + str(self.headers) + "\n" + \
            "请求参数: " + str(self.data)
        return result

