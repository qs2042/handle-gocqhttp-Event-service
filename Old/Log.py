import threading,sys,os
from Function import Qiass as Function

class Qiass:
    def __init__(self, applicationName:str) -> None:
        self.initilizationConstructorVariable(applicationName)
        self.initilizationVariable()

    def initilizationConstructorVariable(self, applicationName):
        self.applicationName = applicationName
    
    def initilizationVariable(self):
        self.dataCount = {
            "countName":"countNumber",
        }
        self.fun = Function()
    
    def getCount(self, countName):
        result = self.dataCount.get(countName)
        if result == None:
            self.dataCount[countName] = 0
            return 0
        
        self.dataCount[countName] = result + 1
        return result + 1
        


    def __message(self, main, info, time, thread, count, title):
        result = "[main][application][time][thread][count][title] [info]"
        result = result.replace("main", main)
        result = result.replace("application", self.applicationName)

        if time == None:
            result = result.replace("[time]", "")
        if time != None:
            result = result.replace("time", self.fun.timeLocal(4))
        
        if thread == None:
            result = result.replace("[thread]", "")
        if thread != None:
            result = result.replace("thread", "%s-%s" % (threading.currentThread().getName(), threading.currentThread().ident))
        
        if count == None:
            result = result.replace("[count]", "")
        if count != None:
            result = result.replace("count", str(self.getCount(count)))
        
        if title == None:
            result = result.replace("[title]", "")
        if title != None:
            if type(title) != list:
                tmp = title
                title = []
                title.append(tmp)
            titleResult = ""
            for i in title:
                titleResult += "[%s]" % i
            result = result.replace("[title]", titleResult)
        
        if info == None:
            result = result.replace("[info]", "")
        if info != None:
            result = result.replace("[info]", str(info))
        
        return result

    def TEST(self, info, title=None,isTest=True):
        if isTest:
            print(self.__message("TEST", info,time=True,thread=True,count=None,title=title))

    def INFO(self, info, time=None, thread=None, count=None, title=None,isTest=True):
        if isTest:
            print(self.__message("INFO", info,time,thread,count,title))

    def ERROR(self, info, time=None, thread=None, count=None, title=None,isTest=True):
        if isTest:
            print(self.__message("ERROR", info,time,thread,count,title))

    def DEBUG(self, info, time=None, thread=None, count=None, title=None,isTest=True):
        if isTest:
            print(self.__message("DEBUG", info,time,thread,count,title))
    


if __name__ == "__main__":
    log = Qiass()
