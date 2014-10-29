from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By as By

import sys

from lxml import etree

from loanServicerClient import LoanServicerClient
from loanServicerClient import NotLoggedInError

class NelnetClient(LoanServicerClient):
    """Primary Class for Interfacing with the Nelnet website
    
        ..note::
            Usually uses the values USERNAME and PASSWORD from userInfo.py
    """
    driver = None
    def __init__(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(10)
        
    def log_in(self, username, password):
        """Logs into nelnet.com, and sets the session and cookies for subsequent operations
        
        Args:
            username(string): The username for the nelnet account
            password(string): The password for the nelnet account
            
        ..note:: Usually uses USERNAME and PASSWORD from userInfo.py
        
        """
        self.driver.get("http://www.nelnet.net")

        #login page
        print "entering username"
        uname_element = self.driver.find_element_by_name("ctl00$txtUserName")
        uname_element.send_keys(username)
        submit_element = self.driver.find_element_by_name("ctl00$btnLogin")
        submit_element.click()

        #password page
        print "entering password"
        panel_element = self.driver.find_element_by_id("PageBodyPlaceHolder_PasswordPanel")
        #print panel_element.text()
        pword_element = self.driver.find_element_by_name("ctl00$PageBodyPlaceHolder$Pwd")
        pword_element.send_keys(password)
        submit_element = self.driver.find_element_by_name("ctl00$PageBodyPlaceHolder$Logon")
        submit_element.click()
        
        self.logged_in = True
    
    def retrieve_data(self):
        """Retreives loan data from nelnet
        
            Returns: loan_data (list): A list of dictionaries containing the following keys:
                    - account: The name of the account
                    - principle_balance: The current principle balance of the loan
                    - interest_rate: The loan's interest rate
                    - accrued_interest: The current amount of accrued interest on the loan
                    - outstanding_balance: The total balance on the loan (principal + accrued interest)
        
        """
        if not self.logged_in: raise NotLoggedInError()
        self.driver.get('http://mma.nelnet.net/Pages/LoanDetailsAndBenefits.aspx')
        parser = etree.HTMLParser()
        root = etree.fromstring(self.driver.page_source, parser)
        name_divs = root.xpath('//div[@class="bottom-border-dotted show-hide-switch content-full"]')
        details_divs = root.xpath('//div[@class="rounded-corner-box-simple item accordion"]')
        items = []
        for ind, div in enumerate(name_divs):
            item = {}
            item['account'] = div.xpath('table/tbody/tr/td/text()')[0].strip()
            item['full_name'] = " ".join(div.xpath('table/tbody/tr/td/text()')[1].split())
            item['name'] = item['full_name'][6]
            item['principle_balance'] = details_divs[ind].xpath('((.//table[1])/tbody/tr)[2]/td/text()')[0].strip();
            item['accrued_interest'] = details_divs[ind].xpath('((.//table[1])/tbody/tr)[3]/td/text()')[0].strip();
            item['outstanding_balance'] = details_divs[ind].xpath('((.//table[1])/tbody/tr)[5]/td/text()')[0].strip();
            item['interest_rate'] = details_divs[ind].xpath('((.//table[1])/tbody/tr)[6]/td/text()')[0].strip();
            item['due_date'] = details_divs[ind].xpath('((.//table[2])/tbody/tr)[2]/td/text()')[0].strip()
            items.append(item)
    
        return items
     
    def make_payment(self, account, loan, amount):
        """Tells nelnet to initiate a payment request from a preprovided bank account
        
            Args:
                account(string): the name or id of the loan account
                loan(string): the name of the loan - usually something like "A," "B," "C," etc.
                amount(number): the amount to pay
        """
        #make a payment page
        print "entering payment amount"
        self.driver.get("http://mma.nelnet.net/Pages/MakeAPayment.aspx")
        show_details_element = self.driver.find_element_by_name('%s_{0}_href' % account)
        show_details_element.click()
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME,'%s_%s_GroupPmtAmount' % (account, loan))))
            
            amount_element = self.driver.find_element_by_name('%s_%s_GroupPmtAmount' % (account, loan))
            amount_element.clear()
            amount_element.send_keys(str(amount))
            submit_element = self.driver.find_element_by_name("ctl00$MainContent$BtnMakeAPayment")
            submit_element.click()
        
            #confirmation page
            print "confirming payment"
            self.driver.find_element_by_name("agree").click()
            self.driver.find_element_by_id("BtnConfirm").click()
            
        finally:
            pass
            
    def __del__(self):
        self.driver.quit()