# So what does the main script do?
# 1. logs into nelnet
# 2. gets current loan data
# 3. saves data to csv file 
# THEN
# 4. asks you if you want to send it to a google spreadsheet
# 5. performs OAuth2 flow
# 6. checks for a spreadsheet "Nelnet Loans" and creates one if not found
# 7. checks for a worksheet "Status Record" and creates one if not found
# 	- and adds the first row to create a list
# 8. adds the loan info along with the date to the spreadsheet
# THEN
# 9. asks if you want to set up recurring updates
# 10. asks if you want to set up recurring payments

# LoanSolver Plan
# LoanSolver is the front-door to get people to sign up for fooNelet - and pay money (What is it about the gates of Hell that makes people just want to walk in 'em?)
# You basically get two sliders - one for the monthy payment amount and one for the total number of payments (i.e. the payoff date)
# By moving these sliders around you can see how the values effect each other and play around with repayment options.
# The trouble is that while it's simple to calculate the number of payments (payoff date) with user defined monthy rate, (i.e. a while loop)
# there's not really a good way of doing it the other way around.
# so we use interpolation/extrapolation instead
# when you put in the initial amount it makes the calculation and shows you your current plan.
# but behind the scenes it calculate a few additional points on the curve 
# then when you use the payoff date slider it does a linear interoplation between the pre-calculated points
# this gives you a quick estimate, which we also use as the input for a guess and check algorithm to get a more precise answer.
# this keeps the UI reponsive and maintains accuracy.
# and make Jeremy Gibson proud!

#

import sys
import os.path
import time
import string
import datetime
from calendar import monthrange

from fooNelnet.userInfo import NELNET_USERNAME
from fooNelnet.userInfo import NELNET_PASSWORD
from fooNelnet.userInfo import MONTHLY_PAYMENT_AMOUNT
from fooNelnet.appendToCSV import appendToCSV
from fooNelnet.appendToCSV import appendPaymentInfoToCSV
from fooNelnet.GDataClient import FooNelnetGoogleClient
from fooNelnet.seleniumClient import SeleniumClient

def main(retain_data=True, make_payment=False):
    print 'getting loan data from nelnet...'
    client = SeleniumClient()
    client.log_in(NELNET_USERNAME, NELNET_PASSWORD)
    data = client.retrieve_data()
    #we always need to sort it according to loan name - for both the csv and gdata
    sorted_data = sorted(data, key=lambda k:k['name'])
    gclient = FooNelnetGoogleClient()
    if retain_data:
        print 'adding data to csv'
        appendToCSV(sorted_data)
        print 'sending data to google spreadsheet'
        gclient.sendToGData(sorted_data)
        
    if make_payment:
        payment_data = sorted(data, key=lambda k:float(k['interest_rate']), reverse=True)
        #get number of days in month
        now = datetime.datetime.now()
        month_range = monthrange(now.year, now.month)
        amount = round(float(MONTHLY_PAYMENT_AMOUNT) / float(month_range[1]), 2)
        #p_client = SeleniumClient()
        #p_client.log_in(NELNET_USERNAME, NELNET_PASSWORD)
        client.make_payment(payment_data[0]['account'], payment_data[0]['name'], amount)
        #makePayment(NELNET_USERNAME, NELNET_PASSWORD, payment_data[0]['account'], payment_data[0]['name'], amount)
        
        #now we need to retain the payment data for our records:
        appendPaymentInfoToCSV(payment_data[0]['name'], amount)
        gclient.sendPaymentInfoToGData(payment_data[0]['name'], amount)
    
        
if __name__=='__main__':
    rd = False
    mp = False
    if '-record_data' in sys.argv: rd = True
    if '-make_payment' in sys.argv: mp = True
    sys.exit(main(rd, mp))
    #sys.exit(make_payment())