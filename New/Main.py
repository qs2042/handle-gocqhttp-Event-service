import socket
###################################################
# Core
###################################################
from Core.Dispatcher import Dispatcher

###################################################
# Utils
###################################################
from Utils.Decorator import InstructionMapping,prefix
from Utils import Decorator
from Utils.Log import Log
from Utils.Reflection import Reflection
from Utils.Sqlite3 import Sqlite3

###################################################
# Entity
###################################################
from Entity.Request import Request
from Entity.Response import Response

from HTML5.Event import Event as Event_H
from Robot.Event import Event as Event_R

class Server: 
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
    def initilizationObject(self):
        self.dispatcher = Dispatcher()
        self.log = Log("Server")
        self.map = {
            "event_H":Event_H(),
            "event_R":Event_R(),
            "Utils":{
                "Log":Log,
                "Reflection":Reflection,
                "Sqlite3":Sqlite3,
                "Decorator":Decorator,
            },
            "Request":None,
            "Response":None,
            "result":{
                "application":None,
                "function":None,
                "result":None,
                "runTime":None,
                "logInfo":None,
            }
        }

    def refreshResult(self):
        self.map["result"] = {
                "application":None,
                "function":None,
                "result":None,
                "runTime":None,
                "logInfo":None,
        }

    def getConn(self, isDecode="utf-8"):
        # 接受TCP连接并返回(conn,address)
        # conn      新的套接字对象, 可以用来接收和发送数据
        # address   连接客户端的地址
        conn, address = self.listenSocket.accept()

        # 接受TCP套接字的数据, 数据以字符串形式返回
        # bufsize指定要接收的最大数据量
        # flag提供有关消息的其他信息, 通常可以忽略
        if isDecode == False:
            source = conn.recv(self.bufsize)
        if isDecode != False:
            source = conn.recv(self.bufsize).decode(encoding=isDecode)
        return conn,address,source
    def sendAll(self, conn, response):
        conn.sendall(bytes(response.result(), "utf-8"))
        return True
    def close(self, conn):
        conn.close()
        return True
    
    def handler(self):
        # 获取套接字
        conn,address,source = self.getConn("utf-8")

        # 解析报文注入属性到Request实体类中
        try:
            self.map["request"] = Request(conn,address,source)
        except:
            print(source)
            return False
        self.map["response"] = Response()

        # 将请求进行派发
        self.dispatcher.main(self.map)

        # 响应请求
        self.sendAll(conn, self.map["response"])

        self.log.TEST("\n" + str(self.map["request"]), title=["Entity", "Request"], time=True, thread=True)
        self.log.TEST("\n" + str(self.map["response"]), title=["Entity", "Response"], time=True, thread=True)
        self.log.TEST("\n" + str(self.map.get("result")), title="ApplicationContext", time=True, thread=True)
        print("\n\n")

        # 关闭连接
        self.close(conn)

    def main(self):
        while True:
            self.refreshResult()
            self.handler()
            


if __name__ == "__main__":
    s = Server(("127.0.0.1", 5701), 1024)
    s.main()