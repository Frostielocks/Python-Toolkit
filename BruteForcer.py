class BruteForcer:
    characters = str() # characters to be used


    def __init__(self, characters):
        self.characters = characters


    def file_bruteforce(self, password, depth=10, file1="temp1.txt", file2="temp2.txt"):
        for i in range(depth):
            fd1 = open(file1, "w")
            for c in self.characters:
                fd1.write(c + "\n")
            fd1.close()

            for j in range(i):
                fd1 = open(file1, "r")
                fd2 = open(file2, "w")
                for s in fd1:
                    s = s[0: len(s)-1]
                    for c in self.characters:
                        fd2.write(s + c + "\n")
                fd1.close()
                fd2.close()
                temp = file1
                file1 = file2
                file2 = temp

            fd1 = open(file1, "r")
            for line in fd1:
                attempt = line[0: len(line)-1]
                if attempt == password:
                    return "password is: %s" % attempt
        return "Couldn't crack password :/"


    def mem_bruteforce(self, password, depth=10):
        for i in range(depth):
            attempts = [c for c in self.characters]
            for j in range(i):
                attempts = [s+c for c in self.characters for s in attempts]
            for attempt in attempts:
                if attempt == password:
                    return "password is: %s" % attempt
        return "Couldn't crack password :/"
