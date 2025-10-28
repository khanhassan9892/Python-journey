#start of Program for converting celsius to kelvin
try:
    C=float(input("Enter temperature in celsius sir: "))
    K = C + 273.15
    print("Temperature in kelvin is: ",K,"K")
except ValueError:
    print("Please enter a valid number :)")

