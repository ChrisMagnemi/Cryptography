#basic number-theoretic algorithms

def euclid(num1,num2):
    while num2 != 0:
        (num1,num2)=(num2,num1 % num2)
    return num1

def extended_euclid(num1,num2):
    #given values x,y return
    #(gcd(x,y),r,s) where r*x+s*y=gcd(x,y)
        (a,b,aa,bb)=(0,1,1,0)
        while num2 !=0:
            (q,r)=divmod(num1,num2)
            (a,b,aa,bb)=(aa-q*a,bb-q*b,a,b)
            (num1,num2)=(num2,r)
        return (num1,(aa,bb))

#This is already built into Python as
#pow(base,exponent,modulus)

def repeated_squaring(base,exponent,modulus):
    power=1
    basepower=base
    while exponent>0:
        (exponent,remainder)=divmod(exponent,2)
        if remainder==1:
            power=(power*basepower)%modulus
        basepower=(basepower**2)%modulus
    return power
