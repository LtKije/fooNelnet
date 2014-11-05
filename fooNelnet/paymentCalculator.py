import datetime
from userInfo import PAYMENT_CSV_FILE_NAME 
from userInfo import MONTHLY_PAYMENT_AMOUNT 

def calculateNextPayment():
    #get the date of our last payment
    fh = open(PAYMENT_CSV_FILE_NAME, 'rb')
    first = fh.readline()
    fh.seek(-2, 2)
    while fh.read(1) != "\n":
        fh.seek(-2, 1)
    last = fh.readline()
    lastDate = datetime.datetime.strptime(last.split(',')[0], "%Y/%m/%d %H:%M:%S")
    currentDate = datetime.datetime.now()
    delta = currentDate - lastDate
    return round((MONTHLY_PAYMENT_AMOUNT * 12.0 / 365.0) * delta.days, 2)
    
    
   