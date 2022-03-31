



class Response:
    def __init__(self) -> None:
        self.agreement = "HTTP/1.1"
        self.statusCode = "200"
        self.text = "<h1> True </h1>"
        self.headers = {
            "Content-Type": "text/html;charset=utf-8",
        }

    def getHeaders(self):
        s = ""
        for i in self.headers:
            s += "%s: %s\n" % (i, self.headers[i])
        return s[:-1]
        
    def result(self):
        return "%s %s OK \n%s\r\n\r\n %s" % (
            self.agreement,
            self.statusCode, 
            self.getHeaders(), self.text)

    def __str__(self) -> str:
        result = "返回版本: " + self.agreement + "\n" + \
            "返回状态码: " + self.statusCode + "\n" + \
            "返回信息: " + self.text + "\n" + \
            "返回请求头: " + str(self.headers)
        return result