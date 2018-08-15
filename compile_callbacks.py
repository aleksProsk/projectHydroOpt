import os
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins
from datetime import date, timedelta, datetime
import base64

def split(c, s):
    return s.split(c)

def compile_callbacks_file(source_code, getScreenVariables, log):
    locals = {}
    byte_code = compile_restricted(
        source = source_code,
        filename = '<inline>',
        mode = 'exec'
    )
    additional_globals = {
        'date': date, 'timedelta': timedelta, 'datetime': datetime, 'getScreenVariables': getScreenVariables, 'log': log, 'decodeFile': base64.b64decode, 'split': split
    }
    safe_globals = safe_builtins
    safe_globals.update(additional_globals)
    exec(byte_code, safe_globals, locals)
    return locals

def compile_callbacks(uid, screenName, getScreenVariables, log):
    path = "user" + uid + "/scripts/dash/screens/"
    f = open(path + screenName + "/callbacks.py", "r")
    s = f.read()
    functionLst = compile_callbacks_file(s, getScreenVariables, log)
    return functionLst

#dct = compile_callbacks("001")