def wordcount(file):
    infile = open(file, "r")
    count = 0

    for line in infile:
        word_list = line.split()
        for word in word_list:
            word.rstrip(".,?!")
            count += 1

    print(count, "Amount of Words")


filename = input("Enter filename: ")
wordcount(filename)
