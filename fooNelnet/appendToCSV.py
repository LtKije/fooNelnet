import sys
import os.path
import time
import string

from userInfo import CSV_FILE_NAME
from userInfo import PAYMENT_CSV_FILE_NAME

def appendToCSV(loan_data):
    """Appends received loan data to a CSV file
    
    Args:
        loan_data (list): A list of dictionaries containing the following keys:
            - account: The name of the account
            - principle_balance: The current principle balance of the loan
            - interest_rate: The loan's interest rate
            - accrued_interest: The current amount of accrued interest on the loan
            - outstanding_balance: The total balance on the loan (principal + accrued interest)
    
    Output: Saves (or appends to) a local csv file - defined in userInfo.py
    
    """
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
        print line
        
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
    """Appends received loan data to a CSV file
    
    Args:
        loan_name (string): The name of the loan
        amount (number): The amount paid.
    
    Output: Saves (or appends to) a local csv file - defined in userInfo.py
    
    """
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

def append_DNA_info_to_csv(dna_info):
    """Appends DNA info to csv
    
    Nelnet - and maybe other providers - have a DNA Threshold for each loan. The loan will only advance the due date if the payment exceeds that threshold. I'm kind of worried that this will make it not recognize the smaller daily payments and slap me with late fees or something. 
    So I want to keep track of these values. Ideally they should go down according to the amount we pay each day.
    
    Args:
        dna_info (list): A list of dictionaries with the following keys:
            - account: the account+loan name
            - dna_threshold: the DNA Threshold on the loan
    """
    line = time.strftime("%Y/%m/%d %H:%M:%S")
    for threshold in dna_info:
        needed_values = [
            threshold['account'].replace(',', ''),
            threshold['dna_threshold'].replace(',', '')
        ]
        line += ',' + ','.join(needed_values)
    
    if os.path.isfile('DNAThresholds.csv'):
        # just append to the end
        fd = open('DNAThresholds.csv', 'a')
        fd.write(line + '\n')
        fd.close()
    else:
        # create the file, add column names for the first row, then write the current data
        column_names = 'date'
        for threshold in dna_info:
            needed_values = [
                threshold['account']+'_account',
                threshold['account']+'_dna_threshold'
            ]
            column_names += ',' + ','.join(needed_values)
            
        fd = open('DNAThresholds.csv', 'w')
        fd.write(column_names + '\n')
        fd.write(line + '\n')
        fd.close()