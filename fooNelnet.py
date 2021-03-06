#!/usr/bin/python

"""A better autopayment system for Nelnet users.

..moduleauthor:: Jacob Boyle <jacob.boo.boyle@gmail.com>

fooNelnet is a web bot that can automatically record loan status data from Nelnet and save it in a google spreadsheet. It can also automatically initiate payments.

I built fooNelnet because I wanted to keep better track of my student loans, and I found the process of getting loan status data from Nelnet into a spreadsheet rather painful to do manually. Once I had the platform built I realized that I could also use to make automated payments. I determined that since student loans accrue interest at a daily rate, if you make daily payments you save on interest over the life of the loan. So I added a feature that enables fooNelnet to make small daily loan payments instead of a single large monthly one.

Be aware that fooNelnet will take tell Nelnet to initiate money transfers out of you bank account. There are no sanity checks, so if set up improperly it could empty or overdraw on your account.

fooNelnet is named after the classic programming term "foo." The fact that you could phonetically respell it as FU-Nelnet is entirly coincidental.

Usage:
    ./fooNelnet.py [-record_data] [-make_payment]

"""

import sys
import os.path
import time
import string
import datetime
from calendar import monthrange

from fooNelnet.userInfo import USERNAME
from fooNelnet.userInfo import PASSWORD
from fooNelnet.userInfo import MONTHLY_PAYMENT_AMOUNT
from fooNelnet.userInfo import PAYMENT_RATE_DAYS
from fooNelnet.appendToCSV import appendToCSV
from fooNelnet.appendToCSV import appendPaymentInfoToCSV
from fooNelnet.appendToCSV import append_DNA_info_to_csv
from fooNelnet.GDataClient import FooNelnetGoogleClient
from fooNelnet.nelnetClient import NelnetClient
from fooNelnet.paymentCalculator import calculate_payment_by_num_days
from fooNelnet.paymentCalculator import get_days_since_last_payment

def main(retain_data=True, make_payment=False):
    #check to see if payment interval has passed:
    num_days = get_days_since_last_payment()
    if num_days < PAYMENT_RATE_DAYS:
        print "no payments to make: {0}".format(num_days)
        return
    
    print 'making payment'
    print 'getting loan data from nelnet...'
    client = NelnetClient()
    client.log_in(USERNAME, PASSWORD)
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
        amount = calculate_payment_by_num_days(num_days)
        client.make_payment(payment_data[0]['account'], payment_data[0]['name'], amount)

        #now we need to retain the payment data for our records:
        appendPaymentInfoToCSV(payment_data[0]['name'], amount)
        gclient.sendPaymentInfoToGData(payment_data[0]['name'], amount)
    
        
if __name__=='__main__':
    rd = False
    mp = False
    if '-record_data' in sys.argv: rd = True
    if '-make_payment' in sys.argv: mp = True
    sys.exit(main(rd, mp))