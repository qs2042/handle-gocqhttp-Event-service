



class Event:
    def __init__(self) -> None:
        pass
    

    def main(self, map:dict):
        request = map["request"]
        response = map["response"]

        response.text = "[test] HTML5 <br> [测试] HTML5网页"
        pass

            
