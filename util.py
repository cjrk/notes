#!/usr/bin/env python3

import re
import os
import time
import configparser
import sys
from dateutil.relativedelta import relativedelta
import subprocess

def env(var):
    return os.environ.get(var)

def assureDirFor(filePath):
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

def assureFile(path, content):
    if not os.path.isfile(path):
        assureDirFor(path)
        with open(path,'w') as f:
            f.write(content)

def read_config(configPath, defaultconfig):
    assureFile(configPath, defaultconfig)
    config = configparser.ConfigParser(interpolation=None)
    config.read(configPath)
    def configFn(section=None, option=None):
        try:
            if not section:
                return config
            if not option:
                return config[section]
            return config.get(section, option)
        except configparser.NoOptionError:
            return None
    return configFn

def beginsWithLetter(s):
    return re.match(r'^[A-Za-z_]+', s) != None

def dateTransformer(s):
    m = re.search(r'([+-]?)([0-9]+)([dwmyDWMY]?)', s)
    if m == None or len(m.groups()) != 3:
        return None
    sign, value, unit = m.groups()
    signFactor = -1 if sign == '-' else 1
    value = int(value) * signFactor
    unit = unit.lower()
    # return fn(date) which returns the modified date
    if unit == 'w':
        return lambda d: d + relativedelta(weeks=value)
    elif unit == 'm':
        return lambda d: d + relativedelta(months=value)
    elif unit == 'y':
        return lambda d: d + relativedelta(years=value)
    else: # day
        return lambda d: d + relativedelta(days=value)

def filterStringsFrom(lst):
    return list(filter(beginsWithLetter, lst))

def filterDatesFrom(lst):
    dates = list(map(dateTransformer, lst))
    return [i for i in dates if i] # remove None-items

def filterOptionsFrom(lst):
    return [i for i in lst if i[:2] == '--'] # remove None-items

def firstFromTwo(lst):
    return lst[0] if len(lst) == 2 else None

def secondFromTwo(lst):
    return lst[1] if len(lst) == 2 else None

def single(lst):
    return lst[0] if len(lst) == 1 else None

def expandString(s, scope, name, date):
    # 1. replace %NAME and %SCOPE
    s1 = s.replace('%NAME', name).replace('%SCOPE', scope)
    # 2. use strftime format to replace date placeholders
    return date.strftime(s1)

def sysExec(*lst):
    os.execvp(lst[0], lst)

def subExec(*lst):
    subprocess.call(lst, stdout=sys.stdout)

def findInDir(path, query):
    subExec('grep', '--recursive', '--ignore-case', '--color=auto', query, path)
