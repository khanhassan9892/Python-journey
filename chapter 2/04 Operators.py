#Assignment operators
a=2
b=2
b=a+b #this will evaluate a+b
print(b)


b=3
b-=3 #this will redue 3 from b
print(b)

c=44
c*=2 #this will multiply c=44 by 2
print(c)

d=55
d/=5#this will divide d by 5
print(d)



# comparison operator -- comparsion operator always output Boolean(true or false)
a=5==5           #'==' mean equal to in comparsion operator
                 #'=' mean puting value on that container eg:a=5 mean we put 5 in a
print(a)





# Logical operator
# T and T #-- True
# T and F #--False
# T or T #--TruF
# T or F #--True

# example,
a=True or False 
print(a) #--output should True
a=False or False 
print(a) #--output should False


b=True and True
print(b) #--output should True
b=True and False
print(b) #--output should False

# !/not mean negation(~) eg. True its !/not/negation will be False
a=True and False #you see output should False but we used 'not' to make its negation
print(not(a))