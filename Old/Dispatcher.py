import time
from Utils import Request,Response

from Robot.Event import Qiass as RobotEvent
from HTML5.Event import Qiass as HTML5Event


class Qiass:
    def __init__(self) -> None:
        self.robotEvent = RobotEvent()
        self.html5Event = HTML5Event()
    
    def robot(self):
        if not "CQHttp" in self.request.headers["User-Agent"]:
            return None
        self.response.info["application"] = "go-cqhttp"
        self.robotEvent.main(self.request, self.response)
        return None
        
    def web(self):
        if not "Chrome" in self.request.headers["User-Agent"]:
            return None

        self.response.info["application"] = "HTML5"
        self.html5Event.main(self.request, self.response)
        return None
    
    def mainInilization(self, request:Request, response:Response) -> Response:
        self.request = request
        self.response = response
    def main(self, request:Request, response:Response):
        self.mainInilization(request, response)

        start = time.time()

        if response.info["application"] == "None":
            self.robot()
        if response.info["application"] == "None":
            self.web()

        end = time.time()
        response.info["runTime"] = (end - start)
        if response.info["application"] == "HTML5":
            response.text = "测试web"
        if response.info["application"] == "go-cqhttp":
            response.text = "测试gocqhttp"
        return response