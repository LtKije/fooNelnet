#base class for nelnet clients
#so we can interchange the mechanize client and the selenium client
#even though we really want to use the mechanize clinet

class NotLoggedInError(Exception):
    pass
class NotImplementedError(Exception):
    pass

class NelnetClient:
    logged_in = False
    def login(self, username, password):
        raise NotImplementedError()
    
    def retrive_data(self):
        raise NotImplementedError()
        
    def make_payment(self, account, loan, amount):
        raise NotImplementedError()
        


