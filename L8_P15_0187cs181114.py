a = {}
a = (1, 2, "rITIK")
print(a)
b = {}
if id(a) == id(b):
    print("yes", id(a), id(b))
else:
    print("No", id(a), id(b))
