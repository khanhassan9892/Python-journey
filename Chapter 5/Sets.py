# to create a empty set
e= set()
print(type(e))
# to create a empty dictionary
d= {}
print(type(d))



# Sets
s= {"szzpect", "wow", "why",}
s.add(11) # adding an element to set
print(s)

s1= {"szzpect", "wow", "why", "mm"}
s2= {"hello", "mm", "python"}
s1.union(s2) # union of two sets
print(s1.union(s2))

print(s1.intersection(s2)) # intersection of two sets

# Intersection mean = value which present in both sets
