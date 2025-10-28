name="szzpect" #this is string 

name='szzpect' #this is also string

name='''szzpect
szzpect szzpect ''' #this is multiline string 

#string length
#eg 
a="szzpect"
b=len(a)
print("line 12:",b)

#string slicing 
name2="s z z p e c t"
 #     0 1 2 3 4 5 6
 #     -7-6-5-4-3-2-1  
name1="szzpect"
shortname=name2[2:5]
print("line 20:",shortname)

name2="szzpect"
print("line 23:",name2[:5])
name3="szzpect"
print("line 25:",name3[0:]) #if we dont put end index eg [1:_] then _ be consider as lenght of string 
                  # here lenght of string is '7' so it is quuivalent [1:_] [1:7]


# Negative   Indices 

# Eg "s z z p e c t"
 #    0 1 2 3 4 5 6
 #    -7-6-5-4-3-2-1  
name4="szzpect"
c=name4[-7:-1] #but dont use negative indices just convert them into posive using line 31,32,33
print("line 36:",c)

#check sattement true or false using string
name3="Szzpect"
print("line 40:",name3.endswith("Sa")) # output is false becuase its ends with Sz , also cpital small alphabet matter

#string replace funtion
a="szzpect is good good boy"
print("line 44:",a.replace("good", "bad"))

#so if i want to change only one good to bad the first good not both then?
a = "szzpect is a good good boy"
b = a.replace("good", "bad", 1)
print("line 49" ,"replaced", b)
