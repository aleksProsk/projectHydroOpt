import os
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins
from datetime import date, timedelta, datetime

def compile_callbacks_file(source_code):
    locals = {}
    byte_code = compile_restricted(
        source = source_code,
        filename = '<inline>',
        mode = 'exec'
    )
    exec(byte_code, safe_builtins, locals)
    if 'objects' in locals:
        return locals['objects']
    return {}

def readObjects(uid, screenName):
    path = "user" + uid + "/scripts/dash/screens/"
    f = open(path + screenName + "/objects.py", "r")
    s = f.read()
    objectsLst = compile_callbacks_file(s)
    return objectsLst

#dct = compile_callbacks("001")