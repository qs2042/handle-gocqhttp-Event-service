import time


class Dispatcher:
    def robot(self, map:dict):
        request = map.get("request")
        if not "CQHttp" in request.headers["User-Agent"]:
            return None
        
        result = map.get("result")
        result["application"] = "go-cqhttp"
        
        map.get("event_R").main(map)
        return None

    def html5(self, map:dict):
        request = map.get("request")
        if not "Chrome" in request.headers["User-Agent"]:
            return None
        
        result = map.get("result")
        result["application"] = "HTML5"

        map.get("event_H").main(map)
        return None

    def main(self,map:dict):
        start = time.time()

        result = map.get("result")
        if result["application"] == None:
            self.robot(map)
        if result["application"] == None:
            self.html5(map)

        end = time.time()
        result["runTime"] = (end - start)