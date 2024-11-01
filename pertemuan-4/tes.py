import re

strin = "Term_1 Or Term_2"

print(re.split("AND", strin))
print(re.split("OR", strin))

print("and" in strin.lower())
print("or" in strin.lower())