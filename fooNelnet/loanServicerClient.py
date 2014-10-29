class NotLoggedInError(Exception):
    pass
class NotImplementedError(Exception):
    pass

class LoanServicerClient:
    """Base class for Loan Servicer Clients
    
    .. note::
        This app could work just as well with other loan servicers such as Sally Mae, Navient, etc.
        This base class provides a level of abstractions so that the other servicers could be added easily without modifing other functionality in the app.
    
    """
    logged_in = False
    def login(self, username, password):
        """Logs into the loan servicers website, and sets the session and cookies for subsequent operations
        
        Args:
            username(string): The username for the loan servicer account
            password(string): The password for the loan servicer account
            
        ..note:: Usually uses USERNAME and PASSWORD from userInfo.py
        
        """
        raise NotImplementedError()
    
    def retrive_data(self):
        """Retreives loan data from the servicer
        
            Returns: loan_data (list): A list of dictionaries containing the following keys:
                    - account: The name of the account
                    - principle_balance: The current principle balance of the loan
                    - interest_rate: The loan's interest rate
                    - accrued_interest: The current amount of accrued interest on the loan
                    - outstanding_balance: The total balance on the loan (principal + accrued interest)
        
        """
        raise NotImplementedError()
        
    def make_payment(self, account, loan, amount):
        """Tells the servicer to initiate a payment request from a preprovided bank account
        
            Args:
                account(string): the name or id of the loan account
                loan(string): the name of the loan - usually something like "A," "B," "C," etc.
                amount(number): the amount to pay
        """
        raise NotImplementedError()
        


