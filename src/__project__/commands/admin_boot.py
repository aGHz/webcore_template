"""
This file is run by the admin command before starting a shell.
"""

from __project__.util import ansi
_ansi = {
    'mdl': ansi.green,
    'cls': ansi.blue,
    'obj': ansi.yellow,
    'func': ansi.cyan,
    'r': ansi.reset
}

print ''
print 'Available {mdl}modules{r}, {cls}classes{r}, {obj}objects{r} and {func}functions{r}'.format(**_ansi)
print '-' * 49
print 'import {mdl}web{r}'.format(**_ansi)
import web
print 'from web.core import {mdl}http{r}, {cls}Controller{r}, {obj}request{r}, {obj}response{r}'.format(**_ansi)
from web.core import http, Controller, request, response
#print 'from __project__ import {obj}settings{r}'.format(**_ansi)
#from __project__ import settings
#print 'from __project__.model import session as {obj}db{r}'.format(**_ansi)
#from __project__.model import session as db
print '{obj}app{r} = paste.fixture.TestApp'.format(**_ansi)
print "          Make requests with app.get('<path>'), app.post('<path>', params='<params>'), etc."

print 'from datetime import {cls}date{r}, {cls}time{r}, {cls}datetime{r}'.format(**_ansi)
from datetime import date, time, datetime
#print 'from dateutil.relativedelta import {cls}relativedelta{r}'.format(**_ansi)
#from dateutil.relativedelta import relativedelta
#print 'from pytz import {cls}timezone{r}, {obj}utc{r}'.format(**_ansi)
#from pytz import timezone, utc
print 'from pprint import {func}pprint{r}'.format(**_ansi)
from pprint import pprint

print ''
print 'Admin shell'
print '-' * 11,
