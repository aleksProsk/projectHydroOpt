import os
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins

def readDict(source_code):
    locals = {}
    byte_code = compile_restricted(
        source = source_code,
        filename = '<inline>',
        mode = 'exec'
    )
    exec(byte_code, safe_builtins, locals)
    if 'd' in locals:
        return locals['d']
    return []

def parse(uid):
    path = "user" + uid + "/scripts/dash/screens/"
    screenNames = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            screenNames.append(os.path.join(name))
    ansDict = []
    for screenName in screenNames:
        f = open(path + screenName + "/objectGraph.py", "r")
        s = f.read()
        curDict = readDict(s)
        for elem in curDict:
            elem['screen'] = screenName
        ansDict = ansDict + curDict
    return ansDict

dct = parse("001")