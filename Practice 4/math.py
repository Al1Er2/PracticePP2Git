import math

degree = float(input("Input degree: "))
radian = math.radians(degree)

print("Output radian:", radian)



height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = (base1 + base2) / 2 * height

print("Expected Output:", area)



import math

n = int(input("Input number of sides: "))
a = float(input("Input the length of a side: "))

area = (n * a ** 2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", area)




base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print("Expected Output:", area)
