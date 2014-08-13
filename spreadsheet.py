import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os

import settings

#bot row name:
ROBOCOLUMN = 'robot'

class Spreadsheet(object):
    def __init__(self, username, password, doc, worksheet):
        print username + password
        self.client = gdata.spreadsheet.service.SpreadsheetsService()
        self.client.email = username
        self.client.password = password
        self.client.ProgrammaticLogin()
        self.worksheet = worksheet
        self.doc = doc
        #magical devletter bot stuff
        #probably deprecated to shit
        #definitely not up to standards with the current v3 docs api
        q = gdata.spreadsheet.service.DocumentQuery()
        q['title'] = self.doc
        q['title-exact'] = 'true'
        feed = self.client.GetSpreadsheetsFeed(query=q)
        spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
        feed = self.client.GetWorksheetsFeed(spreadsheet_id)
        #is this how it even works? D:
        worksheet_id = feed.entry[self.worksheet-1].id.text.rsplit('/',1)[1]
        self.rows = self.client.GetListFeed(spreadsheet_id, worksheet_id).entry


    #normally, I think a generator would be good here, but that doesn't
    #quite mesh with the relatively stateless nature of the project
    #oh well, hideous runtime it is then
    #thank god this is just a one-off tool and we don't have a Real Data-sized
    #DB
    #wait, if this is one-off, why am I making it all flexible?
    def get_next_row(self):
        for row in self.rows:
            if row.custom.get(ROBOCOLUMN).text == None:
                for i in row.custom:
                    if row.custom.get(i).text == None:
                        row.custom[i] = ''
                    else:
                        row.custom[i] = str(row.custom.get(i).text.encode('utf-8'))
                #row.custom[ROBOCOLUMN] = 'beep!'
                row.custom[ROBOCOLUMN] = ''
                self.client.UpdateRow(row, row.custom)
                print 'updated row'
                return row
        #nothing left!
        return None
