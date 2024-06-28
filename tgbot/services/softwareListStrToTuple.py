def softwareListStrToTuple(message:str) -> list:
    res = tuple(map(str, message.split(',')))
    new_res = []
    print (f"old tuple - {res}")
    for soft in res:
        soft = soft.strip()
        new_res.append(soft)
    print (f"new list - {new_res}")
    return new_res

