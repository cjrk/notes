#!/usr/bin/env python3

import os
from os.path import expanduser
import sys
import datetime
from util import env, read_config
from util import filterStringsFrom, filterDatesFrom, filterOptionsFrom
from util import firstFromTwo, secondFromTwo, single
from util import expandString, sysExec, assureFile, assureDirFor, findInDir

# init config
DEFAULT_CONFIG = """
[journal]
editor = nano
basepath = ~/journals
filename = %Y/%m/%d/%NAME.md
template = ## %A, %d.%m.%Y (KW %W) 

[notes]
editor = nano
basepath = ~/notes
filename = %NAME.md
template = ## %NAME
"""

config = read_config(os.path.join(env('HOME'), '.config', 'notes', 'config.ini'), DEFAULT_CONFIG)

### get arguments

appname = os.path.basename(sys.argv[0])
arguments = sys.argv[1:]
stringArgs = filterStringsFrom(arguments)
dateArgs = filterDatesFrom(arguments) # returns already parsed dates
optionArgs = filterOptionsFrom(arguments)


## Search in notes
# $ notes --find lel
# - search in 'notes' basedir for lel

# $ notes --find-all lel
# - search in every beasedir for lel
# first, let's check if we just want to --find

if single(optionArgs) == '--find-all' and single(stringArgs):
    query = single(stringArgs)
    scopes = config().sections()
    for scope in scopes:
        if config(scope, 'basepath'):
            print()
            print('Find in', scope)
            findInDir(expanduser(config(scope, 'basepath')), query)

elif single(optionArgs) == '--find' and single(stringArgs):
    query = single(stringArgs)
    scope = appname
    if config(scope, 'basepath'):
        print('Find in', scope)
        findInDir(expanduser(config(scope, 'basepath')), query)


## Edit notes
# $ notes idm
# - scope: from appname
# - name: idm
# - date: defaults to today

# $ notes 
# - scope: defaults to appname (notes)
# - name: defaults to scope (notes)
# - date: defaults to today

# $ notes mynotes idm
# - scope: mynotes
# - name: idm
# - date: defaults to today

# $ notes mynotes idm +1
# - scope: mynotes
# - name: idm
# - date: tomorrow

# $ notes mynotes idm -1w
# - scope: mynotes
# - name: idm
# - date: 1 week before

# $ notes mynotes idm +1y -1d
# - scope: mynotes
# - name: idm
# - date: yesterday in a year

else:
    scope = firstFromTwo(stringArgs) or appname
    name = secondFromTwo(stringArgs) or single(stringArgs) or scope
    date = datetime.date.today()
    for dateTransformer in dateArgs:
        date = dateTransformer(date)


    ### get config values
    basepath = config(scope, 'basepath')
    filename = config(scope, 'filename')
    fullpath = os.path.join(basepath, filename)
    editor = env('NOTES_EDITOR') or config(scope, 'editor') or env('EDITOR') or 'nano'


    expandedPath = os.path.expanduser(expandString(fullpath, scope, name, date))
    template = config(scope, 'template')
    if template:
        assureFile(expandedPath, expandString(template, scope, name, date))
    assureDirFor(expandedPath)
    sysExec(editor, expandedPath)
