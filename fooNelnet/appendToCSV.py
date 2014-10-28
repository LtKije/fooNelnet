import sys
import os.path
import time
import string

from userInfo import CSV_FILE_NAME
from userInfo import PAYMENT_CSV_FILE_NAME

def appendToCSV(loan_data):
    # generate csv data line
    line = time.strftime("%Y/%m/%d %H:%M:%S")
    for loan_info in loan_data:
        needed_values = [
            loan_info['account'],
            loan_info['principle_balance'].replace(',',''), 
            loan_info['interest_rate'].replace(',',''), 
            loan_info['accrued_interest'].replace(',',''),
            loan_info['outstanding_balance'].replace(',','')
        ]
        line += ',' + ','.join(needed_values)
        
    if os.path.isfile(CSV_FILE_NAME):
        # just append to the end
        fd = open(CSV_FILE_NAME, 'a')
        fd.write(line + '\n')
        fd.close()
    else:
        # create the file, add column names for the first row, then write the current data
        column_names = 'date'
        for loan_info in loan_data:
            needed_values = [
                loan_info['name']+'_account',
                loan_info['name']+'_principle_balance',
                loan_info['name']+'_interest_rate', 
                loan_info['name']+'_accrued_interest',
                loan_info['name']+'_outstanding_balance'
            ]
            column_names += ',' + ','.join(needed_values)
            
        fd = open(CSV_FILE_NAME, 'w')
        fd.write(column_names + '\n')
        fd.write(line + '\n')
        fd.close()
        
def appendPaymentInfoToCSV(loan_name, amount):
    line = '%s,%s,%s' % (time.strftime("%Y/%m/%d %H:%M:%S"), loan_name, amount)
    if os.path.isfile(PAYMENT_CSV_FILE_NAME):
        #we just need to append
        fd = open(PAYMENT_CSV_FILE_NAME, 'a')
        fd.write(line + '\n')
        fd.close()
    else:
        fd = open(PAYMENT_CSV_FILE_NAME, 'w')
        fd.write('date,loan,amount\n')
        fd.write(line + '\n')
        fd.close()