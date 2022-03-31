import threading,time


class Utils:
    def timeLocal():
        res = time.localtime()
        result = "%s年%s月%s日 %s:%s(%s)" % (
            res.tm_year,
            res.tm_mon,
            res.tm_mday,
            res.tm_hour,
            res.tm_min,
            res.tm_sec
        )
        return result

class Log:
    def __init__(self, applicationName:str) -> None:
        self.applicationName = applicationName
        self.dataCount = { "countName":"countNumber" }

    def getCount(self, countName):
        number = self.dataCount.get(countName)
        if number == None:
            self.dataCount[countName] = 0
            return "0"
        
        self.dataCount[countName] += 1
        return str(number + 1)
        

    def __message(self, main, info, time, thread, cound, title):
        result = "[main][application][time][thread][cound][title] [info]"
        result = result.replace("main", main).replace("application", self.applicationName)
        result = result.replace("[info]", info)

        if time != "":
            time = Utils.timeLocal()
        if thread != "":
            thread = "%s-%s" % (threading.currentThread().getName(), threading.currentThread().ident)
        if cound != "":
            cound = str(self.getCount(cound))
        if title != "":
            if type(title) != list:
                tmp = title
                title = []
                title.append(tmp)
            titleResult = ""
            for i in title:
                titleResult += "[%s]" % i
            title = titleResult

        result = result.replace("time", time)
        result = result.replace("thread", thread)
        result = result.replace("cound", cound)
        result = result.replace("[title]", title)
        return result.replace("[]", "")

    def TEST(self, info, time="", thread="", count="", title=""):
        print(self.__message("TEST", info, time, thread, count, title))
    def INFO(self, info, time="", thread="", count="", title=""):
        print(self.__message("INFO", info, time, thread, count, title))
    def DEBUG(self, info, time="", thread="", count="", title=""):
        print(self.__message("DEBUG", info, time, thread, count, title))
    def ERROR(self, info, time="", thread="", count="", title=""):
        print(self.__message("ERROR", info, time, thread, count, title))
    
'''
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
    '''


if __name__ == "__main__":
    pass
