




class Reflection:
    def __init__(self, targetObject) -> None:
        self.obj = targetObject
    
    # 获取所有类成员变量
    def getVariables(self):
        data = self.obj.__dict__
        if len(data) == 0:
            return False
        result = {
            "variableHide":[],
            "variable":[]
        }
        return data
    
    # 获取所有类方法
    def getMethods(self):
        l = dir(self.obj)
        result = {
            "pythonHide":[],
            "programmerHide":[],
            "method":[]
        }
        for i in l:
            if i[:2] == "__":
                result["pythonHide"].append(i)
                continue
            if i[:1] == "_":
                result["programmerHide"].append(i)
                continue

            result["method"].append(i)
        return result



    # 获取指定函数/方法的注解
    def getMethodAnnotations(self, func):
        return func.__annotations__
    
    # 获取类成员变量/方法
    def getAttribute(self, attributeName:str):
        try:
            return self.obj.__getattribute__(attributeName)
        except:
            return False

    # 设置类成员变量/方法
    def setAttribute(self, attributeName:str, value):
        self.obj.__setattr__(attributeName, value)
        return True

    # 删除类成员变量/方法
    def delAttribute(self, attributeName:str):
        try:
            return self.obj.__delattr__(attributeName)
        except:
            return False


if __name__ == "__main__":pass
