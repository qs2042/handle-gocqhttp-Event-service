import socket,json,threading,asyncio,time

from Dispatcher import Qiass as Dispatcher  # 前端控制器
from Utils import Request,Response,Utils    # Utils
from Log import Qiass as Log                # Log

'''
流程图
Server      接收请求
↓   ↓   ↓   ↓   ↓   ↓
Dispatcher  派发请求
↓   ↓   ↓   ↓   ↓   ↓
HTML5       →   Event   →   Function
go-cqhttp   →   Event   →   ...
↓   ↓   ↓   ↓   ↓   ↓
'''


class Qiass:
    def __init__(self, ipPort=("127.0.0.1", 5701), bufsize=1024) -> None:
        self.initilizationConstructorVariable(ipPort, bufsize)
        self.initilizationSocket()
        self.initilizationObject()

    def initilizationConstructorVariable(self, ipPort, bufsize):
        self.ipPort = ipPort
        self.bufsize = bufsize
    def initilizationSocket(self):
        # 创建一个socket对象
        # AF_INET       = 服务器之间网络通信
        # SOCK_STREAM   = 流式socket , for TCP
        listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 添加Address
        # address = self.ipPort;listenSocket.bind(address)
        listenSocket.bind(self.ipPort)

        # 设置超时时间
        # listenSocket.settimeout(100)

        # 设置最大连接数|开始监听TCP传入连接。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。
        listenSocket.listen(1)

        self.listenSocket = listenSocket
        return True
    def initilizationObject(self):
        self.dispatcher = Dispatcher()
        self.utils = Utils()
        self.log = Log("Server")

    def getConn(self, isDecode="utf-8"):
        # 接受TCP连接并返回(conn,address)
        # conn      新的套接字对象, 可以用来接收和发送数据
        # address   连接客户端的地址
        conn, Address = self.listenSocket.accept()

        # 接受TCP套接字的数据, 数据以字符串形式返回
        # bufsize指定要接收的最大数据量
        # flag提供有关消息的其他信息, 通常可以忽略
        if isDecode == False:
            request = conn.recv(self.bufsize)
        if isDecode != False:
            request = conn.recv(self.bufsize).decode(encoding=isDecode)
        return {"conn":conn, "address":Address, "source":request}

    def sendAll(self, conn, response:Response):
        conn.sendall(bytes(response.result(), "utf-8"))
        return True

    def close(self, conn:socket):
        conn.close()
        return True
    


    def printLog(self, request:Request, response:Response):
        print("*"*25, "request" ,"*"*25)
        self.log.INFO(info="request", time=True, thread=True, count="request")
        self.log.INFO(info=request.method, title="请求方式", time=True, thread=True)
        self.log.INFO(info=request.url, title="请求路径", time=True, thread=True)
        self.log.INFO(info=request.version, title="请求版本", time=True, thread=True)
        #self.log.INFO(info=request.headers, title="请求头", time=True, thread=True)
        #for i in request.headers:
        #    self.log.INFO(info=request.headers[i], title=["请求头", i], time=True, thread=True)
        self.log.INFO(info=request.data, title="请求参数", time=True, thread=True)
        print("*"*25, "response" ,"*"*25)
        self.log.TEST("%s/%s" % (response.agreement, response.version), title="返回版本")
        self.log.TEST(response.statusCode, title="返回状态码")
        self.log.TEST(response.text, title="返回内容")
        self.log.TEST(response.headers, title="返回头")
        self.log.TEST(response.info["application"], title=["功能信息", "应用名称"])
        self.log.TEST(response.info["function"], title=["功能信息", "功能名称"])
        self.log.TEST(response.info["result"], title=["功能信息", "返回数据"])
        self.log.TEST(response.info["runTime"], title=["功能信息", "运行时间"])
        self.log.TEST(response.info["showDatabase"], title=["功能信息", "显示数据"])
        print("\n\n\n")

    # 因为多线程导致的问题: 消息乱窜, 打印错位, 多线程有时候会报错
    # 消息乱窜: 加个sleep就解决了
    # 打印错位: 加个sleep就解决了一半, 可能是因为打印需要的资源太多了, 后期可改成日志存数据库, 再从数据库中读取并展示
    def run(self, isLog=True):
        # ...
        data:dict = self.getConn("utf-8")
        conn = data["conn"]
        address = data["address"]
        source:str = data["source"]
        
        # 将报文(source)注入到Request类中
        try:
            request = self.utils.analysisSource(source)
        except:
            self.log.ERROR(source[source.find("{"):], title="解析异常")
            print("\n\n")
            return None
        
        # 将请求进行派发
        response = self.dispatcher.main(request, Response())

        # 响应请求
        self.sendAll(conn, response)

        # 关闭连接
        self.close(conn)

        if response.info["application"] == "go-cqhttp":
            if response.info["function"] == "interval":return None
            if response.info["result"] == "None":return None
        if response.info["application"] == "go-cqhttp":pass

        if isLog == True:self.printLog(request, response)
            
        return None

    def main(self):
        self.utils.serverInfo()

        while True:
            time.sleep(2)
            t = threading.Thread(target=self.run)
            t.start()
                
                

    def mainOld(self, isLog=True):
        self.utils.serverInfo()

        while True:
            data:dict = self.getConn("utf-8")
            conn = data["conn"]
            address = data["address"]
            source:str = data["source"]
            try:
                # 把报文(source) 注入到request类中
                request = self.utils.analysisSource(source)
            except:
                self.log.ERROR(source[source.find("{"):], title="解析异常")
                print("\n")
                continue

            # [Socket] 把request类传递给Dispatcher进行请求派发, 并根据事件处理器的返回数据进行返回
            #try:
            response = self.dispatcher.main(request, Response())
            if response.info["application"] == "HTML5":
                response.text = "测试web"
            if response.info["application"] == "go-cqhttp":
                response.text = "测试gocqhttp"
            #except:
            #    self.log.ERROR("未知的错误 - 101")
            
            #try:
            self.sendAll(conn, response)
            # [Socket]关闭连接
            self.close(conn)
            #except:
            #self.log.ERROR("未知的错误 - 102")
            
            # [Log] 如果是go-cqhttp
            if response.info["application"] == "go-cqhttp":
                # 如果此间无触发(即interval)那么就不输出日志
                if response.info["function"] == "interval":
                    continue
                # 如果此间有触发但是没有完全触发, 那么就不输出日志
                if response.info["result"] == "None":pass
            
            # [Log] 如果是web
            if response.info["application"] == "HTML5":
                # 如果地址/资源不存在...
                pass
            # [Log] 是否打印日志
            if isLog:
                print("*"*25, "request" ,"*"*25)
                self.log.INFO(info="request", time=True, thread=True, count="request")
                self.log.INFO(info=request.method, title="请求方式", time=True, thread=True)
                self.log.INFO(info=request.url, title="请求路径", time=True, thread=True)
                self.log.INFO(info=request.version, title="请求版本", time=True, thread=True)
                #self.log.INFO(info=request.headers, title="请求头", time=True, thread=True)
                #for i in request.headers:
                #    self.log.INFO(info=request.headers[i], title=["请求头", i], time=True, thread=True)
                self.log.INFO(info=request.data, title="请求参数", time=True, thread=True)
                print("*"*25, "response" ,"*"*25)
                self.log.TEST("%s/%s" % (response.agreement, response.version), title="返回版本")
                self.log.TEST(response.statusCode, title="返回状态码")
                self.log.TEST(response.text, title="返回内容")
                self.log.TEST(response.headers, title="返回头")
                self.log.TEST(response.info["application"], title=["功能信息", "应用名称"])
                self.log.TEST(response.info["function"], title=["功能信息", "功能名称"])
                self.log.TEST(response.info["result"], title=["功能信息", "返回数据"])
                self.log.TEST(response.info["runTime"], title=["功能信息", "运行时间"])
                self.log.TEST(response.info["showDatabase"], title=["功能信息", "显示数据"])
                print("\n\n\n")





if __name__ == "__main__":
    q = Qiass(("127.0.0.1", 5701))
    q.main()
    # http://127.0.0.1:5701/?a=1&b=2&c=3




