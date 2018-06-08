import string
max = 10
password = "test"
characters = string.printable
#characters = string.ascii_letters
#characters = string.ascii_lowercase
#characters = string.ascii_uppercase
#characters = string.digits


for i in range(max):
    attempts = [c for c in characters]
    for j in range(i):
        attempts = [s+c for c in characters for s in attempts]
    for attempt in attempts:
        if attempt == password:
            print("password is: %s" % attempt)
            exit(0)
