from functools import wraps
from textwrap import wrap



def InstructionMapping(value="", handleReturn=True):
    def isTriggerInstruction(text, instruction, isCleanSpaces=True):
        # 对Value进行转换, 不管任何类型都转为list
        if type(instruction) != list:
            tmp = instruction
            instruction = []
            instruction.append(tmp)
        
        switch = False
        for i in instruction:
            # 指令如果是False,'',[]那么就直接放行
            if i == False or i == None or i == '' or i == []:
                # switch = True
                # break
                return text
            if i == text[:len(i)]:
                switch = True
                result = text[len(i):]
                break
        
        # 如果没触发指令
        if not switch:
            return False

        # 如果触发了指令(这里不用判断switch)

        # 是否要去空格
        if isCleanSpaces:
            i = 0
            for items in result:
                if items == " ":
                    i += 1
            if i > 0:
                result = result[i:]
        if result == "":
            return "Default"
        return result

    def mapping_decorator(func):
        def warpper(*args, **kwargs):
            result = isTriggerInstruction(kwargs["text"], value)
            # 前缀不匹配
            if not result:
                # 用户不想自己在函数内处理返回值
                if handleReturn:return result
            return func(self=kwargs.get("self"),result=result,kwargs=kwargs)
        return warpper
    return mapping_decorator

def Print(first = "", behind= ""):
    def decorator(func):
        def warpper(*args, **kwargs):
            if first != "":print(first)
            result = func(*args, **kwargs)
            if behind != "":print(behind)
            return result
        return warpper
    return decorator


def mapping(value=""):
    def isTriggerInstruction(text, instruction, isCleanSpaces=True):
        if type(instruction) != list:
            tmp = instruction
            instruction = []
            instruction.append(tmp)
        switch = False
        for i in instruction:
            if i == False or i == None or i == '' or i == []:
                switch = True
                break
            if i == text[:len(i)]:
                switch = True
                result = text[len(i):]
                break
        
        # 如果没触发指令
        if not switch:
            return False

        # 如果触发了指令(这里不用判断switch)
        if isCleanSpaces:
            i = 0
            for items in result:
                if items == " ":
                    i += 1
            if i > 0:
                result = result[i:]
        return result
    
    def mapping_decorator(func):
        def warpper(*args, **kwargs):
            # 获取传进来的消息
            text = kwargs["text"]
            instruction = value
            if kwargs.get("self") == None:
                kwargs["self"] = None
            if kwargs.get("utils") == None:
                kwargs["utils"] = None
            if kwargs.get("data") == None:
                kwargs["data"] = None
            # 判断是否触发指令
            result = isTriggerInstruction(text, instruction)
            return func(self=kwargs["self"],result=result,utils=kwargs["utils"],data=kwargs["data"])
        return warpper
    return mapping_decorator


@mapping(value=["点歌", "给我来一首", "我想听"])
def test1(**kwargs):
    return kwargs

@mapping(value="点歌")
def test2(**kwargs):
    return kwargs

class Test:
    @mapping(value=["点歌", "给我来一首", "我想听"])
    def test1(self, *args, **kwargs):
        return kwargs
    
    @mapping(value="点歌")
    def test2(self, *args, **kwargs):
        return kwargs

if __name__ == "__main__":
    t = Test()
    














