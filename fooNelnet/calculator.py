round_to_n = lambda x, n: round(x, -int(floor(log10(x))) + (n - 1))

def computePaymentForMonth(amount, interest, monthly_payment):
    return (monthly_payment, round(amount * (interest/365.0) * 30, 2))
    
def computePaymentDaily(amount, interest, daily_payment):
    d_interest = interest / 365.0
    p_principle = 0
    p_interest = 0
    for i in range(30):
        p_interest += round(amount * d_interest, 2)
        p_principle += daily_payment
        amount -= daily_payment
        
    return (round(p_principle,2), round(p_interest,2))
    
if __name__=='__main__':
    print computePaymentForMonth(24387.02, .0825, 1000.0)
    print computePaymentDaily(24387.02, .0825, 1000.0/30)