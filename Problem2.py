#Monthly interest rate = (Annual interest rate) / 12.0
#Monthly unpaid balance = (Previous balance) - (Minimum fixed monthly payment)
#Updated balance each month = (Monthly unpaid balance) + (Monthly interest rate x Monthly unpaid balance)

#balance - the outstanding balance on the credit card
#annualInterestRate - annual interest rate as a decimal

mir = annualInterestRate/12.0
fmp = 10
b = balance
while True:
    b = balance
    for i in range(12):
        mub = b - fmp
        b = mub + (mir * mub)
    if b <= 0:
        break
    else:
        fmp += 10

print(fmp)
