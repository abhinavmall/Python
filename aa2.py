#balance - the outstanding balance on the credit card
#annualInterestRate - annual interest rate as a decimal
#monthlyPaymentRate - minimum monthly payment rate as a decimal

#Monthly interest rate= (Annual interest rate) / 12.0
#Minimum monthly payment = (Minimum monthly payment rate) x (Previous balance)
#Monthly unpaid balance = (Previous balance) - (Minimum monthly payment)
#Updated balance each month = (Monthly unpaid balance) + (Monthly interest rate x Monthly unpaid balance)
balance = 42; annualInterestRate = 0.2; monthlyPaymentRate = 0.04
# 31.38
mir = annualInterestRate/12.0

for i in range(12):
    mmp = monthlyPaymentRate * balance
    mub = balance - mmp
    balance = mub + (mir*mub)

print("%.2f" % round(balance,2))
