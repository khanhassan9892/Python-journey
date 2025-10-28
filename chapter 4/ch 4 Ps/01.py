Fruitlist=[]
Fruitlist = []

f1 = input("Enter the first fruit name: ")
Fruitlist.append(f1)

f2 = input("Enter the second fruit name: ")
Fruitlist.append(f2)

f3 = input("Enter the third fruit name: ")
Fruitlist.append(f3)

f4 = input("Enter the fourth fruit name: ")
Fruitlist.append(f4)

f5 = input("Enter the fifth fruit name: ")
Fruitlist.append(f5)

f6 = input("Enter the sixth fruit name: ")
Fruitlist.append(f6)
import ast

Fruitlist = []

for i in range(6):
    user_input = input(f"Enter fruit {i+1}: ")
    try:
        value = ast.literal_eval(user_input)
    except (ValueError, SyntaxError):
        value = user_input
    Fruitlist.append(value)

print(Fruitlist)


