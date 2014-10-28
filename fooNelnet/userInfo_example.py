#username and password for logging into Nelnet.net
NELNET_USERNAME = 'your_nelnet_username'
NELNET_PASSWORD = 'your_nelnet_password'

# name of csv file to locally store loan info:
# you can modify these if you want
CSV_FILE_NAME = 'nelnetLoanData.csv'
PAYMENT_CSV_FILE_NAME = 'nelnetPayments.csv'

#Google Data API values
#You will have to setup your own google api client id and client secret if you want to post data to google docs
GDATA_CLIENT_ID = 'your_google_apps_client_id'
GDATA_SECRET = 'your_google_apps_oauth2_secret'
#the name of the spreadsheet to store loan data
GSPREADSHEET_NAME = 'Nelnet Loan Info'
# the name of the worksheet that stores loan status data within the GSPREADSHEET_NAME spreadsheet
GSPREADSHEET_WORKSHEET_NAME = 'Loan Info'
# the name of the worksheet that stores loan payment history within the GSPREADSHEET_NAME spreadsheet
GSPREADSHEET_PAYMENT_WORKSHEET_NAME = 'Loan Payments'

#The $ amount you want to automatically spend per month
#this gets divided by the number of days in the month when daily payments are made
MONTHLY_PAYMENT_AMOUNT = 1000
