from django.test import TestCase

from transfer.spreadsheet import Spreadsheet
from transfer.settings import settings
# Create your tests here.

def test1():
    s = Spreadsheet(**settings)
    print 'init done'
    while True:
        r = s.get_next_row()
        if r == None:
            break
        for i in r.custom:
            print i + ' ' + r.custom.get(i).text
    print 'done!'

def test2():
    s = Spreadsheet(**settings)
    return s.get_next_row()
