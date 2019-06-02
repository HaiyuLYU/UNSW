# Written by *** and Eric Martin for COMP9021


'''
Prompts the user for two strictly positive integers, numerator and denominator.

Determines whether the decimal expansion of numerator / denominator is finite or infinite.

Then computes integral_part, sigma and tau such that numerator / denominator is of the form
integral_part . sigma tau tau tau ...
where integral_part in an integer, sigma and tau are (possibly empty) strings of digits,
and sigma and tau are as short as possible.
'''


import sys
from math import gcd
from math import sqrt
from fractions import Fraction

try:
    numerator, denominator = input('Enter two strictly positive integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    numerator, denominator = int(numerator), int(denominator)
    if numerator <= 0 or denominator <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()


has_finite_expansion = True
integral_part = 0
sigma = ''
tau = ''
#Task 1
def isPrime(N):
    prime_l=list(range(2,N+1))
    i=0
    while prime_l[i]<=round(sqrt(N)):
        k=0
        while 1:
            factors=prime_l[i]*prime_l[i+k]
            if factors>N:
                break
            else:
                while factors<=N:
                    prime_l.remove(factors)
                    factors=factors*prime_l[i]
            k=k+1
        i=i+1
    return prime_l
primeList=isPrime(100)
primeList.remove(2)
primeList.remove(5)
l=Fraction(numerator, denominator)
newDenominator=l.denominator
if numerator%denominator==0:
	has_fanite_expansion=True
else:
	for e in primeList:
		if newDenominator%e==0:
			has_finite_expansion=False
			break
#Task2
if numerator%denominator==0:
	integral_part=int(numerator/denominator)
elif has_finite_expansion==True:
	integral_part=int(numerator/denominator)
	not_integral_part=numerator/denominator-integral_part
	s1=str(not_integral_part)
	sigma=s1[2:]
else:
	integral_part=int(numerator/denominator)
	fz=numerator
	fm=denominator
	list1=[]#jieguo
	list2=[]#Chushu
	cs=fz*10#Chushu
	while True:
		list1.append(int(cs/fm))
		ys=cs%fm
		if int(cs/10) not in list2:
			list2.append(int(cs/10))
		else:
			wz=list2.index(cs/10)
			break
		cs=ys*10
	list3=list1[:-1:]
	list4=list3[0:wz]
	list5=list3[wz:]
	for i in range (len(list4)):
		sigma=sigma+str(list4[i])
	for i in range(len(list5)):
		tau=tau+str(list5[i])
if has_finite_expansion:
    print(f'\n{numerator} / {denominator} has a finite expansion')
else:
    print(f'\n{numerator} / {denominator} has no finite expansion')
if not tau:
    if not sigma:
        print(f'{numerator} / {denominator} = {integral_part}')
    else:
        print(f'{numerator} / {denominator} = {integral_part}.{sigma}')
else:
    print(f'{numerator} / {denominator} = {integral_part}.{sigma}({tau})*')

