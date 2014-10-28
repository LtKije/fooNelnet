import sys
import time

import httplib2
import pprint
import os.path
import gdata.gauth
import gdata.spreadsheets.client

import gdata.docs.client

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from gdata.spreadsheets.data import ListEntry

import pickle
import logging


#Google Data API values
from userInfo import GDATA_CLIENT_ID
from userInfo import GDATA_SECRET
from userInfo import GSPREADSHEET_NAME
from userInfo import GSPREADSHEET_WORKSHEET_NAME
from userInfo import GSPREADSHEET_PAYMENT_WORKSHEET_NAME

class FooNelnetGoogleClient:
    
    _auth2token = None
    _gd_client = None
    _ss_client = None
    _reauthorize = None
    
    def get_column_by_index(self, index):
        ordInd = ord('A')
        c = index // 26
        m = index % 26
        if c > 0:
            return chr(ordInd + c - 1) + chr(ordInd + m)
        else:
            return chr(ordInd+m)
    
    def get_oauth_token(self):
        if self._auth2token is not None: return self._auth2token
        # Check https://developers.google.com/drive/scopes for all available scopes
        OAUTH_SCOPE = 'https://docs.google.com/feeds/ https://spreadsheets.google.com/feeds/'
        # Redirect URI for installed apps
        REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
        
        storage_fname = 'oauth-fooNelnet'
        #first we check if the authorization file exists
        if not self._reauthorize and os.path.isfile(storage_fname):
            storage = Storage(storage_fname)
            credentials = storage.get()
        else:
            # Run through OAuth Flow and check credentials:
            flow = OAuth2WebServerFlow(GDATA_CLIENT_ID, GDATA_SECRET, OAUTH_SCOPE, REDIRECT_URI)
            authorize_url = flow.step1_get_authorize_url()
            print 'Go to the following link on your browser: ' + authorize_url
            code = raw_input('Enter verification code: ').strip()
            credentials = flow.step2_exchange(code)
    
            # Save it to a file:
            storage = Storage(storage_fname)
            storage.put(credentials)
    
        #authorize transaction
        http = httplib2.Http()
        http = credentials.authorize(http)
    
        self._auth2token = gdata.gauth.OAuth2TokenFromCredentials(credentials)
        return self._auth2token
    
    def partial_oauth_request(self):
        OAUTH_SCOPE = 'https://docs.google.com/feeds/ https://spreadsheets.google.com/feeds/'
        # Redirect URI for installed apps
        REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
        
        storage_fname = 'oauth-fooNelnet'
        
        flow = OAuth2WebServerFlow(GDATA_CLIENT_ID, GDATA_SECRET, OAUTH_SCOPE, REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link on your browser: ' + authorize_url
        
        pickle.dump(flow, open( "flow.p", "wb"))
        
    def partial_oauth_confirm(self, confirm_code):
        storage_fname = 'oauth-fooNelnet'
        flow = pickle.load( open("flow.p", "rb"))
        
        credentials = flow.step2_exchange(confirm_code)

        # Save it to a file:
        storage = Storage(storage_fname)
        storage.put(credentials)
    
    def get_docs_client(self):
        if self._gd_client is not None: return self._gd_client
        
        auth2token = self.get_oauth_token()
        self._gd_client = gdata.docs.client.DocsClient()
        self._gd_client = auth2token.authorize(self._gd_client)
        return self._gd_client
        
    def get_spreadsheets_client(self):
        if self._ss_client is not None: return self._ss_client
        
        auth2token = self.get_oauth_token()
        self._ss_client = gdata.spreadsheets.client.SpreadsheetsClient()
        self._ss_client = auth2token.authorize(self._ss_client)
        return self._ss_client
    
    def get_or_create_spreadsheet(self, spreadsheet_name):
        gd_client = self.get_docs_client()
        
        #find the spreadsheet or create if it doesn't exist
        query = gdata.docs.client.DocsQuery(
            title=spreadsheet_name
        )
        
        resources = gd_client.GetResources(q=query)
        spreadsheet = None
        #check if the spreadsheet is empty
        if not resources.entry:
            #create a new spreadsheet
            print 'creating spreadsheet named: ' + spreadsheet_name
            spreadsheet = gdata.docs.data.Resource(type='spreadsheet', title=spreadsheet_name)
            spreadsheet = gd_client.CreateResource(spreadsheet)
        else:
            spreadsheet = resources.entry[0]
        
        spreadsheet_key = spreadsheet.GetId().split("%3A")[1]
        return spreadsheet_key
        
    def sendToGData(self, loan_data, reauthorize=False):
        self._reauthorize = reauthorize
        
        spreadsheet_key = self.get_or_create_spreadsheet(GSPREADSHEET_NAME)
        
        #now we put the data into the spreadsheet
        ss_client = self.get_spreadsheets_client()
        
        #check to make sure we have the correct worksheet
        worksheets = ss_client.GetWorksheets(spreadsheet_key)
        ws_id = None
        for sheet in worksheets.entry:
            if sheet.title.text == GSPREADSHEET_WORKSHEET_NAME: ws_id = sheet.GetWorksheetId()
        
        if not ws_id:
            #we need to create the worksheet:
            print 'creating worksheet named: ' + GSPREADSHEET_WORKSHEET_NAME
            worksheet = ss_client.AddWorksheet(spreadsheet_key, GSPREADSHEET_WORKSHEET_NAME, 1, len(loan_data)*4 + 1)
            ws_id = worksheet.GetWorksheetId()
            
            #generate header names and add via cells batch request:
            cells_feed = ss_client.GetCells(spreadsheet_key, ws_id)
            cells_feed.add_set_cell(1, 1, 'date')
    
            ind = 2
            for loan_info in loan_data:
                cells_feed.add_set_cell(1, ind, loan_info['name']+'_account')
                cells_feed.add_set_cell(1, ind+1, loan_info['name']+'_principle_balance')
                cells_feed.add_set_cell(1, ind+2, loan_info['name']+'_interest_rate')
                cells_feed.add_set_cell(1, ind+3, loan_info['name']+'_accrued_interest')
                cells_feed.add_set_cell(1, ind+4, loan_info['name']+'_outstanding_balance')
                ind += 4
            
            updated = ss_client.Batch(cells_feed, cells_feed.FindBatchLink(), force=True)
        
        #add the row
        rowDict = {'date':time.strftime("%Y/%m/%d %H:%M:%S")}
        for loan_info in loan_data:
            rowDict[loan_info['name'].lower()+'account'] = loan_info['account']
            rowDict[loan_info['name'].lower()+'principlebalance'] = loan_info['principle_balance']
            rowDict[loan_info['name'].lower()+'interestrate'] = loan_info['interest_rate']
            rowDict[loan_info['name'].lower()+'accruedinterest'] = loan_info['accrued_interest']
            rowDict[loan_info['name'].lower()+'outstandingbalance'] = loan_info['outstanding_balance'] 
            
        listEntry = gdata.spreadsheets.data.ListEntry()
        listEntry.from_dict(rowDict)
        ss_client.AddListEntry(listEntry, spreadsheet_key, ws_id)
    
    def sendPaymentInfoToGData(self, loan_name, amount, reauthorize=False):
        self._reauthorize = reauthorize
        spreadsheet_key = self.get_or_create_spreadsheet(GSPREADSHEET_NAME)
        
        #now we put the data into the spreadsheet
        ss_client = self.get_spreadsheets_client()
        
        #check to make sure we have the correct worksheet
        worksheets = ss_client.GetWorksheets(spreadsheet_key)
        ws_id = None
        for sheet in worksheets.entry:
            if sheet.title.text == GSPREADSHEET_PAYMENT_WORKSHEET_NAME: ws_id = sheet.GetWorksheetId()
        
        if not ws_id:
            #we need to create the worksheet:
            print 'creating worksheet named: ' + GSPREADSHEET_PAYMENT_WORKSHEET_NAME
            worksheet = ss_client.AddWorksheet(spreadsheet_key, GSPREADSHEET_PAYMENT_WORKSHEET_NAME, 1, 3)
            ws_id = worksheet.GetWorksheetId()
            
            #generate header names and add via cells batch request:
            cells_feed = ss_client.GetCells(spreadsheet_key, ws_id)
            cells_feed.add_set_cell(1, 1, 'date')
            cells_feed.add_set_cell(1, 2, 'loan')
            cells_feed.add_set_cell(1, 3, 'payment amount')
            
            updated = ss_client.Batch(cells_feed, cells_feed.FindBatchLink(), force=True)
        
        #add the row
        rowDict = {'date':time.strftime("%Y/%m/%d %H:%M:%S"), 'loan':loan_name, 'paymentamount':str(amount)}
            
        listEntry = gdata.spreadsheets.data.ListEntry()
        listEntry.from_dict(rowDict)
        ss_client.AddListEntry(listEntry, spreadsheet_key, ws_id)
     
if __name__ == '__main__':
    reauthorize = False
    if "-reauthorize" in sys.argv:
        reauthorize = True
    
        
    client = FooNelnetGoogleClient()
    if sys.argv[1] == '-oauth_setup':
        if len(sys.argv) > 2:
            sys.exit( client.partial_oauth_confirm(sys.argv[2]))
       
        else:
            sys.exit( client.partial_oauth_request())
    #sys.exit( client.sendPaymentInfoToGData('A', '100') )