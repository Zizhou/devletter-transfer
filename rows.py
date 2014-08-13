import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os
import random


#janky credentials (because ain't nobody got time for OAuth)
username = 'iggdevletterbot@gmail.com'
password = 'iamrobot'

#this is so lazy (and remember to change this)
doc = '2013 Test List'
#doc = '2013 Games List'
worksheet_number = 1

#login
client = gdata.spreadsheet.service.SpreadsheetsService()
client.email = username
client.password = password
client.ProgrammaticLogin()


#I'll admit, this part is pretty much just magic
q = gdata.spreadsheet.service.DocumentQuery()
q['title'] = doc
q['title-exact'] = 'true'
feed = client.GetSpreadsheetsFeed(query=q)
#could check other worksheets by incrementing the entry number, but meh
spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
feed = client.GetWorksheetsFeed(spreadsheet_id)
worksheet_id = feed.entry[worksheet_number-1].id.text.rsplit('/',1)[1]

rows = client.GetListFeed(spreadsheet_id, worksheet_id).entry


#so fucking sloppy
#I should really decide what the conditions are before starting to write this
for row in rows:
    if row.custom.get('forbotuse').text == None:
        for i in row.custom:
            if row.custom.get(i).text == None:
                row.custom[i] = ''
            else:
                row.custom[i] = str(row.custom.get(i).text.encode('utf-8'))
        print type(row)
        print type(row.custom)
        row.custom['forbotuse'] = 'beep!'#sillyWord()
        client.UpdateRow(row, row.custom)
        

print 'done'
