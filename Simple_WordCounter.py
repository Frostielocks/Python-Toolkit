import sys

def wordcount(file):
    infile = open(file, "r")
    count = 0

    for line in infile:
        word_list = line.split()
        for word in word_list:
            word.rstrip(".,?!")
            count += 1

    print(count, "word(s) in file.")


wordcount(sys.argv[1])
